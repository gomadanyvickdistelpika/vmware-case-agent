from typing import Literal
from pydantic import BaseModel, Field

Workflow = Literal[
    "case", "logs", "email", "automation", "business", "learning",
    "career", "documents", "tech_devices", "media", "portfolio", "pc_navigation",
]


class AnalyzeRequest(BaseModel):
    workflow: Workflow = "case"
    text: str = Field(min_length=1, max_length=500_000)
    product: str | None = None
    version: str | None = None
    save_to_memory: bool = False
    external_action_approved: bool = False


class EvidenceItem(BaseModel):
    id: str
    source: str
    observation: str
    line: int | None = None


class AnalysisResponse(BaseModel):
    workflow: Workflow
    redacted_input: str
    redactions: list[str]
    content: str
    evidence: list[EvidenceItem]
    confidence: Literal["low", "medium", "high"]
    missing_evidence: list[str]
    memory_id: int | None = None
