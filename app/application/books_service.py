from typing import Optional, List
from app.domain.book import Book
from app.domain.book_repository import BookRepository


class BooksService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def create(self, title: str, author: Optional[str]) -> Book:
        return self.repo.create(title=title, author=author)

    def list(
        self,
        limit: int,
        offset: int,
        title: Optional[str],
        sort: Optional[str],
    ) -> List[Book]:
        return self.repo.list(
            limit=limit,
            offset=offset,
            title=title,
            sort=sort,
        )

    def update(
        self,
        book_id: int,
        title: str,
        author: Optional[str],
    ) -> Optional[Book]:
        # IMPORTANT: return the repository result
        return self.repo.update(
            book_id=book_id,
            title=title,
            author=author,
        )

    def delete(self, book_id: int) -> bool:
        return self.repo.delete(book_id)