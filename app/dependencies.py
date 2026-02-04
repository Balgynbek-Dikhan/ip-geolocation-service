from fastapi import Request

from app.services.geo_service import GeoService
from app.services.providers import GeoProvider


def get_geo_provider(request: Request) -> GeoProvider:
    provider = request.app.state.geo_provider
    if not isinstance(provider, GeoProvider):
        raise RuntimeError("Geolocation provider is not initialized.")
    return provider


def get_geo_service(request: Request) -> GeoService:
    provider = get_geo_provider(request)
    return GeoService(provider)
