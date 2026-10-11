"""
Integration & Unit Test Suite for AI Productivity Suite Backend.

Tests database persistence, repository queries, AI NLU inference, and FastAPI HTTP endpoints.
"""

from datetime import datetime, date, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.services.ai.resume_nlu import ResumeNLUService
from app.services.ai.task_nlu import TaskNLUService
from main import app

# In-memory SQLite for isolated, fast test execution
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database schema for each test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Override get_db dependency with isolated in-memory test session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ============================================================================
# Unit Tests: AI Inference Engines
# ============================================================================

def test_resume_nlu_extraction():
    """Verify ResumeNLUService accurately extracts skills, metrics, and computes scores."""
    service = ResumeNLUService()
    sample_resume = """
    Alex Mercer
    Senior Software Engineer specializing in backend systems.
    
    Experience:
    - Architected high-throughput microservices using Python, FastAPI, and PostgreSQL.
    - Improved API response latency by 45% under 150ms for 10M+ daily active users.
    - Led a team of 8 engineers and migrated deployment pipeline to Docker and Kubernetes on AWS.
    - Reduced cloud infrastructure expenditures by $250K annually.
    """

    result = service.parse(sample_resume)

    assert result["candidate_name"] == "Alex Mercer"
    assert "backend systems" in result["summary"]

    categories = {cat["category"]: cat["skills"] for cat in result["skills"]}
    assert "Python" in categories.get("Languages", [])
    assert "FastAPI" in categories.get("Frameworks & Libraries", [])
    assert "PostgreSQL" in categories.get("Databases & Storage", [])
    assert "AWS" in categories.get("Cloud & Infrastructure", [])

    # Check metrics
    extracted_quant_values = [m["quantified_value"] for m in result["metrics"]]
    assert any("45%" in q for q in extracted_quant_values)
    assert any("$250" in q for q in extracted_quant_values)
    assert result["overall_score"] >= 70.0


def test_task_nlu_parsing():
    """Verify TaskNLUService parses natural language times, priorities, and tasks."""
    service = TaskNLUService()
    ref_dt = datetime(2026, 10, 12, 10, 0, 0, tzinfo=timezone.utc)  # Monday
    prompt = "Schedule an urgent mock interview tomorrow at 5 PM for 90 mins"

    result = service.parse(prompt, reference_datetime=ref_dt)

    assert result.intent == "SCHEDULE_INTERVIEW"
    assert "Mock interview" in result.extracted_title
    assert result.priority.value == "URGENT"
    assert result.duration_minutes == 90
    assert result.target_start_time.date() == date(2026, 10, 13)
    assert result.target_start_time.hour == 17
    assert result.target_start_time.minute == 0
    assert result.target_end_time.hour == 18
    assert result.target_end_time.minute == 30


# ============================================================================
# Integration Tests: Endpoints & Persistence Flow
# ============================================================================

def test_root_and_health(client):
    """Verify root and health endpoints."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "documentation" in resp.json()

    resp_health = client.get("/api/v1/health")
    assert resp_health.status_code == 200
    assert resp_health.json()["status"] == "healthy"


def test_user_lifecycle(client):
    """Verify creating and fetching users."""
    user_payload = {"email": "engineer@enterprise.ai", "full_name": "Ada Lovelace"}
    create_resp = client.post("/api/v1/users/", json=user_payload)
    assert create_resp.status_code == 201
    created_user = create_resp.json()
    assert created_user["email"] == "engineer@enterprise.ai"
    user_id = created_user["id"]

    # Conflict on duplicate email
    dup_resp = client.post("/api/v1/users/", json=user_payload)
    assert dup_resp.status_code == 409

    # Retrieve user
    get_resp = client.get(f"/api/v1/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["full_name"] == "Ada Lovelace"


def test_resume_analysis_endpoint(client):
    """Verify POST /api/v1/analyze-resume persists and extracts correctly."""
    # 1. Create a user first
    user_resp = client.post(
        "/api/v1/users/",
        json={"email": "candidate@faang.com", "full_name": "Alan Turing"},
    )
    user_id = user_resp.json()["id"]

    # 2. Analyze Resume
    resume_payload = {
        "user_id": user_id,
        "resume_text": """
        Alan Turing
        Principal Systems Architect.
        Developed high-performance distributed systems in Go, Python, and SQL.
        Reduced processing latency by 60% and scaled data pipeline to 50k QPS.
        Managed team of 12 engineers, saving $1.2M annually in compute costs.
        """,
    }

    resp = client.post("/api/v1/analyze-resume", json=resume_payload)
    assert resp.status_code == 201
    data = resp.json()

    assert data["user_id"] == user_id
    assert data["candidate_name"] == "Alan Turing"
    assert len(data["skills"]) > 0
    assert len(data["metrics"]) >= 2
    assert data["overall_score"] > 50.0

    # 3. Retrieve historical resumes
    hist_resp = client.get(f"/api/v1/resumes/user/{user_id}")
    assert hist_resp.status_code == 200
    assert len(hist_resp.json()) == 1


def test_smart_task_and_daily_itinerary(client):
    """Verify POST /api/v1/smart-tasks and subsequent GET itinerary endpoint."""
    # 1. Create User
    user_resp = client.post(
        "/api/v1/users/",
        json={"email": "scheduler@test.com", "full_name": "Grace Hopper"},
    )
    user_id = user_resp.json()["id"]

    # 2. Submit Natural Language Task
    ref_time = datetime(2026, 10, 15, 8, 0, 0, tzinfo=timezone.utc).isoformat()
    task_payload = {
        "user_id": user_id,
        "natural_language_input": "Schedule a critical system design review tomorrow at 3 PM for 2 hours",
        "reference_datetime": ref_time,
    }

    post_resp = client.post("/api/v1/smart-tasks", json=task_payload)
    assert post_resp.status_code == 201
    data = post_resp.json()

    assert "System design review" in data["task"]["title"]
    assert data["task"]["priority"] == "URGENT"
    assert data["schedule"]["task_id"] == data["task"]["id"]
    assert "2026-10-16" in data["schedule"]["scheduled_date"]

    # 3. Query Daily Itinerary for target date
    itinerary_resp = client.get(
        f"/api/v1/schedules/daily/{user_id}?date=2026-10-16"
    )
    assert itinerary_resp.status_code == 200
    itinerary = itinerary_resp.json()

    assert itinerary["user_id"] == user_id
    assert itinerary["scheduled_date"] == "2026-10-16"
    assert itinerary["total_blocks"] == 1
    assert len(itinerary["itinerary"]) == 1
    assert itinerary["itinerary"][0]["time_block_title"] == data["task"]["title"]


def test_not_found_handling(client):
    """Ensure graceful 404 responses for invalid user foreign keys."""
    resp = client.post(
        "/api/v1/analyze-resume",
        json={"user_id": 99999, "resume_text": "Sample valid resume text with enough characters for test."},
    )
    assert resp.status_code == 404
    assert "does not exist" in resp.json()["detail"]


def test_scheduling_conflict_handling(client):
    """Ensure conflict detection throws 409 when allow_overlap is set to False."""
    user_resp = client.post(
        "/api/v1/users/",
        json={"email": "conflict_test@test.com", "full_name": "Conflict User"},
    )
    user_id = user_resp.json()["id"]
    ref_time = datetime(2026, 10, 20, 9, 0, 0, tzinfo=timezone.utc).isoformat()

    # Book slot 1
    resp1 = client.post(
        "/api/v1/smart-tasks?allow_overlap=false",
        json={
            "user_id": user_id,
            "natural_language_input": "Schedule team sprint sync today at 2 PM for 1 hour",
            "reference_datetime": ref_time,
        },
    )
    assert resp1.status_code == 201

    # Book conflicting slot with allow_overlap=false
    resp2 = client.post(
        "/api/v1/smart-tasks?allow_overlap=false",
        json={
            "user_id": user_id,
            "natural_language_input": "Schedule 1:1 meeting today at 2 PM for 30 minutes",
            "reference_datetime": ref_time,
        },
    )
    assert resp2.status_code == 409
    assert "Scheduling conflict detected" in resp2.json()["detail"]


def test_user_task_listing(client):
    """Verify GET /api/v1/tasks/user/{user_id} lists extracted tasks."""
    user_resp = client.post(
        "/api/v1/users/",
        json={"email": "tasklist@test.com", "full_name": "Task Lister"},
    )
    user_id = user_resp.json()["id"]

    client.post(
        "/api/v1/smart-tasks",
        json={
            "user_id": user_id,
            "natural_language_input": "Schedule a quick code review tomorrow at 11 AM",
        },
    )

    resp = client.get(f"/api/v1/tasks/user/{user_id}")
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) == 1
    assert "code review" in tasks[0]["title"].lower()


def test_input_validation(client):
    """Ensure FastAPI rejects invalid payloads with 422 Unprocessable Entity."""
    # Short resume text < 20 chars
    resp = client.post(
        "/api/v1/analyze-resume",
        json={"user_id": 1, "resume_text": "too short"},
    )
    assert resp.status_code == 422

