import sqlite3
from typing import List, Optional

from app.domain.book import Book


class SQLiteBookRepository:
    """
    SQLite implementation of the Book repository.

    Notes:
    - Uses a new connection per operation.
    - Schema is ensured on EVERY connection to avoid
      'no such table' issues with SQLite in-memory DBs.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        """
        Create a connection and ensure schema exists.

        This is critical for SQLite in-memory databases,
        where schema may not persist across connections.
        """
        conn = sqlite3.connect(self.db_path, uri=True)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT
            )
            """
        )
        return conn

    def reset(self) -> None:
        """
        Used by tests to reset database state.
        """
        with self._connect() as conn:
            conn.execute("DELETE FROM books")

    def create(self, title: str, author: Optional[str]) -> Book:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO books (title, author) VALUES (?, ?)",
                (title, author),
            )
            book_id = cur.lastrowid

        return Book(id=book_id, title=title, author=author)

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        title: Optional[str] = None,
        sort: str = "id",
    ) -> List[Book]:
        allowed_sort_fields = {"id", "title", "author"}

        direction = "ASC"
        field = sort or "id"

        if field.startswith("-"):
            direction = "DESC"
            field = field[1:]

        if field not in allowed_sort_fields:
            field = "id"

        query = "SELECT id, title, author FROM books"
        params: list = []

        if title:
            query += " WHERE title LIKE ?"
            params.append(f"%{title}%")

        query += f" ORDER BY {field} {direction} LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        return [Book(id=r[0], title=r[1], author=r[2]) for r in rows]

    def get(self, book_id: int) -> Optional[Book]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, title, author FROM books WHERE id = ?",
                (book_id,),
            ).fetchone()

        if not row:
            return None

        return Book(id=row[0], title=row[1], author=row[2])

    def update(self, book_id: int, title: str, author: Optional[str]) -> Optional[Book]:
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE books SET title = ?, author = ? WHERE id = ?",
                (title, author, book_id),
            )

        if cur.rowcount == 0:
            return None

        return Book(id=book_id, title=title, author=author)

    def delete(self, book_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,),
            )

        return cur.rowcount > 0