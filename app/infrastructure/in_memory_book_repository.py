class InMemoryBookRepository:
    def __init__(self):
        self._books = []

    def list(self):
        return self._books

    def add(self, book):
        self._books.append(book)

    def clear(self):
        self._books.clear()