from abc import ABC, abstractmethod

from app.models import GeoResponse


class GeoProvider(ABC):
    @abstractmethod
    async def lookup(self, ip: str) -> GeoResponse:
        raise NotImplementedError


class FakeGeoProvider(GeoProvider):
    async def lookup(self, ip: str) -> GeoResponse:
        return GeoResponse(
            ip=ip,
            country="United States",
            region="California",
            city="San Francisco",
            latitude=37.7749,
            longitude=-122.4194,
            timezone="America/Los_Angeles",
            isp="Example ISP",
            source="fake",
        )
