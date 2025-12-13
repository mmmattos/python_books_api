from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_list_books_empty():
    r = client.get("/books")
    assert r.status_code == 200
    assert r.json() == []

def test_create_book():
    payload = {"title": "Clean Code", "author": "Robert C. Martin"}
    r = client.post("/books", json=payload)
    assert r.status_code == 201
    assert r.json()["title"] == "Clean Code"

def test_list_books_after_create():
    r = client.get("/books")
    assert r.status_code == 200
    assert len(r.json()) == 1