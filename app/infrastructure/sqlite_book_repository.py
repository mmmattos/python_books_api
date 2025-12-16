import sqlite3
from typing import Optional, List

from app.domain.book import Book
from app.domain.book_repository import BookRepository


class SQLiteBookRepository(BookRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT
                )
                """
            )

    # -------- REQUIRED BY BooksService --------

    def add(self, title: str, author: Optional[str] = None) -> Book:
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO books (title, author) VALUES (?, ?)",
                (title, author),
            )
            book_id = cursor.lastrowid

        return Book(id=book_id, title=title, author=author)

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        title: Optional[str] = None,
    ) -> List[Book]:
        query = "SELECT id, title, author FROM books"
        params = []

        if title:
            query += " WHERE title LIKE ?"
            params.append(f"%{title}%")

        query += " ORDER BY id LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        return [Book(id=row[0], title=row[1], author=row[2]) for row in rows]

    def update(
        self,
        book_id: int,
        title: str,
        author: Optional[str] = None,
    ) -> Book:
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE books SET title = ?, author = ? WHERE id = ?",
                (title, author, book_id),
            )

            if cur.rowcount == 0:
                raise KeyError("Book not found")

        return Book(id=book_id, title=title, author=author)

    def delete(self, book_id: int) -> None:
        with self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,),
            )

            if cur.rowcount == 0:
                raise KeyError("Book not found")