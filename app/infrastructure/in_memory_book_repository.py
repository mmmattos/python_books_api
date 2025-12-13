from typing import List
from app.domain.book import Book
from app.domain.book_repository import BookRepository

class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self._books: List[Book] = []
        self._next_id = 1

    def list(self) -> List[Book]:
        return self._books

    def add(self, title: str, author: str | None) -> Book:
        book = Book(
            id=self._next_id,
            title=title,
            author=author,
        )
        self._next_id += 1
        self._books.append(book)
        return book