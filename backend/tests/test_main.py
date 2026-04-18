import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.auth import get_password_hash
from app.models import User

# --- Setup Test Database ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tasks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- The Tests ---

def test_register_user():
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_user():
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_task():
    # 1. Get the token
    login_res = client.post("/auth/login", data={"username": "testuser", "password": "testpassword"})
    token = login_res.json()["access_token"]

    # 2. Use the token to create a task
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Task", "description": "This is a test"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"