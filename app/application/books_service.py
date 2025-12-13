from typing import List
from app.domain.book import Book
from app.domain.book_repository import BookRepository

class BooksService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def list_books(self) -> List[Book]:
        return self.repo.list()

    def create_book(self, title: str, author: str | None) -> Book:
        return self.repo.add(title, author)