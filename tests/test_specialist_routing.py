import pytest
from dany_super_agent.analyzer import render


@pytest.mark.parametrize("workflow", ["business", "learning", "career", "documents", "tech_devices", "media", "portfolio"])
def test_general_specialists_do_not_take_external_actions(workflow):
    output, *_ = render(workflow, "Synthetic planning request", None, None)
    assert "requires explicit human review and approval" in output
    assert "No such action was executed" in output


@pytest.mark.parametrize(
    ("workflow", "heading"),
    [
        ("career", "Career & Job Application Agent"),
        ("documents", "Documents & Forms Agent"),
        ("tech_devices", "Consumer Tech & Device Troubleshooting Agent"),
        ("media", "Media & Creative Task Agent"),
        ("portfolio", "Project Portfolio Agent"),
    ],
)
def test_export_informed_specialists_route_to_expected_agent(workflow, heading):
    output, *_ = render(workflow, "Synthetic request", None, None)
    assert heading in output
    assert "say when freshness was not checked" in output


def test_pc_navigation_is_blocked_without_approval_and_still_nonexecuting_with_it():
    blocked, *_ = render("pc_navigation", "Open settings", None, None, False)
    approved, *_ = render("pc_navigation", "Open settings", None, None, True)
    assert "BLOCKED" in blocked
    assert "execution remains disabled" in approved
    assert "every click" in approved
