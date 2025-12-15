from app.infrastructure.in_memory_book_repository import InMemoryBookRepository
from app.application.books_service import BooksService

_repo = InMemoryBookRepository()


def get_books_service():
    return BooksService(_repo)


def reset_repo():
    _repo.clear()