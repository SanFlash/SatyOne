from uuid import uuid4

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
    assert len(response.json()) >= 20
    slugs = {item["slug"] for item in response.json()}
    assert {"agent-plan", "research-plan", "privacy-review", "a11y-audit"} <= slugs


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
    assert "/TESTCASE" in response.json()["selected_commands"]
    prompt = response.json()["prompt"]
    assert "SAFETY, PRIVACY AND AUTHORIZATION" in prompt
    assert "Do not fabricate citations" in prompt


def test_saved_prompt_round_trip():
    owner = f"pytest-{uuid4()}"
    created = client.post("/api/v1/saved-prompts", json={
        "title": "Local persistence test",
        "prompt": "A saved prompt survives API requests.",
        "owner_key": owner,
    })
    assert created.status_code == 200
    prompt_id = created.json()["id"]
    listed = client.get(f"/api/v1/saved-prompts?owner_key={owner}")
    assert listed.status_code == 200
    assert any(item["id"] == prompt_id for item in listed.json())
    deleted = client.delete(f"/api/v1/saved-prompts/{prompt_id}?owner_key={owner}")
    assert deleted.status_code == 200
    assert deleted.json()["deleted"] is True


def test_saved_prompt_search_edit_and_version_history():
    owner = f"pytest-{uuid4()}"
    created = client.post("/api/v1/saved-prompts", json={
        "title": "Regression checklist",
        "prompt": "Check login and logout flows.",
        "owner_key": owner,
    })
    assert created.status_code == 200
    prompt_id = created.json()["id"]

    search = client.get(f"/api/v1/saved-prompts?owner_key={owner}&q=Regression")
    assert search.status_code == 200
    assert len(search.json()) == 1

    updated = client.put(f"/api/v1/saved-prompts/{prompt_id}", json={
        "title": "Updated regression checklist",
        "prompt": "Check login, logout, session expiry and error handling.",
        "owner_key": owner,
    })
    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated regression checklist"

    history = client.get(f"/api/v1/saved-prompts/{prompt_id}/versions?owner_key={owner}")
    assert history.status_code == 200
    assert len(history.json()) == 1
    assert history.json()[0]["title"] == "Regression checklist"
    assert history.json()[0]["prompt"] == "Check login and logout flows."

    client.delete(f"/api/v1/saved-prompts/{prompt_id}?owner_key={owner}")


def test_command_difficulty_filter():
    response = client.get("/api/v1/commands?difficulty=advanced")
    assert response.status_code == 200
    assert response.json()
    assert all(item["difficulty"] == "advanced" for item in response.json())
