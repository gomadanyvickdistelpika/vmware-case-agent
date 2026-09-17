import json
from pathlib import Path
from dany_super_agent.analyzer import render

CASES = json.loads((Path(__file__).parent / "fixtures" / "public_issue_demo.json").read_text(encoding="utf-8"))


def test_public_demo_has_ten_distinct_redacted_cases():
    assert len(CASES) == 10
    assert len({case["title"] for case in CASES}) == 10
    assert all("@" not in case["prompt"] and "password" not in case["prompt"].lower() for case in CASES)


def test_kb_matching_is_conservative_and_expected():
    for case in CASES:
        output, findings, confidence, missing = render("case", case["prompt"], case["product"], case["version"])
        identified = "No specific Broadcom KB was verified" not in output
        assert identified is case["kb_expected"]
        assert findings.evidence and confidence and missing
        assert "APPROVAL REQUIRED" in output and "Rollback plan" in output


def test_generated_report_represents_all_ten_runs():
    report = (Path(__file__).parent.parent / "PUBLIC_ISSUE_DEMO.md").read_text(encoding="utf-8")
    assert sum(line.startswith("## ") and line[3:4].isdigit() for line in report.splitlines()) == 10
    assert report.count("**Synthetic prompt:**") == 10
    assert report.count("### Concise local-agent answer") == 10
    assert report.count("### KB correctness assessment") == 10
    assert report.count("**PASS") == 10
