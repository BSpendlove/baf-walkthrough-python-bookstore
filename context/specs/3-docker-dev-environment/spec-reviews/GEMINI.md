# Spec Review: Docker Development Environment (Issue #3)

**Agent:** Gemini
**Status:** COMPLETE
**Review Date:** 2026-03-24

## Summary

The specification provides a solid foundation for a Docker-based development environment using a modern stack (Caddy + FastAPI + uvicorn). The decision to use `bookstore.localhost` for automatic DNS resolution and Caddy's `tls internal` for automatic TLS management is excellent for developer experience.

However, there are critical technical blockers in the proposed `Dockerfile` build process and the implementation of data persistence that must be addressed before implementation begins.

---

## Findings

### CRITICAL

#### 1. Dockerfile Build Failure: Package Discovery
- **Severity:** CRITICAL
- **Description:** The proposed `pip install .` command will fail because the project structure cannot be automatically discovered by the default `setuptools` backend. Running `pip install .` on the current codebase results in an error: `Multiple top-level packages discovered in a flat-layout: ['app', 'context', 'tests']`. This is because `pyproject.toml` lacks a `[build-system]` section and explicit `[tool.setuptools]` package configuration.
- **Suggested Resolution:** Modify `pyproject.toml` to include a `[build-system]` section and specify that only the `app` directory should be treated as a package, OR use a different method to install dependencies (e.g., a temporary `requirements.txt` or a tool like `uv`).

#### 2. Broken Layer Caching Strategy
- **Severity:** CRITICAL
- **Description:** Step 2 of the Implementation Order proposes copying `pyproject.toml` and then running `pip install .` to cache dependencies. However, `pip install .` (even with the `--no-deps` flag) requires the package source code to be present to build the project. Since only `pyproject.toml` is copied before the install command, the build will fail at this step.
- **Suggested Resolution:** If the goal is layer caching, use a tool that can install dependencies without building the project (like `pip install -r requirements.txt`), or copy the `app/` directory *before* the `pip install .` command (acknowledging that this reduces cache efficiency if source code changes).

### HIGH

#### 1. Missing SQLite Data Persistence
- **Severity:** HIGH
- **Description:** Decision 3 states that "data persists across container restarts but doesn't pollute the host project directory" using a named volume. However, the Implementation Plan (Step 4) only lists a bind-mount for the source code and named volumes for Caddy. It does not provide a volume for the `bookstore.db` file. Since the database is created at `/app/bookstore.db` (in the container's root working directory), it will be lost whenever the container is removed (e.g., during `docker compose down` or image updates).
- **Suggested Resolution:** Mount a named volume to a directory (e.g., `/data`) and modify `app/database.py` to use a path in that directory (e.g., `sqlite:////data/bookstore.db`), preferably via an environment variable. If modifying `app/database.py` is forbidden, a bind-mount for the specific file may be required, but this "pollutes" the host as per the spec's own definition.

### MEDIUM

#### 1. Resolution of `bookstore.localhost`
- **Severity:** MEDIUM
- **Description:** While most modern browsers resolve `*.localhost` to `127.0.0.1`, this is not universal across all operating systems, DNS configurations, or CLI tools (like `curl`). Users on older systems or specific network setups may find the environment unreachable.
- **Suggested Resolution:** Add a note to the Developer Guide instructions for Step 5 recommending the addition of `127.0.0.1 bookstore.localhost` to the host's `/etc/hosts` file as a troubleshooting step.

#### 2. Uvicorn Reload in Docker
- **Severity:** MEDIUM
- **Description:** Uvicorn's `--reload` (using `watchfiles`) occasionally fails to detect changes on some host/container combinations (especially on macOS/Windows with certain file system drivers) unless polling is enabled.
- **Suggested Resolution:** Mention `WATCHFILES_FORCE_POLLING=true` as an optional environment variable in the Developer Guide if hot-reload is not working for the user.

### LOW

#### 1. Production vs. Development Dockerfile
- **Severity:** LOW
- **Description:** The spec explicitly excludes production optimizations. However, using `python:3.12-slim` is a good choice. For consistency, explicitly using `python:3.12.2-slim` (or a specific patch version) would ensure more reproducible builds.
- **Suggested Resolution:** Use a more specific base image tag.

---

## Conclusion

The spec's architectural direction is sound, but the `Dockerfile` and `pyproject.toml` interplay is technically flawed in its current form and will prevent a successful build. Additionally, the data persistence goal requires either a modification to the application's database configuration or a compromise on host "pollution" (via bind-mounting the DB file).
