from app.errors import InvalidIPError
from app.models import GeoResponse
from app.services.providers import GeoProvider
from app.utils import validate_ip


class GeoService:
    def __init__(self, provider: GeoProvider) -> None:
        self._provider = provider

    async def lookup_ip(self, ip: str) -> GeoResponse:
        if not validate_ip(ip):
            raise InvalidIPError(ip)
        return await self._provider.lookup(ip)
