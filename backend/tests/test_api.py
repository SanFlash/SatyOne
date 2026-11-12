from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
    response=client.get("/health")
    assert response.status_code==200
    assert response.json()["status"]=="healthy"
def test_commands_seeded():
    response=client.get("/api/v1/commands")
    assert response.status_code==200
    assert len(response.json())>=8
def test_prompt_builder():
    response=client.post("/api/v1/prompt-builder",json={"objective":"Create a test plan for a login page","audience":"QA engineer","tone":"professional","output_format":"numbered plan","constraints":["Include negative cases"],"command_slugs":["testcase"]})
    assert response.status_code==200
    assert "OBJECTIVE" in response.json()["prompt"]
    assert "/TESTCASE" in response.json()["selected_commands"]
