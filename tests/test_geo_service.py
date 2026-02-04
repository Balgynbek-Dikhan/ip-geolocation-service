import pytest

from app.errors import InvalidIPError
from app.models import GeoResponse
from app.services.geo_service import GeoService
from app.services.providers import GeoProvider


class DummyProvider(GeoProvider):
    async def lookup(self, ip: str) -> GeoResponse:
        return GeoResponse(ip=ip)


@pytest.mark.asyncio
async def test_geo_service_rejects_invalid_ip() -> None:
    service = GeoService(DummyProvider())

    with pytest.raises(InvalidIPError):
        await service.lookup_ip("not-an-ip")
