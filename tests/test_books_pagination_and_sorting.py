from fastapi.testclient import TestClient

from app.main import app
from app.presentation.dependencies import reset_repo

client = TestClient(app)


def setup_function():
    # Ensure clean DB state before every test
    reset_repo()


def _seed_books():
    """
    Insert a deterministic set of books for pagination & sorting tests.
    IDs are auto-incremented, titles chosen to sort clearly.
    """
    books = [
        {"title": "Clean Code", "author": "Robert C. Martin"},
        {"title": "Domain-Driven Design", "author": "Eric Evans"},
        {"title": "Refactoring", "author": "Martin Fowler"},
        {"title": "The Pragmatic Programmer", "author": "Andy Hunt"},
    ]

    for b in books:
        client.post("/books", json=b)


# ------------------------
# Pagination contract
# ------------------------

def test_list_books_default_pagination():
    _seed_books()

    r = client.get("/books")
    assert r.status_code == 200

    data = r.json()
    assert len(data) == 4  # default limit is >= dataset size


def test_list_books_limit_and_offset():
    _seed_books()

    r = client.get("/books?limit=2&offset=1")
    assert r.status_code == 200

    data = r.json()
    assert len(data) == 2

    # Should skip the first inserted book
    assert data[0]["title"] == "Domain-Driven Design"


def test_list_books_offset_beyond_range():
    _seed_books()

    r = client.get("/books?limit=10&offset=100")
    assert r.status_code == 200
    assert r.json() == []


# ------------------------
# Sorting contract
# ------------------------

def test_sort_by_title_ascending():
    _seed_books()

    r = client.get("/books?sort=title")
    assert r.status_code == 200

    titles = [b["title"] for b in r.json()]
    assert titles == sorted(titles)


def test_sort_by_title_descending():
    _seed_books()

    r = client.get("/books?sort=-title")
    assert r.status_code == 200

    titles = [b["title"] for b in r.json()]
    assert titles == sorted(titles, reverse=True)


def test_sort_by_invalid_field_falls_back_to_id():
    _seed_books()

    r = client.get("/books?sort=does_not_exist")
    assert r.status_code == 200

    ids = [b["id"] for b in r.json()]
    assert ids == sorted(ids)


def test_sort_with_no_parameter_defaults_to_id():
    _seed_books()

    r = client.get("/books")
    assert r.status_code == 200

    ids = [b["id"] for b in r.json()]
    assert ids == sorted(ids)