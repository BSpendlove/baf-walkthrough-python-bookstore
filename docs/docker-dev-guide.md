# Docker Development Guide

This guide covers running the Bookstore API in Docker for local development.

## Prerequisites

- Docker Engine installed
- Docker Compose plugin (`docker compose` command available)

## Starting the Environment

```bash
docker compose up --build
```

This starts two services:

- **app** — FastAPI application on port 8000 (direct access)
- **caddy** — Reverse proxy with automatic TLS on port 443

The first build pulls base images and installs dependencies. Subsequent starts are faster due to layer caching.

## Accessing the API

| URL | Description |
|-----|-------------|
| `https://bookstore.localhost` | API via Caddy (TLS) |
| `https://bookstore.localhost/docs` | Swagger UI |
| `http://localhost:8000` | Direct access (no TLS) |

Your browser will warn about the self-signed certificate on first visit. Accept the certificate to proceed.

## Hot-Reload

The `app/` directory is bind-mounted into the container. When you edit any Python file in `app/` on your host machine, uvicorn detects the change and restarts automatically. No container rebuild needed.

`WATCHFILES_FORCE_POLLING=true` is set by default in docker-compose.yml to ensure file change detection works reliably across all platforms, including macOS and Windows with Docker Desktop.

## Running Tests

Tests run inside the container with all dev dependencies available:

```bash
docker compose exec app pytest
```

Tests use an in-memory SQLite database for request handling. Note that the FastAPI lifespan may still initialize the persistent database schema on startup, but test data is fully isolated.

## Stopping the Environment

```bash
# Stop and remove containers (data persists in volumes)
docker compose down

# Stop and remove containers AND volumes (deletes all data)
docker compose down -v
```

## Data Persistence

The SQLite database is stored in a named Docker volume (`bookstore_data`). Data persists across `docker compose down` and `docker compose up` cycles. To reset the database, use `docker compose down -v` to remove the volume.

## Troubleshooting

### `bookstore.localhost` not resolving

Most modern browsers resolve `*.localhost` to `127.0.0.1` automatically. If it doesn't work in your environment, add this to your `/etc/hosts` file (or `C:\Windows\System32\drivers\etc\hosts` on Windows):

```
127.0.0.1 bookstore.localhost
```

### Hot-reload not working

The `WATCHFILES_FORCE_POLLING` environment variable is already set to `true` in `docker-compose.yml`. If changes still aren't detected, verify that you're editing files inside the `app/` directory (other directories are not mounted into the container).

### Port conflicts

If ports 80, 443, or 8000 are already in use, either stop the conflicting service or change the port mappings in `docker-compose.yml`.
