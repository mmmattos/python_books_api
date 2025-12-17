from typing import List, Optional

from app.domain.book import Book
from app.domain.book_repository import BookRepository


class BooksService:
    """
    Application service for Books.

    Orchestrates use cases and delegates persistence
    to the repository interface.
    """

    def __init__(self, repo: BookRepository):
        self.repo = repo

    def create(self, title: str, author: Optional[str] = None) -> Book:
        """
        Create a new book.
        """
        return self.repo.create(title=title, author=author)

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        title: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> List[Book]:
        """
        List books with pagination, optional filtering, and sorting.
        """
        return self.repo.list(
            limit=limit,
            offset=offset,
            title=title,
            sort=sort,
        )

    def get(self, book_id: int) -> Optional[Book]:
        """
        Get a single book by ID.
        """
        return self.repo.get(book_id)

    def update(
        self,
        book_id: int,
        title: str,
        author: Optional[str] = None,
    ) -> Optional[Book]:
        """
        Update an existing book.
        """
        return self.repo.update(
            book_id=book_id,
            title=title,
            author=author,
        )

    def delete(self, book_id: int) -> bool:
        """
        Delete a book by ID.
        """
        return self.repo.delete(book_id)