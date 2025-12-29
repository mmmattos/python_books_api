import pytest

from app.infrastructure.sqlite_book_repository import SQLiteBookRepository
from app.domain.book import Book


@pytest.fixture()
def repo():
    """
    Use an in-memory SQLite database.

    IMPORTANT:
    - `cache=shared` ensures schema persists across connections.
    """
    repo = SQLiteBookRepository("file::memory:?cache=shared")
    repo.reset()
    return repo


# ------------------------
# Create
# ------------------------

def test_create_book(repo):
    book = repo.create("Clean Code", "Robert C. Martin")

    assert isinstance(book, Book)
    assert book.id is not None
    assert book.title == "Clean Code"
    assert book.author == "Robert C. Martin"


# ------------------------
# Get
# ------------------------

def test_get_existing_book(repo):
    created = repo.create("DDD", "Eric Evans")

    fetched = repo.get(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.title == "DDD"


def test_get_non_existing_book(repo):
    assert repo.get(9999) is None


# ------------------------
# List
# ------------------------

def test_list_books_empty(repo):
    books = repo.list()
    assert books == []


def test_list_books_with_data(repo):
    repo.create("A", "a")
    repo.create("B", "b")

    books = repo.list()
    assert len(books) == 2


def test_list_with_limit_and_offset(repo):
    repo.create("A", "a")
    repo.create("B", "b")
    repo.create("C", "c")

    books = repo.list(limit=1, offset=1)
    assert len(books) == 1
    assert books[0].title == "B"


# ------------------------
# Sorting
# ------------------------

def test_sort_by_title_asc(repo):
    repo.create("C", "c")
    repo.create("A", "a")
    repo.create("B", "b")

    books = repo.list(sort="title")
    titles = [b.title for b in books]

    assert titles == ["A", "B", "C"]


def test_sort_by_title_desc(repo):
    repo.create("C", "c")
    repo.create("A", "a")
    repo.create("B", "b")

    books = repo.list(sort="-title")
    titles = [b.title for b in books]

    assert titles == ["C", "B", "A"]


def test_sort_invalid_field_falls_back_to_id(repo):
    repo.create("X", "x")
    repo.create("Y", "y")

    books = repo.list(sort="does_not_exist")
    ids = [b.id for b in books]

    assert ids == sorted(ids)


# ------------------------
# Update
# ------------------------

def test_update_existing_book(repo):
    book = repo.create("Old", "A")

    updated = repo.update(book.id, "New", "B")

    assert updated is not None
    assert updated.id == book.id
    assert updated.title == "New"
    assert updated.author == "B"


def test_update_non_existing_book(repo):
    result = repo.update(9999, "X", "Y")
    assert result is None


# ------------------------
# Delete
# ------------------------

def test_delete_existing_book(repo):
    book = repo.create("Delete Me", None)

    ok = repo.delete(book.id)
    assert ok is True

    assert repo.get(book.id) is None


def test_delete_non_existing_book(repo):
    ok = repo.delete(9999)
    assert ok is False


# ------------------------
# Reset
# ------------------------

def test_reset_clears_all_data(repo):
    repo.create("A", None)
    repo.create("B", None)

    repo.reset()

    assert repo.list() == []