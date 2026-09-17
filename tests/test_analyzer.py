from dany_super_agent.analyzer import inspect, render


def test_recognizes_vmware_components_and_labels_hypotheses():
    text = "2026-01-01 vpxd ERROR timeout contacting vmdird\nvmkernel storage warning"
    content, findings, confidence, missing = render("case", text, "vCenter", "8.0")
    assert {"vpxd", "vmdird", "vmkernel"}.issubset(findings.components)
    assert "HYPOTHESIS" in content
    assert "APPROVAL REQUIRED" in content
    assert "Rollback plan" in content
    assert confidence == "medium"
    assert missing


def test_all_required_log_families_recognized():
    text = " ".join(["vpxd", "hostd", "vmkernel", "vobd", "vmafdd", "vmdird", "applmgmt", "SSO", "lookup service", "vLCM", "EAM", "WCP", "VAPI"])
    findings = inspect(text)
    assert len(findings.components) == 13

