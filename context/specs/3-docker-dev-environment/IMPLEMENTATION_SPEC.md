# Implementation Spec: Docker Development Environment

## Overview

Add Docker containerization and docker-compose orchestration for the bookstore API development workflow. The setup uses Caddy as a reverse proxy with automatic internal TLS, mounts the application code as a volume for hot-reload via watchdog/uvicorn `--reload`, and includes a developer guide for getting started.

## Source Issue

[#3 — Dockerfile and docker compose support for development environment](https://github.com/BSpendlove/baf-walkthrough-python-bookstore/issues/3)

## Current State

- FastAPI application running on uvicorn (port 8000)
- SQLite database at `bookstore.db` (relative path, created at working directory)
- Dependencies managed via `pyproject.toml` (pip-installable)
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
```

### Key Decisions

1. **Caddy for TLS** — Caddy automatically generates and manages internal (self-signed) TLS certificates. No manual cert generation needed. The `tls internal` directive handles this.

2. **Volume mount for hot-reload** — The `app/` directory is bind-mounted into the container so code changes on the host are immediately visible. Uvicorn's `--reload` flag watches for file changes and restarts the server automatically. No watchdog package needed — uvicorn's built-in file watcher (using `watchfiles` from `uvicorn[standard]`) handles this.

3. **SQLite volume** — The database file is stored in a named volume so data persists across container restarts but doesn't pollute the host project directory.

4. **Single Dockerfile** — One Dockerfile targeting development use. Production optimization (multi-stage builds, etc.) is out of scope.

5. **Caddy domain** — Use `bookstore.localhost` as the development domain. Most browsers resolve `*.localhost` to `127.0.0.1` without `/etc/hosts` changes.

### Container Configuration

- **App container:** Python 3.12-slim base, installs dependencies from `pyproject.toml`, runs uvicorn with `--reload` and `--host 0.0.0.0`
- **Caddy container:** Official `caddy:2-alpine` image, reverse proxies HTTPS :443 → app:8000

## Configuration

### Environment Variables

None required. The app currently has no environment-variable-based configuration. The SQLite path is hardcoded in `app/database.py`.

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

No existing files need modification.

## Implementation Order

### Step 1: Create `.dockerignore`

Exclude `.venv/`, `*.db`, `.git/`, `__pycache__/`, `.pytest_cache/`, `context/`, `.github/` from the Docker build context.

**Verify:** File exists and lists appropriate exclusions.

### Step 2: Create `Dockerfile`

- Base image: `python:3.12-slim`
- Set working directory to `/app`
- Copy `pyproject.toml` first (layer caching for dependencies)
- Install dependencies with `pip install .`
- Copy application code
- Expose port 8000
- CMD: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

**Verify:** `docker build -t bookstore-api .` succeeds.

### Step 3: Create `Caddyfile`

Configure `bookstore.localhost` with `reverse_proxy app:8000` and `tls internal`.

**Verify:** File is valid Caddy configuration syntax.

### Step 4: Create `docker-compose.yml`

Two services:
- **app**: builds from `Dockerfile`, mounts `./app:/app/app` for hot-reload, exposes port 8000 (optional, for direct API access), depends on nothing
- **caddy**: uses `caddy:2-alpine`, mounts `Caddyfile`, publishes ports 443 and 80, depends on `app`, uses named volumes for Caddy data/config

Volumes: `caddy_data`, `caddy_config`

**Verify:** `docker compose config` validates without errors.

### Step 5: Create `docs/docker-dev-guide.md`

Write a concise developer guide covering:
- Prerequisites (Docker, docker compose plugin)
- Starting the environment (`docker compose up`)
- Accessing the API (`https://bookstore.localhost`)
- How hot-reload works
- Trusting the Caddy internal CA (optional, for browsers)
- Running tests inside the container
- Stopping and cleaning up

**Verify:** Guide is accurate and follows the actual setup.

## Testing

- `docker compose up --build` starts both containers without errors
- `https://bookstore.localhost/docs` loads the FastAPI Swagger UI (after accepting self-signed cert)
- Modify a file in `app/` on the host → uvicorn auto-reloads inside the container
- API endpoints respond correctly through Caddy (e.g., `curl -k https://bookstore.localhost/books`)
- `docker compose down` stops cleanly

All testing is manual — no new automated tests are needed for containerization.

## Not In Scope

- Docker installation instructions (issue explicitly excludes this)
- Production-ready Dockerfile (multi-stage builds, non-root user, etc.)
- Dev containers / VS Code devcontainer configuration (noted as future work in the issue)
- CI/CD pipeline changes
- Environment variable configuration system
- Database migration tooling
