import json
from pathlib import Path
import pytest

from dany_super_agent.analyzer import render
from dany_super_agent.privacy import redact

CASES = json.loads((Path(__file__).parent / "fixtures" / "case_evaluations.json").read_text(encoding="utf-8"))


def test_suite_has_five_approachable_and_five_difficult_cases():
    assert len(CASES) == 10
    assert sum(case["difficulty"] == "approachable" for case in CASES) == 5
    assert sum(case["difficulty"] == "difficult" for case in CASES) == 5


@pytest.mark.parametrize("scenario", CASES, ids=[case["id"] for case in CASES])
def test_case_agent_quality_contract(scenario):
    cleaned = redact(scenario["input"])
    output, findings, confidence, missing = render("case", cleaned.text, scenario["product"], scenario["version"])
    required = [
        "Issue Clarification", "Evidence / Verification", "Ranked hypotheses", "HYPOTHESIS",
        "Safe checks", "READ-ONLY", "Risky checks", "APPROVAL REQUIRED", "Rollback plan",
        "Customer-ready draft", "Internal-note draft", "KB applicability gate", "Quality checklist",
        "Confidence and missing evidence",
    ]
    assert all(label in output for label in required)
    assert findings.evidence and all(item.id.startswith("E") and item.source for item in findings.evidence)
    assert confidence in {"low", "medium", "high"}
    assert missing
    assert "Validate both before applying any KB" in output
    assert "Observed:" in output and "Inferred:" in output and "Unverified:" in output
    assert scenario["infer"] and scenario["request"] and scenario["avoid"]
    assert "test@example.invalid" not in cleaned.text


def test_every_difficult_case_records_public_sources():
    difficult = [case for case in CASES if case["difficulty"] == "difficult"]
    assert all(case.get("sources") for case in difficult)
    assert all(url.startswith("https://") for case in difficult for url in case["sources"])

