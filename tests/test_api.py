from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_db_test():
    response = client.get("/test_db")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Database Session Created"
    }


def test_resume_upload():
    with open("tests/test_files/test_resume.pdf", "rb") as file:
        response = client.post(
            "/resume",
            files={
                "file": (
                    "test_resume.pdf",
                    file,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test_resume.pdf"
    assert data["total_chunks"] > 0
    assert data["embedding_count"] == data["total_chunks"]
    assert data["embedding_dimensions"] == 384


def test_job_description():
    with open("tests/test_files/test_resume.pdf", "rb") as file:
        resume_response = client.post(
            "/resume",
            files={
                "file": (
                    "test_resume.pdf",
                    file,
                    "application/pdf"
                )
            }
        )

    assert resume_response.status_code == 200

    resume_data = resume_response.json()

    resume_id = resume_data["resume.id"]

    response = client.post(
        "/job-description",
        json={
            "text": "Looking for a Python developer with FastAPI and PostgreSQL experience.",
            "resume_id": resume_id
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_description" in data