from app.application.books_service import BooksService
from app.infrastructure.sqlite_book_repository import SQLiteBookRepository

# Single shared repository instance
_repo = SQLiteBookRepository(db_path="books.db")


def get_books_service() -> BooksService:
    return BooksService(_repo)


def reset_repo() -> None:
    """
    Used by tests to reset database state.
    """
    # Brutally simple for now: delete all rows
    with _repo._connect() as conn:
        conn.execute("DELETE FROM books")