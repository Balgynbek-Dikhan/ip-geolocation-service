import httpx

from app.errors import InvalidIPError, NotFoundError, RateLimitError, UpstreamError
from app.models import GeoResponse
from app.services.providers import GeoProvider


class IpApiProvider(GeoProvider):
    def __init__(self, client: httpx.AsyncClient, base_url: str) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")

    async def lookup(self, ip: str) -> GeoResponse:
        try:
            response = await self._client.get(
                f"{self._base_url}/json/{ip}",
                params={
                    "fields": "status,message,country,regionName,city,lat,lon,timezone,isp,query"
                },
            )
        except httpx.TimeoutException as exc:
            raise UpstreamError("Upstream provider timeout.", details=str(exc)) from exc
        except httpx.RequestError as exc:
            raise UpstreamError("Upstream provider request failed.", details=str(exc)) from exc

        if response.status_code == 429:
            raise RateLimitError("Upstream rate limit exceeded.")
        if response.status_code >= 500:
            raise UpstreamError(
                "Upstream provider error.",
                details={"status_code": response.status_code},
            )
        if response.status_code != 200:
            raise UpstreamError(
                "Unexpected upstream response.",
                details={"status_code": response.status_code},
            )

        payload = response.json()
        if payload.get("status") != "success":
            message = payload.get("message", "lookup failed")
            if message == "invalid query":
                raise InvalidIPError(ip)
            raise NotFoundError(ip, reason=message)

        return GeoResponse(
            ip=payload.get("query", ip),
            country=payload.get("country"),
            region=payload.get("regionName"),
            city=payload.get("city"),
            latitude=payload.get("lat"),
            longitude=payload.get("lon"),
            timezone=payload.get("timezone"),
            isp=payload.get("isp"),
            source="ip-api",
        )
