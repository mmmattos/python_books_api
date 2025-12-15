from app.domain.book import Book
from app.presentation.schemas import BookOut

class BooksService:
    def __init__(self, repo):
        self.repo = repo

    def list(self) -> list[BookOut]:
        return [
            BookOut(title=b.title, author=b.author)
            for b in self.repo.list()
        ]

    def create(self, title, author):
        book = self.repo.add(title, author)
        return BookOut(id=book.id, title=book.title, author=book.author)