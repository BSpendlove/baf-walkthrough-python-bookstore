# Implementation Spec: Docker Development Environment

## Overview

Add Docker containerization and docker-compose orchestration for the bookstore API development workflow. The setup uses Caddy as a reverse proxy with automatic internal TLS, mounts the application code as a volume for hot-reload via uvicorn `--reload`, and includes a developer guide for getting started.

## Source Issue

[#3 — Dockerfile and docker compose support for development environment](https://github.com/BSpendlove/baf-walkthrough-python-bookstore/issues/3)

## Current State

- FastAPI application running on uvicorn (port 8000)
- SQLite database at `bookstore.db` (relative path, created at working directory)
- Dependencies managed via `pyproject.toml` (pip-installable, but missing `[build-system]` and package scoping)
- No containerization, no reverse proxy, no TLS
- Python >=3.11 required

## Design

### Architecture

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Browser    │──TLS──│    Caddy      │──HTTP──│   App (API)  │
│              │ :443  │  (reverse     │ :8000  │  (uvicorn    │
│              │       │   proxy)      │        │   --reload)  │
└──────────────┘       └──────────────┘       └──────────────┘
                        internal TLS            volume mount:
                        auto-certs              ./app → /app/app
                                                /data → named volume
```

### Key Decisions

1. **Caddy for TLS** — Caddy automatically generates and manages internal (self-signed) TLS certificates. No manual cert generation needed. The `tls internal` directive handles this.

2. **Volume mount for hot-reload** — The `app/` directory is bind-mounted into the container so code changes on the host are immediately visible. Uvicorn's `--reload` flag watches for file changes and restarts the server automatically. No watchdog package needed — uvicorn's built-in file watcher (using `watchfiles` from `uvicorn[standard]`) handles this. `WATCHFILES_FORCE_POLLING=true` is set in docker-compose.yml to ensure reliable change detection on macOS/Windows Docker Desktop where native filesystem events may not propagate through bind mounts.

3. **SQLite persistence via environment variable** — `app/database.py` is updated to read `DATABASE_URL` from the environment with a fallback to the current default (`sqlite:///bookstore.db`). In docker-compose.yml, the app service sets `DATABASE_URL=sqlite:////data/bookstore.db` and mounts a named volume at `/data`. This persists data across container restarts without polluting the host project directory.

4. **Single Dockerfile with dev dependencies** — One Dockerfile targeting development use. Installs `.[dev]` (includes pytest and httpx) so tests can run inside the container. Production optimization (multi-stage builds, etc.) is out of scope.

5. **Caddy domain** — Use `bookstore.localhost` as the development domain. Most browsers resolve `*.localhost` to `127.0.0.1` without `/etc/hosts` changes. The dev guide includes a troubleshooting note for environments where this doesn't work.

6. **pyproject.toml build configuration** — Add `[build-system]` section and `[tool.setuptools.packages.find]` to scope package discovery to `app` only, preventing `pip install .` from failing due to multiple top-level directories (`app/`, `context/`, `tests/`).

### Container Configuration

- **App container:** Python 3.12-slim base, installs dependencies from `pyproject.toml` (including dev extras), runs uvicorn with `--reload` and `--host 0.0.0.0`, `WATCHFILES_FORCE_POLLING=true` for reliable hot-reload
- **Caddy container:** Official `caddy:2-alpine` image, reverse proxies HTTPS :443 → app:8000

## Configuration

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `sqlite:///bookstore.db` | SQLAlchemy database connection string. Overridden in docker-compose.yml to `sqlite:////data/bookstore.db` for volume-backed persistence. |
| `WATCHFILES_FORCE_POLLING` | (unset) | Set to `true` in docker-compose.yml to ensure file change detection works through bind mounts on Docker Desktop. |

### Caddyfile

```
bookstore.localhost {
    reverse_proxy app:8000
    tls internal
}
```

## File Plan

| File | Action | Purpose |
|------|--------|---------|
| `Dockerfile` | Create | Python container for the bookstore API |
| `docker-compose.yml` | Create | Orchestrate app + Caddy services |
| `Caddyfile` | Create | Caddy reverse proxy configuration |
| `.dockerignore` | Create | Exclude unnecessary files from build context |
| `docs/docker-dev-guide.md` | Create | Developer guide for Docker-based workflow |
| `app/database.py` | Modify | Read `DATABASE_URL` from environment with fallback to current default |
| `pyproject.toml` | Modify | Add `[build-system]` and `[tool.setuptools.packages.find]` sections |

## Implementation Order

### Step 1: Update `pyproject.toml`

Add `[build-system]` section specifying `setuptools` as the build backend. Add `[tool.setuptools.packages.find]` to include only the `app` package, preventing discovery of `context/` and `tests/` as top-level packages.

```toml
[build-system]
requires = ["setuptools>=75.0.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.setuptools.packages.find]
include = ["app*"]
```

**Verify:** `pip install .` succeeds in a clean virtual environment.

### Step 2: Update `app/database.py`

Read `DATABASE_URL` from `os.environ` with a fallback to the current hardcoded value:

```python
import os
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///bookstore.db")
```

This is a minimal change — existing behavior is preserved when the variable is not set.

**Verify:** App still starts normally without the env var set. Tests still pass.

### Step 3: Create `.dockerignore`

Exclude `.venv/`, `*venv*/`, `*.db`, `.git/`, `__pycache__/`, `.pytest_cache/`, `context/`, `.github/` from the Docker build context.

**Verify:** File exists and lists appropriate exclusions.

### Step 4: Create `Dockerfile`

- Base image: `python:3.12-slim`
- Set working directory to `/app`
- Copy `pyproject.toml` and `app/` directory
- Install with `pip install ".[dev]"` (includes test dependencies)
- Create `/data` directory for SQLite volume mount
- Expose port 8000
- CMD: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

Note: Both `pyproject.toml` and `app/` must be copied before `pip install` because `pip install .` builds the project from source. Layer caching still helps — these layers only rebuild when dependencies or app code change. The bind mount in docker-compose.yml overlays the baked-in `app/` at runtime for hot-reload.

**Verify:** `docker build -t bookstore-api .` succeeds.

### Step 5: Create `Caddyfile`

Configure `bookstore.localhost` with `reverse_proxy app:8000` and `tls internal`.

**Verify:** File is valid Caddy configuration syntax.

### Step 6: Create `docker-compose.yml`

Two services:
- **app**: builds from `Dockerfile`, mounts `./app:/app/app` for hot-reload, mounts named volume `bookstore_data` at `/data` for SQLite persistence, sets `DATABASE_URL=sqlite:////data/bookstore.db` and `WATCHFILES_FORCE_POLLING=true`, exposes port 8000 (optional, for direct API access)
- **caddy**: uses `caddy:2-alpine`, mounts `Caddyfile`, publishes ports 443 and 80, depends on `app`, uses named volumes for Caddy data/config

Volumes: `caddy_data`, `caddy_config`, `bookstore_data`

**Verify:** `docker compose config` validates without errors.

### Step 7: Create `docs/docker-dev-guide.md`

Write a concise developer guide covering:
- Prerequisites (Docker, docker compose plugin)
- Starting the environment (`docker compose up`)
- Accessing the API (`https://bookstore.localhost`)
- How hot-reload works
- Troubleshooting: `*.localhost` DNS resolution (add `/etc/hosts` entry if needed)
- Troubleshooting: hot-reload not working (`WATCHFILES_FORCE_POLLING` is already set, but document it)
- Running tests inside the container (`docker compose exec app pytest`)
- Stopping and cleaning up

**Verify:** Guide is accurate and follows the actual setup.

## Testing

- `docker compose up --build` starts both containers without errors
- `https://bookstore.localhost/docs` loads the FastAPI Swagger UI (after accepting self-signed cert)
- Modify a file in `app/` on the host → uvicorn auto-reloads inside the container
- API endpoints respond correctly through Caddy (e.g., `curl -k https://bookstore.localhost/books`)
- **Data persistence:** Create a book via the API, run `docker compose down && docker compose up`, verify the book still exists
- `docker compose exec app pytest` runs tests successfully inside the container
- `docker compose down` stops cleanly

All testing is manual — no new automated tests are needed for containerization.

## Not In Scope

- Docker installation instructions (issue explicitly excludes this)
- Production-ready Dockerfile (multi-stage builds, non-root user, etc.)
- Dev containers / VS Code devcontainer configuration (noted as future work in the issue)
- CI/CD pipeline changes
- Database migration tooling
