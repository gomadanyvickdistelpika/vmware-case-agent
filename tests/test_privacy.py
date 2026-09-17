import re

from dany_super_agent.config import settings
from dany_super_agent.privacy import redact


def test_redacts_sensitive_fields():
    source = "Customer: Jane Doe email jane@example.com phone +353 87 123 4567 Case # SR-123456 password: Secret! link https://private.example/a"
    result = redact(source)
    assert "Jane Doe" not in result.text
    assert "jane@example.com" not in result.text
    assert "+353 87 123 4567" not in result.text
    assert "SR-123456" not in result.text
    assert "Secret!" not in result.text
    assert "https://" not in result.text
    assert {"person_name", "email", "phone", "case_id", "attachment_password", "access_link"}.issubset(result.categories)


def test_searchable_knowledge_contains_no_pps_numbers():
    pps_pattern = re.compile(r"\b\d{7}[A-Z]{1,2}\b", re.I)
    for path in settings.knowledge_dir.glob("**/*"):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".csv"}:
            assert not pps_pattern.search(path.read_text(encoding="utf-8")), path
