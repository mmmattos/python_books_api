import sqlite3


def run_migrations(db_path: str) -> None:
    """
    Run database migrations.

    This function is intentionally:
    - idempotent (safe to run multiple times)
    - simple (no migration history yet)
    - explicit (called from app startup or tests)

    For now, it only ensures the `books` table exists.
    """
    conn = sqlite3.connect(db_path, uri=True)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()