from fastapi.testclient import TestClient
from backend.main import app
import backend.routes as routes

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "LegalEase API is running"

def test_generate_with_mock(monkeypatch):
    class FakeGenerator:
        def __init__(self, settings): pass
        def generate_document(self, *args): return "1. Purpose\nGenerated draft."
    monkeypatch.setattr(routes, "GeminiDocumentGenerator", FakeGenerator)
    response = client.post("/generate", json={"document_type":"NDA","parties":"A and B","terms":"Confidentiality;Return materials","effective_date":"2026-09-25"})
    assert response.status_code == 200
    assert "Generated draft" in response.json()["content"]
