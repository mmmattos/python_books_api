import sqlite3
from typing import List, Optional

from app.domain.book import Book


class SQLiteBookRepository:
    """
    SQLite implementation of BookRepository.

    Notes:
    - Keeps a single connection alive (required for in-memory DBs).
    - Repository provides DEFAULTS.
    - Validation belongs to API / service layer.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn = sqlite3.connect(
            db_path,
            uri=True,
            check_same_thread=False,
        )
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT
            )
            """
        )
        self._conn.commit()

    # -----------------------------
    # Test support
    # -----------------------------
    def reset(self) -> None:
        self._conn.execute("DELETE FROM books")
        self._conn.commit()

    # -----------------------------
    # CRUD operations
    # -----------------------------
    def create(self, title: str, author: Optional[str]) -> Book:
        cur = self._conn.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            (title, author),
        )
        self._conn.commit()

        return Book(id=cur.lastrowid, title=title, author=author)

    def get(self, book_id: int) -> Optional[Book]:
        row = self._conn.execute(
            "SELECT id, title, author FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()

        if row is None:
            return None

        return Book(id=row[0], title=row[1], author=row[2])

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        title: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> List[Book]:
        allowed_sort_fields = {"id", "title", "author"}

        field = sort or "id"
        direction = "ASC"

        if field.startswith("-"):
            direction = "DESC"
            field = field[1:]

        if field not in allowed_sort_fields:
            field = "id"

        sql = "SELECT id, title, author FROM books"
        params: list = []

        if title:
            sql += " WHERE title LIKE ?"
            params.append(f"%{title}%")

        sql += f" ORDER BY {field} {direction} LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self._conn.execute(sql, params).fetchall()

        return [Book(id=r[0], title=r[1], author=r[2]) for r in rows]

    def update(self, book_id: int, title: str, author: Optional[str]) -> Optional[Book]:
        cur = self._conn.execute(
            "UPDATE books SET title = ?, author = ? WHERE id = ?",
            (title, author, book_id),
        )
        self._conn.commit()

        if cur.rowcount == 0:
            return None

        return Book(id=book_id, title=title, author=author)

    def delete(self, book_id: int) -> bool:
        cur = self._conn.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,),
        )
        self._conn.commit()

        return cur.rowcount > 0