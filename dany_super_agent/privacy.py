"""Deterministic redaction before persistence or knowledge indexing."""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RedactionResult:
    text: str
    categories: tuple[str, ...]


RULES: tuple[tuple[str, re.Pattern[str], str], ...] = (
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I), "[REDACTED_EMAIL]"),
    ("phone", re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{7,}\d)(?!\w)"), "[REDACTED_PHONE]"),
    ("access_link", re.compile(r"https?://[^\s<>]+", re.I), "[REDACTED_LINK]"),
    ("case_id", re.compile(r"\b(?:case|sr|ticket)\s*(?:id|#|number|no\.?|:)??\s*[-:]?\s*[A-Z0-9][A-Z0-9-]{5,}\b", re.I), "[REDACTED_CASE_ID]"),
    ("attachment_password", re.compile(r"(?im)\b(?:attachment|archive|zip|file)?\s*(?:password|passcode|pwd)\s*[:=]\s*\S+"), "attachment password: [REDACTED_SECRET]"),
    ("person_name", re.compile(r"(?im)\b(?:customer|contact|name)\s*[:=]\s*[A-Z][A-Za-z'\-]+(?:\s+[A-Z][A-Za-z'\-]+){1,3}"), "name: [REDACTED_NAME]"),
)


def redact(text: str) -> RedactionResult:
    cleaned = text.replace("\x00", "")
    found: list[str] = []
    for category, pattern, replacement in RULES:
        cleaned, count = pattern.subn(replacement, cleaned)
        if count:
            found.append(category)
    return RedactionResult(cleaned, tuple(found))

