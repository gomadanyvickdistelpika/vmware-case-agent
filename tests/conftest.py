from pathlib import Path
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from dany_super_agent import api
    from dany_super_agent.memory import MemoryStore
    monkeypatch.setattr(api, "memory", MemoryStore(tmp_path / "test.db"))
    with TestClient(api.app) as test_client:
        yield test_client

