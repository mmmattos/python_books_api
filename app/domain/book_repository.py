from abc import ABC, abstractmethod
from typing import List
from app.domain.book import Book

class BookRepository(ABC):
    @abstractmethod
    def list(self) -> List[Book]:
        pass

    @abstractmethod
    def add(self, title: str, author: str | None) -> Book:
        pass