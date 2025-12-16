from fastapi.testclient import TestClient

from app.main import app
from app.presentation.dependencies import reset_repo

client = TestClient(app)


def setup_function():
    # Ensure in-memory state is clean before every test
    reset_repo()


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

    body = r.json()
    assert body["title"] == "Clean Code"
    assert body["author"] == "Robert C. Martin"


def test_list_books_after_create():
    client.post(
        "/books",
        json={"title": "Clean Code", "author": "Robert C. Martin"},
    )

    r = client.get("/books")
    assert r.status_code == 200

    books = r.json()
    assert len(books) == 1
    assert books[0]["title"] == "Clean Code"

def test_update_book():
    r = client.post("/books", json={"title": "Old", "author": "A"})
    book_id = r.json()["id"]

    r = client.put(
        f"/books/{book_id}",
        json={"title": "New", "author": "B"},
    )
    assert r.status_code == 200
    assert r.json()["title"] == "New"


def test_delete_book():
    r = client.post("/books", json={"title": "Delete Me"})
    book_id = r.json()["id"]

    r = client.delete(f"/books/{book_id}")
    assert r.status_code == 204

    r = client.get("/books")
    assert r.json() == []