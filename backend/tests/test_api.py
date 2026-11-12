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
    response = client.get("/api/v1/commands?limit=1000")
    assert response.status_code == 200
    assert len(response.json()) >= 1100
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
    assert "OBJECTIVE AND SUCCESS DEFINITION" in response.json()["prompt"]
    assert "/TESTCASE" in response.json()["selected_commands"]
    prompt = response.json()["prompt"]
    assert "RISK, SECURITY, PRIVACY AND COMPLIANCE" in prompt
    assert "Never invent sources, facts, execution results" in prompt


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


def test_unknown_ai_provider_is_rejected():
    response = client.post("/api/v1/execute/unknown", json={"prompt": "Say hello"})
    assert response.status_code == 404


def test_ai_status_does_not_expose_secrets():
    response = client.get("/api/v1/ai/status")
    assert response.status_code == 200
    body = response.json()
    assert {item["id"] for item in body["providers"]} == {"ollama", "openai"}
    assert all("api_key" not in item and "secret" not in item for item in body["providers"])


def test_expanded_command_catalogue_exceeds_600_and_is_unique():
    response = client.get("/api/v1/commands?limit=1000")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 1100
    assert len({item["slug"] for item in items}) == len(items)
    assert len({item["syntax"] for item in items}) == len(items)
    assert any(item["category"]["slug"] == "finance-accounting" for item in items)
    assert any(item["category"]["slug"] == "healthcare-admin" for item in items)


def test_prompt_builder_produces_detailed_structured_brief():
    response = client.post("/api/v1/prompt-builder", json={
        "objective": "Create a launch readiness plan for a new customer portal",
        "audience": "Product and engineering leadership",
        "tone": "clear and decisive",
        "output_format": "implementation brief with tables",
        "constraints": ["Include rollback criteria"],
        "command_slugs": ["business-strategy-roadmap"],
    })
    assert response.status_code == 200
    prompt = response.json()["prompt"]
    for heading in ["EXPERT ROLE", "OBJECTIVE AND SUCCESS", "CONTEXT AND INPUT", "SCOPE, NON-GOALS", "DETAILED EXECUTION PLAN", "REQUIRED DELIVERABLE", "CASE MATRIX", "QUALITY ASSURANCE", "FAILURE HANDLING", "FINAL QUALITY GATE"]:
        assert heading in prompt
    assert "Include rollback criteria" in prompt


def test_qa_and_qa_automation_command_packs_are_available():
    response = client.get("/api/v1/commands?limit=1000")
    assert response.status_code == 200
    items = response.json()
    qa = [item for item in items if item["category"]["slug"] == "qa"]
    automation = [item for item in items if item["category"]["slug"] == "qa-automation"]
    assert len(qa) >= 40
    assert len(automation) >= 40
    slugs = {item["slug"] for item in items}
    assert "qa-specialist-requirements-analysis" in slugs
    assert "qa-automation-specialist-playwright-framework" in slugs
    assert "qa-automation-specialist-appium-ios" in slugs
    assert all(len(item["instruction_template"]) > 400 for item in qa + automation)


def test_advanced_commands_expand_all_domains():
    response = client.get("/api/v1/commands?limit=2000")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 1200
    advanced = [item for item in items if "-advanced-" in item["slug"]]
    assert len(advanced) >= 380
    assert len({item["slug"] for item in advanced}) == len(advanced)
    assert all(item["difficulty"] == "advanced" for item in advanced)


def test_prompt_builder_includes_context_specific_edge_cases():
    response = client.post("/api/v1/prompt-builder", json={
        "objective": "Build a Playwright automation framework for a customer portal",
        "audience": "QA automation engineer",
        "tone": "technical and precise",
        "output_format": "implementation plan and code examples",
        "constraints": ["Use Python and Pytest"],
        "command_slugs": ["qa-automation-specialist-playwright-framework"],
    })
    assert response.status_code == 200
    prompt = response.json()["prompt"]
    for term in ["flaky-test triage", "session expiry", "test isolation", "rollback", "acceptance criteria", "Use Python and Pytest"]:
        assert term.lower() in prompt.lower()
