from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_uses_local_sqlite():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["database"] == "sqlite"

def test_commands_are_seeded():
    response = client.get("/api/v1/commands")
    assert response.status_code == 200
    assert len(response.json()) >= 20\n    slugs = {item["slug"] for item in response.json()}\n    assert {"agent-plan", "research-plan", "privacy-review", "a11y-audit"} <= slugs

def test_prompt_builder_uses_selected_command():
    response = client.post("/api/v1/prompt-builder", json={
        "objective": "Create a test plan for a login page",
        "audience": "QA engineer",
        "tone": "professional",
        "output_format": "numbered plan",
        "constraints": ["Include negative cases"],
        "command_slugs": ["testcase"],
    })
    assert response.status_code == 200
    assert "OBJECTIVE" in response.json()["prompt"]
    assert "/TESTCASE" in response.json()["selected_commands"]\n    prompt = response.json()["prompt"]\n    assert "SAFETY, PRIVACY AND AUTHORIZATION" in prompt\n    assert "Do not fabricate citations" in prompt

def test_saved_prompt_round_trip():
    created = client.post("/api/v1/saved-prompts", json={
        "title": "Local persistence test",
        "prompt": "A saved prompt survives API requests.",
        "owner_key": "pytest-local",
    })
    assert created.status_code == 200
    prompt_id = created.json()["id"]
    listed = client.get("/api/v1/saved-prompts?owner_key=pytest-local")
    assert listed.status_code == 200
    assert any(item["id"] == prompt_id for item in listed.json())
    deleted = client.delete(f"/api/v1/saved-prompts/{prompt_id}?owner_key=pytest-local")
    assert deleted.status_code == 200
    assert deleted.json()["deleted"] is True

def test_command_difficulty_filter():
    response = client.get("/api/v1/commands?difficulty=advanced")
    assert response.status_code == 200
    assert response.json()
    assert all(item["difficulty"] == "advanced" for item in response.json())
