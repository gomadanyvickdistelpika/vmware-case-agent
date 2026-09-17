from __future__ import annotations

import csv
import io
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile

from .analyzer import render
from .config import settings
from .knowledge import KnowledgeBase
from .memory import MemoryStore
from .models import AnalysisResponse, AnalyzeRequest
from .privacy import redact

memory = MemoryStore(settings.database_path)
knowledge = KnowledgeBase(settings.knowledge_dir)


@asynccontextmanager
async def lifespan(_: FastAPI):
    memory.initialize()
    yield


app = FastAPI(title="Dany Super Agent API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": "local-only", "infrastructure_execution": False}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalyzeRequest) -> AnalysisResponse:
    redacted = redact(request.text)
    content, findings, confidence, missing = render(
        request.workflow, redacted.text, request.product, request.version, request.external_action_approved
    )
    memory_id = None
    if request.save_to_memory:
        memory_id = memory.save(request.workflow, redacted.text, content, [item.model_dump() for item in findings.evidence], confidence)
    return AnalysisResponse(
        workflow=request.workflow, redacted_input=redacted.text, redactions=list(redacted.categories),
        content=content, evidence=findings.evidence, confidence=confidence,
        missing_evidence=missing, memory_id=memory_id,
    )


@app.post("/upload")
async def upload(file: UploadFile = File(...)) -> dict:
    suffix = (file.filename or "").lower().rsplit(".", 1)[-1]
    if suffix not in {"log", "txt", "csv"}:
        raise HTTPException(415, "Only .log, .txt, and .csv files are accepted")
    raw = await file.read(settings.max_upload_bytes + 1)
    if len(raw) > settings.max_upload_bytes:
        raise HTTPException(413, "File exceeds configured upload limit")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(400, "File must be UTF-8 text") from exc
    if suffix == "csv":
        rows = list(csv.reader(io.StringIO(text)))
        text = "\n".join(" | ".join(row) for row in rows)
    redacted = redact(text)
    return {"filename": file.filename, "redacted_text": redacted.text, "redactions": list(redacted.categories), "stored": False}


@app.get("/memory")
def recent_memory(limit: int = 20) -> list[dict]:
    return memory.recent(limit)


@app.get("/knowledge/search")
def search_knowledge(q: str, limit: int = 3) -> list[dict]:
    return knowledge.search(q, limit)
