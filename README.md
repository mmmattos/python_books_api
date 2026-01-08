
# 📚 Books API — Clean & Hexagonal Architecture (Python + FastAPI)

This repository contains a **production-ready REST API** for managing books, built with **FastAPI**, **SQLite**, and a **strict architectural discipline**.

The goal of this project is **not** just CRUD — it is to demonstrate how to structure Python APIs using:

- ✅ **Clean Architecture**
- ✅ **Hexagonal (Ports & Adapters) Architecture**
- ✅ Testability-first design
- ✅ SQLite safety (including in-memory testing)
- ✅ Clear separation of responsibilities

---

## 🧱 High-Level Architecture

This project follows **both**:

- **Clean Architecture (Uncle Bob)**
- **Hexagonal Architecture (Ports & Adapters)**

They are complementary — not competing.

---

## 🧠 Architectural View — Clean Architecture

Clean Architecture organizes code by **policy vs details**, from the center outward:

```
┌───────────────────────────────┐
│         Presentation          │  ← FastAPI routes, schemas, HTTP
│   (controllers / delivery)    │
└──────────────▲────────────────┘
               │
┌──────────────┴────────────────┐
│          Application           │  ← Use cases / services
│        (business rules)        │
└──────────────▲────────────────┘
               │
┌──────────────┴────────────────┐
│             Domain             │  ← Entities & repository contracts
│        (core business)         │
└──────────────▲────────────────┘
               │
┌──────────────┴────────────────┐
│        Infrastructure          │  ← SQLite, migrations, adapters
│     (frameworks & drivers)     │
└───────────────────────────────┘
```

### Key rules (strictly enforced):

- **Domain depends on nothing**
- **Application depends only on Domain**
- **Infrastructure depends inward**
- **Presentation depends inward**
- Dependencies always point **toward the center**

---

## 🔌 Architectural View — Hexagonal Architecture

Hexagonal Architecture focuses on **how the system interacts with the outside world**.

```
            ┌───────────────┐
            │   FastAPI     │
            │  (HTTP API)   │
            └──────▲────────┘
                   │
        ┌──────────┴──────────┐
        │    Application      │
        │   (BooksService)    │
        └──────▲────────▲─────┘
               │        │
      ┌────────┘        └────────┐
      │                          | 
┌─────┴─────-┐              ┌────┴───────┐
│ Repository │              │   Tests    │
│  Adapter   │              │ (pytest)   │
│ (SQLite)   │              │            │
└────────────┘              └────────────┘
```

### Hexagonal mapping

| Concept | In this project |
|----------------------|-------------------------------------|
| **Port**             | `BookRepository` (domain interface) |
| **Adapter**          | `SQLiteBookRepository`              |
| **Driving adapter**  | FastAPI routes                      |
| **Driven adapter**   | SQLite                              |
| **Application core** | `BooksService`                      |

The core **does not know**:
- SQLite
- FastAPI
- pytest
- HTTP
- SQL

And it never should.

---

## 📂 Folder Structure

```
app/
├── main.py                     # FastAPI app entrypoint
│
├── domain/                     # Core business (NO frameworks)
│   ├── book.py
│   └── book_repository.py
│
├── application/                # Use cases
│   └── books_service.py
│
├── infrastructure/             # Adapters & persistence
│   ├── sqlite_book_repository.py
│   ├── in_memory_book_repository.py
│   └── migrations.py
│
├── presentation/               # HTTP layer
│   ├── books_api.py
│   ├── schemas.py
│   └── dependencies.py
│
├── config.py                   # Environment configuration
└── __init__.py
```

---

## 🧪 Testing Strategy

### Types of tests included

| Layer | Tested? | How |
|-----|--------|----|
| Domain | ✅ | Pure unit tests |
| Application | ✅ | Service tests |
| Repository | ✅ | SQLite in-memory tests |
| API | ✅ | FastAPI TestClient |

### SQLite in-memory safety

- Uses **one persistent connection**
- Uses `file::memory:?cache=shared`
- Schema initialized explicitly
- No flaky tests

---

## 🗄 Migrations Strategy

- Migrations are handled via `infrastructure/migrations.py`
- Repository **does not** create schema implicitly
- Migrations are executed at application startup (via dependencies)

This keeps:
- Tests deterministic
- Production predictable
- Schema evolution explicit

---

## ▶️ Running the API

```bash
uvicorn app.main:app --reload
```

Health check:

```bash
GET /health
```

---

## ▶️ Running tests

```bash
python -m pytest -q
```

Expected:

```
27 passed in <1s
```

---

## 🚀 Why this structure matters

This architecture allows you to:

- Swap SQLite → Postgres without touching business logic
- Add a CLI or gRPC interface without changing services
- Test everything without mocks
- Scale the codebase safely

This is **not tutorial code** — this is **real-world architecture**.

---

## 📌 Next steps (optional)

- Production DB (Postgres)
- Alembic-style migrations
- Pagination metadata (HATEOAS)
- Auth / RBAC
- Async repository adapter

---

## ✅ Status

- ✔ Clean Architecture compliant
- ✔ Hexagonal Architecture compliant
- ✔ Testable
- ✔ Maintainable
- ✔ Production-ready foundation
