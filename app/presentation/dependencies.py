from app.application.books_service import BooksService
from app.infrastructure.sqlite_book_repository import SQLiteBookRepository

# Single, shared database for the app & tests
# Use file-based DB to avoid SQLite in-memory connection issues
_DB_PATH = "file:books.db?mode=rwc"

_repo = SQLiteBookRepository(db_path=_DB_PATH)


def get_books_service() -> BooksService:
    return BooksService(_repo)


def reset_repo() -> None:
    """
    Used by tests to reset database state.
    """
    _repo.reset()