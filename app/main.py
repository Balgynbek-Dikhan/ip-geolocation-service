from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router as geo_router
from app.errors import AppError, ErrorResponse
from app.services.providers import FakeGeoProvider, GeoProvider


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    provider: GeoProvider = FakeGeoProvider()
    if not isinstance(provider, GeoProvider):
        raise RuntimeError("Geolocation provider failed to initialize.")
    app.state.geo_provider = provider
    yield


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
