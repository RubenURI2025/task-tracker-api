def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "Task Tracker API is running"


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Learn Docker"})
    assert response.status_code == 201
    assert response.json["title"] == "Learn Docker"
    assert response.json["completed"] is False


def test_create_task_missing_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert "error" in response.json


def test_list_tasks(client):
    client.post("/tasks", json={"title": "First task"})
    client.post("/tasks", json={"title": "Second task"})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json) == 2


def test_complete_task(client):
    create_response = client.post("/tasks", json={"title": "Finish me"})
    task_id = create_response.json["id"]

    response = client.patch(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json["completed"] is True
