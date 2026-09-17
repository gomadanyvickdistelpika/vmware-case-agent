def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["infrastructure_execution"] is False


def test_analyze_redacts_before_memory(client):
    response = client.post("/analyze", json={"workflow": "logs", "text": "Contact: Jane Doe jane@example.com\nvpxd ERROR timeout", "save_to_memory": True})
    assert response.status_code == 200
    body = response.json()
    assert "jane@example.com" not in body["redacted_input"]
    assert body["memory_id"]
    recent = client.get("/memory").json()
    assert len(recent) == 1


def test_upload_restrictions_and_no_persistence(client):
    response = client.post("/upload", files={"file": ("sample.log", b"hostd failed contact me@example.com", "text/plain")})
    assert response.status_code == 200
    assert response.json()["stored"] is False
    assert "me@example.com" not in response.json()["redacted_text"]
    rejected = client.post("/upload", files={"file": ("bad.pdf", b"x", "application/pdf")})
    assert rejected.status_code == 415


def test_automation_never_executes(client):
    response = client.post("/analyze", json={"workflow": "automation", "text": "vpxd timeout", "save_to_memory": False})
    content = response.json()["content"]
    assert "never executes infrastructure changes" in content
    assert "APPROVAL REQUIRED" in content

