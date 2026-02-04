# IP Geolocation Service

FastAPI microservice for IP address geolocation, implemented as a take-home
exercise.

## Overview

The service exposes endpoints to:
- Look up geolocation information for an explicit IP address.
- Look up geolocation information for the calling client IP.

The API is designed spec-first, with an OpenAPI definition stored at
`openapi/openapi.yaml`.

## Requirements

- Python 3.11+
- uv for environment and dependency management

## Environment setup (uv)

1) Install uv (one-time per machine):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2) Create and sync the virtual environment:

```bash
uv venv .venv
uv pip install -e ".[dev]"
```

## Running the API locally

```bash
uv run uvicorn app.main:app --reload
```

By default, the app listens on `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## OpenAPI spec (source of truth)

The canonical OpenAPI spec is stored at `openapi/openapi.yaml`.
To regenerate it from the FastAPI app:

```bash
uv run python export_openapi.py
```

This also writes `openapi/openapi.json`.

## API design decisions

- Versioned routes under `/v1` for forward compatibility.
- Consistent error envelope: `{ "error": { "code", "message", "details?" } }`.
- Thin routers; business logic lives in services and providers.
- Explicit resource initialization in `lifespan`.

## Tests

```bash
uv run pytest
```

## Code quality

Lint and format with ruff:

```bash
uv run ruff check .
uv run ruff format .
```

Type checking:

```bash
uv run mypy .
```

### Pre-commit hooks

Install hooks:

```bash
uv run pre-commit install
```

Run all hooks:

```bash
uv run pre-commit run --all-files
```

## Endpoints

- `GET /v1/geo/{ip}`: lookup by IP
- `GET /v1/geo`: lookup for the requesting client IP

## Development notes

See `DEVELOPMENT_NOTES.md` for implementation details and reflection.
