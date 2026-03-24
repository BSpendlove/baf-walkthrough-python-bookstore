# Implementation Spec: Bookstore REST API

## Overview

Build a REST API for managing a bookstore catalog using FastAPI, SQLite, and Pydantic. The API provides CRUD operations for books, search by title/author, and ISBN-13 validation. This unblocks the frontend team by providing the backend they need to build the catalog UI.

## Source Issue

[Issue #1 — Add Bookstore REST API with CRUD, search, and ISBN validation](../../.github/../../../issues/1)

## Current State

Greenfield project — no application code, dependencies, or database exists yet. The repository contains only the baf workflow scaffolding (`context/`, `.claude/`, `.github/`).

## Design

### Architecture

```
FastAPI application (single module)
├── app/
│   ├── main.py          # FastAPI app, lifespan, router mounting
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── database.py       # SQLite engine, session management
│   ├── routes/
│   │   └── books.py      # Book CRUD + search endpoints
│   └── isbn.py           # ISBN-13 validation logic
└── tests/
    ├── conftest.py        # Fixtures (test client, test DB)
    ├── test_books.py      # CRUD endpoint tests
    ├── test_search.py     # Search endpoint tests
    └── test_isbn.py       # ISBN validation unit tests
```

### Data Model

**Book** table:
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| title | TEXT | NOT NULL |
| author | TEXT | NOT NULL |
| isbn | TEXT | NOT NULL, UNIQUE |
| price | REAL | NOT NULL, > 0 |
| published_year | INTEGER | nullable |
| description | TEXT | nullable |
| created_at | DATETIME | NOT NULL, default=now |
| updated_at | DATETIME | NOT NULL, default=now, onupdate=now |

### API Endpoints

| Method | Path | Description | Status Codes |
|--------|------|-------------|--------------|
| POST | `/books` | Create a book | 201, 422 |
| GET | `/books` | List books (paginated) | 200 |
| GET | `/books/{id}` | Get a single book | 200, 404 |
| PUT | `/books/{id}` | Update a book | 200, 404, 422 |
| DELETE | `/books/{id}` | Delete a book | 204, 404 |
| GET | `/books/search?q=` | Search by title/author | 200 |

### Pagination

`GET /books` accepts `skip` (default 0) and `limit` (default 20, max 100) query parameters. Response includes the list of books directly (no envelope).

### ISBN-13 Validation

ISBN-13 is validated on `POST /books` and `PUT /books/{id}`:

1. Strip hyphens and spaces
2. Must be exactly 13 digits
3. Check digit must be valid per ISBN-13 algorithm (alternating weights of 1 and 3, mod 10)
4. Invalid ISBN returns 422 with a descriptive error message

### Search

`GET /books/search?q=<query>` performs case-insensitive `LIKE` search across `title` and `author` columns. Returns paginated results using the same `skip`/`limit` parameters.

### Error Handling

- 404: `{"detail": "Book not found"}`
- 422: FastAPI's default validation error format (includes field-level errors for Pydantic failures; custom message for ISBN validation)
- Duplicate ISBN on create/update: 409 `{"detail": "A book with this ISBN already exists"}`

## Configuration

No environment variables needed. SQLite database file defaults to `bookstore.db` in the project root. Tests use an in-memory SQLite database.

## File Plan

| File | Action | Purpose |
|------|--------|---------|
| `pyproject.toml` | Create | Project metadata, dependencies (fastapi, uvicorn, sqlalchemy, pydantic, pytest, httpx) |
| `app/__init__.py` | Create | Package init |
| `app/database.py` | Create | SQLAlchemy engine, `SessionLocal`, `Base`, `get_db` dependency |
| `app/models.py` | Create | `Book` SQLAlchemy model |
| `app/schemas.py` | Create | `BookCreate`, `BookUpdate`, `BookResponse` Pydantic schemas |
| `app/isbn.py` | Create | `validate_isbn13(isbn: str) -> str` — returns normalized ISBN or raises `ValueError` |
| `app/routes/__init__.py` | Create | Package init |
| `app/routes/books.py` | Create | All book endpoints (CRUD + search) |
| `app/main.py` | Create | FastAPI app creation, lifespan (create tables), include router |
| `tests/__init__.py` | Create | Package init |
| `tests/conftest.py` | Create | Test client fixture with in-memory SQLite |
| `tests/test_isbn.py` | Create | Unit tests for ISBN-13 validation |
| `tests/test_books.py` | Create | CRUD endpoint integration tests |
| `tests/test_search.py` | Create | Search endpoint tests |
| `.gitignore` | Create | Python gitignore (venv, __pycache__, *.db, .env) |

## Implementation Order

1. **Project setup** — Create `pyproject.toml` and `.gitignore`
2. **Database layer** — `app/database.py` with engine, session, Base
3. **Models** — `app/models.py` with Book model
4. **Schemas** — `app/schemas.py` with Pydantic models
5. **ISBN validation** — `app/isbn.py` with validation function + `tests/test_isbn.py`
6. **Book routes** — `app/routes/books.py` with all endpoints
7. **App entry point** — `app/main.py` with lifespan and router
8. **Test fixtures** — `tests/conftest.py`
9. **CRUD tests** — `tests/test_books.py`
10. **Search tests** — `tests/test_search.py`

Each step is independently verifiable: steps 1-4 can be validated by import, step 5 by running ISBN unit tests, steps 6-10 by running the full test suite.

## Testing

- **Framework:** pytest with httpx `AsyncClient` (or `TestClient` from fastapi.testclient for sync tests)
- **Database:** In-memory SQLite per test session, tables created/dropped via fixtures
- **ISBN tests:** Valid ISBNs, invalid check digits, wrong length, non-numeric, hyphens/spaces normalization
- **CRUD tests:** Create, read, list (pagination), update, delete, 404 on missing, duplicate ISBN 409
- **Search tests:** Match by title, match by author, case insensitivity, no results, partial match
- Run: `pytest` from project root

## Not In Scope

- Authentication and user accounts
- Frontend/UI
- Deployment configuration
- Book cover images
- Author as a separate entity (author is a string field on Book)
