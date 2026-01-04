from app.application.books_service import BooksService
from app.infrastructure.sqlite_book_repository import SQLiteBookRepository
from app.infrastructure.migrations import run_migrations

# -------------------------------------------------------------------
# Database configuration
# -------------------------------------------------------------------

# Tests (shared in-memory SQLite)
DATABASE_URL = "file::memory:?cache=shared"

# Dev / Prod (uncomment when needed)
# DATABASE_URL = "books.db"

# -------------------------------------------------------------------
# Infrastructure wiring
# -------------------------------------------------------------------

_repo = SQLiteBookRepository(DATABASE_URL)

# Ensure schema exists ONCE at startup
run_migrations(DATABASE_URL)


def get_books_service() -> BooksService:
    """
    FastAPI dependency.
    """
    return BooksService(_repo)


# -------------------------------------------------------------------
# Test-only helpers
# -------------------------------------------------------------------

def reset_repo() -> None:
    """
    Used by tests to reset database state.

    IMPORTANT:
    - This is NOT part of the application API
    - It is intentionally placed here for test control
    """
    _repo.reset()