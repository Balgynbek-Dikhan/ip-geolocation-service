from fastapi import APIRouter, Depends, Request

from app.dependencies import get_geo_service
from app.errors import ErrorResponse
from app.models import GeoResponse
from app.services.geo_service import GeoService
from app.utils import get_request_ip

router = APIRouter(prefix="/v1", tags=["geolocation"])


@router.get(
    "/geo/{ip}",
    response_model=GeoResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid IP address."},
        404: {"model": ErrorResponse, "description": "IP not found."},
        429: {"model": ErrorResponse, "description": "Rate limited by provider."},
        502: {"model": ErrorResponse, "description": "Upstream provider failure."},
    },
    summary="Lookup geolocation for a specific IP address",
)
async def geo_by_ip(
    ip: str, service: GeoService = Depends(get_geo_service)
) -> GeoResponse:
    return await service.lookup_ip(ip)


@router.get(
    "/geo",
    response_model=GeoResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid IP address."},
        404: {"model": ErrorResponse, "description": "IP not found."},
        429: {"model": ErrorResponse, "description": "Rate limited by provider."},
        502: {"model": ErrorResponse, "description": "Upstream provider failure."},
    },
    summary="Lookup geolocation for the requesting client IP",
)
async def geo_for_client(
    request: Request, service: GeoService = Depends(get_geo_service)
) -> GeoResponse:
    ip = get_request_ip(request)
    return await service.lookup_ip(ip)
