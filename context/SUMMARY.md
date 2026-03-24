# Project Summary

This file tracks project state. Every agent session should read this before starting new work.

**Updated after every spec is implemented.**

## Current State

Bookstore API — core REST API implemented with CRUD, search, and ISBN-13 validation. Docker development environment with Caddy TLS reverse proxy.

## Completed Specs

| Spec | Issue | Status | Summary |
|------|-------|--------|---------|
| `1-bookstore-rest-api` | #1 | Implemented | FastAPI REST API with Book CRUD, search by title/author, ISBN-13 validation, SQLite storage |
| `3-docker-dev-environment` | #3 | Implemented | Dockerfile, docker-compose with Caddy TLS, hot-reload via bind mount, SQLite persistence via named volume |

## Key Decisions

- **Framework:** FastAPI + SQLAlchemy + SQLite + Pydantic
- **Author model:** String field on Book, not a separate entity
- **ISBN storage:** Normalized (digits only) for UNIQUE constraint consistency
- **Search:** `.ilike()` for case-insensitive matching (FTS5 for future scale)
- **Pagination:** `skip`/`limit` query params, no response envelope
- **Database URL:** Configurable via `DATABASE_URL` env var, defaults to `sqlite:///bookstore.db`
- **Dev domain:** `bookstore.localhost` with Caddy internal TLS
