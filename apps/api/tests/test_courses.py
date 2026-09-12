from fastapi.testclient import TestClient


def test_list_courses(client: TestClient) -> None:
    response = client.get("/courses")
    assert response.status_code == 200
    slugs = [c["slug"] for c in response.json()]
    assert "build" in slugs


def test_get_build_course_has_five_sprints(client: TestClient) -> None:
    response = client.get("/courses/build")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "BUILD"
    assert len(body["sprints"]) == 5
    assert sum(len(s["missions"]) for s in body["sprints"]) == 25


def test_get_mission_three_matches_authored_spec(client: TestClient) -> None:
    response = client.get("/courses/build/missions/3")
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Fix your first bug: the /health check lies"
    assert body["mission_type"] == "debugging"
    assert body["acceptance_criteria"] is not None
    assert "GET /health returns HTTP 200" in body["acceptance_criteria"]


def test_get_unknown_course_404s(client: TestClient) -> None:
    response = client.get("/courses/does-not-exist")
    assert response.status_code == 404
