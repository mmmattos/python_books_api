from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.book import Book


class BookRepository(ABC):
    """
    Repository interface for Book persistence.

    Application and domain layers depend on this abstraction,
    not on concrete database implementations.
    """

    @abstractmethod
    def create(self, title: str, author: Optional[str]) -> Book:
        """
        Persist a new book and return it.
        """
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    def get(self, book_id: int) -> Optional[Book]:
        """
        Retrieve a book by ID.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        book_id: int,
        title: str,
        author: Optional[str],
    ) -> Optional[Book]:
        """
        Update a book and return it, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, book_id: int) -> bool:
        """
        Delete a book by ID.
        Returns True if deleted, False if not found.
        """
        raise NotImplementedError