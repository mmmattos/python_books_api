from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.book import Book


class BookRepository(ABC):
    @abstractmethod
    def list(self) -> List[Book]:
        ...

    @abstractmethod
    def add(self, title: str, author: str | None) -> Book:
        ...

    @abstractmethod
    def update(self, book_id: int, title: str, author: str | None) -> Optional[Book]:
        ...

    @abstractmethod
    def delete(self, book_id: int) -> bool:
        ...