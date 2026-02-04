from contextlib import asynccontextmanager
from typing import AsyncIterator

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router as geo_router
from app.config import get_settings
from app.errors import AppError, ErrorResponse
from app.services.ip_api_provider import IpApiProvider
from app.services.providers import GeoProvider


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    client = httpx.AsyncClient(timeout=settings.http_timeout_seconds)
    provider: GeoProvider = IpApiProvider(client, settings.ip_api_base_url)
    if not isinstance(provider, GeoProvider):
        raise RuntimeError("Geolocation provider failed to initialize.")
    app.state.http_client = client
    app.state.geo_provider = provider
    yield
    await client.aclose()


app = FastAPI(
    title="IP Geolocation Service",
    version="1.0.0",
    description=(
        "FastAPI microservice that returns geolocation data for a given IP address "
        "or the requesting client."
    ),
    lifespan=lifespan,
)

app.include_router(geo_router)


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        ).model_dump(exclude_none=True),
    )
