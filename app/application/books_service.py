class BooksService:
    def __init__(self, repo):
        self.repo = repo

    def list(self):
        return self.repo.list()

    def create(self, title: str, author: str):
        book = {"title": title, "author": author}
        self.repo.add(book)   # SINGLE add
        return book