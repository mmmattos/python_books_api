from typing import Optional, List

from app.domain.book import Book
from app.domain.book_repository import BookRepository


class BooksService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        title: Optional[str] = None,
    ) -> List[Book]:
        return self.repo.list(
            limit=limit,
            offset=offset,
            title=title,
        )

    def create(self, title: str, author: Optional[str] = None) -> Book:
        return self.repo.add(title=title, author=author)

    def update(
        self,
        book_id: int,
        title: str,
        author: Optional[str] = None,
    ) -> Book:
        return self.repo.update(
            book_id=book_id,
            title=title,
            author=author,
        )

    def delete(self, book_id: int) -> None:
        self.repo.delete(book_id)