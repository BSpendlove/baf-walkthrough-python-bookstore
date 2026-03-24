# Code Review: 3-docker-dev-environment

## Findings

### HIGH: In-container test workflow from the spec cannot run the repository test suite
- **Files:** `Dockerfile:5-8`, `.dockerignore:8-9`, `docs/docker-dev-guide.md:39-45`
- The finalized spec requires `docker compose exec app pytest` to work, and the guide tells developers to use that command. The image never copies `tests/` into `/app`, and `.dockerignore` explicitly excludes `tests/`, so the container does not contain the repository test suite. In practice, `pytest` inside the `app` container cannot execute the project tests that the spec says should be runnable there.

### MEDIUM: The guide says containerized tests do not touch the development database, but the app lifespan still initializes the persistent engine
- **Files:** `docs/docker-dev-guide.md:41-47`, `app/main.py:10-13`, `tests/conftest.py:26-39`, `docker-compose.yml:7-9`
- The guide states that tests "do not affect the development database." However, `docker compose exec app pytest` runs with `DATABASE_URL=sqlite:////data/bookstore.db`, and `TestClient(app)` triggers the FastAPI lifespan, which calls `Base.metadata.create_all(bind=engine)` on the persistent app engine before each test client session. Request handling is redirected to the in-memory override, but the persistent database file is still initialized from the test run, so the documentation overstates the isolation guarantee.
