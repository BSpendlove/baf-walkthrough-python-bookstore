# Spec Critique: 3-docker-dev-environment

**Agent:** Codex
**Date:** 2026-03-24

## Summary
The spec is directionally sound, but it currently has several concrete implementation gaps against this repository. As written, the Docker build order will fail, the SQLite persistence plan cannot work without changing application configuration, and the container setup does not account for the common bind-mount reload failure mode on Docker Desktop. There is also a mismatch between the guide's promised "run tests inside the container" workflow and the dependencies installed into the app image.

## Findings

### Dependency install order in the Dockerfile will fail
- **Severity:** CRITICAL
- **Description:** Step 2 says to copy only `pyproject.toml`, run `pip install .`, and copy the application code afterward. In this repository, `pip install .` installs the local project package, which requires the `app/` package to already be present in the build context inside the image. Running the install before copying `app/` will fail the image build, so the spec's own verification command (`docker build -t bookstore-api .`) is not achievable as written.
- **Suggested Resolution:** Change the Dockerfile plan so dependency installation does not require the application package before it is copied. For example, either copy `app/` before `pip install .`, or split dependency installation from project installation with an approach the repo can actually support.

### SQLite persistence design is impossible without changing the app's database path
- **Severity:** CRITICAL
- **Description:** The spec says the SQLite database should live in a named volume, while also saying no existing files need modification and the database path remains hardcoded in `app/database.py`. Today the app uses `sqlite:///bookstore.db`, which resolves relative to the working directory. A named volume cannot persist that file cleanly unless the container mounts over the path the app actually writes to, and mounting a volume broadly enough to catch that file would conflict with the application files at `/app`. The persistence design therefore cannot be implemented as specified without changing application configuration or the database path strategy.
- **Suggested Resolution:** Update the spec to include an application configuration change for the database location, preferably via an environment variable with a container-specific path mounted from a named volume. If changing app code is intentionally out of scope, then drop the named-volume persistence requirement and state that the containerized dev database is ephemeral.

### Hot-reload is underspecified for bind mounts on Docker Desktop
- **Severity:** HIGH
- **Description:** The issue acceptance criteria require hot-reload without rebuilding. The spec assumes `uvicorn --reload` alone is sufficient because `uvicorn[standard]` includes `watchfiles`. That is not enough on many Docker Desktop setups, where filesystem events from bind-mounted host files are not delivered reliably into the container. In practice this often requires polling mode for the watcher. Without accounting for that runtime setting, the spec risks missing one of the main promised outcomes on macOS and Windows development environments.
- **Suggested Resolution:** Explicitly define the file-watch strategy for containerized bind mounts, including the required environment variable or reload configuration needed when native file events are unavailable. The testing section should verify reload from a host edit, not just container startup.

### The guide promises in-container test execution, but the image does not install test dependencies
- **Severity:** HIGH
- **Description:** Step 5 says the developer guide should cover running tests inside the container, but Step 2 installs only `pip install .`. In this repo, test tooling lives under the `dev` extra in `pyproject.toml` (`pytest` and `httpx`). As specified, the app image would not contain those dependencies, so the documented workflow would fail or force an undocumented second installation path.
- **Suggested Resolution:** Decide whether the development image is expected to run tests. If yes, update the spec so the image installs `.[dev]` or otherwise includes test dependencies. If no, remove the "run tests inside the container" requirement from the guide.

### The testing section does not verify the spec's claimed data persistence behavior
- **Severity:** MEDIUM
- **Description:** The design calls out a named volume so the SQLite database persists across container restarts, but the Testing section only verifies startup, endpoint access, reload, and shutdown. It never checks the one behavior that justifies introducing the database volume. That leaves a core design claim untested.
- **Suggested Resolution:** Add an explicit persistence test: create data, restart the app stack, and verify the records are still present. If persistence is no longer required after spec revision, remove the named-volume claim from the design.

### The `.dockerignore` plan does not account for the repo's existing local virtualenv naming
- **Severity:** LOW
- **Description:** The `.dockerignore` step excludes `.venv/`, but this working tree already contains `test_venv/`. If a developer has any non-dot virtualenv directory or similar local artifact, it will still be sent in the Docker build context. That is avoidable build bloat and slows the main dev workflow this issue is trying to improve.
- **Suggested Resolution:** Broaden the ignore patterns to cover common virtualenv and local artifact directories beyond `.venv/`, or explicitly ignore `test_venv/` for this repository.
