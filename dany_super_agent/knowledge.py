from __future__ import annotations

from pathlib import Path


class KnowledgeBase:
    def __init__(self, directory: Path):
        self.directory = directory

    def documents(self) -> list[tuple[str, str]]:
        result = []
        for path in sorted(self.directory.glob("**/*")):
            if path.is_file() and path.suffix.lower() in {".md", ".txt", ".csv"}:
                result.append((str(path.relative_to(self.directory)), path.read_text(encoding="utf-8")))
        return result

    def search(self, query: str, limit: int = 3) -> list[dict]:
        terms = {term.lower() for term in query.split() if len(term) > 3}
        scored = []
        for source, text in self.documents():
            score = sum(text.lower().count(term) for term in terms)
            if score:
                scored.append({"source": source, "score": score, "excerpt": text[:500]})
        return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]

