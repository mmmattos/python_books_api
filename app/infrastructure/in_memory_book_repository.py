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

    def get(self, book_id: int) -> Book | None:
        for book in self._books:
            if book.id == book_id:
                return book
        return None

    def update(self, book_id: int, title: str, author: str | None):
        book = self.get(book_id)
        if not book:
            return None
        book.title = title
        book.author = author
        return book

    def delete(self, book_id: int) -> bool:
        book = self.get(book_id)
        if not book:
            return False
        self._books.remove(book)
        return True

    def clear(self):
        self._books.clear()
        self._next_id = 1