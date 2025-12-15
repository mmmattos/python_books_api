from app.domain.book import Book

class InMemoryBookRepository:
    def __init__(self):
        self._books: list[Book] = []
        self._next_id = 1

    def add(self, title: str, author: str | None):
        book = Book(
            id=self._next_id,
            title=title,
            author=author,
        )
        self._next_id += 1
        self._books.append(book)
        return book

    def list(self):
        return self._books

    def clear(self):
        self._books.clear()
        self._next_id = 1