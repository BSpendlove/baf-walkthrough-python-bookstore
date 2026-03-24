# Decisions: 3-docker-dev-environment

## Accepted

### Dockerfile build failure: package discovery
- **Source:** Gemini, Codex
- **Severity:** CRITICAL
- **Resolution:** Added `[build-system]` and `[tool.setuptools.packages.find]` to `pyproject.toml` in the file plan and implementation order. Scopes package discovery to `app` only, preventing `pip install .` from failing on multiple top-level directories.

### Broken layer caching strategy
- **Source:** Gemini, Codex
- **Severity:** CRITICAL
- **Resolution:** Changed Dockerfile strategy to copy both `pyproject.toml` and `app/` before running `pip install ".[dev]"`. Acknowledged that `pip install .` requires source code present. The bind mount in docker-compose.yml overlays the baked-in code at runtime for hot-reload.

### SQLite persistence requires app code change
- **Source:** Gemini, Codex
- **Severity:** CRITICAL (Gemini: HIGH)
- **Resolution:** Added `app/database.py` to the file plan. Updated to read `DATABASE_URL` from environment with fallback to current default. Container uses `DATABASE_URL=sqlite:////data/bookstore.db` with a named volume at `/data`.

### Hot-reload underspecified for Docker Desktop
- **Source:** Codex (Gemini: MEDIUM)
- **Severity:** HIGH
- **Resolution:** Added `WATCHFILES_FORCE_POLLING=true` as a default environment variable in the app service in docker-compose.yml. Documented in dev guide.

### Test dependencies not installed in image
- **Source:** Codex
- **Severity:** HIGH
- **Resolution:** Changed Dockerfile to install `.[dev]` instead of `.`, so pytest and httpx are available. Added `docker compose exec app pytest` to dev guide and testing section.

### `bookstore.localhost` DNS resolution not universal
- **Source:** Gemini
- **Severity:** MEDIUM
- **Resolution:** Added troubleshooting note to dev guide covering `/etc/hosts` fallback for environments where `*.localhost` doesn't resolve.

### Testing section doesn't verify data persistence
- **Source:** Codex
- **Severity:** MEDIUM
- **Resolution:** Added persistence verification step to testing section: create data, `docker compose down && docker compose up`, verify data persists.

### `.dockerignore` too narrow
- **Source:** Codex
- **Severity:** LOW
- **Resolution:** Changed `.venv/` exclusion to `*venv*/` pattern to cover non-dot virtualenv directories like `test_venv/`.

## Rejected

### Pin specific Python base image patch version
- **Source:** Gemini
- **Severity:** LOW
- **Rationale:** This is a development environment, not a production image. Pinning to `python:3.12-slim` is sufficient — patch-level pinning adds maintenance overhead without meaningful benefit for dev containers.
