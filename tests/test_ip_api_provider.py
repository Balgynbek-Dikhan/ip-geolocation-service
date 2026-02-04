import httpx
import pytest

from app.errors import InvalidIPError, NotFoundError, RateLimitError, UpstreamError
from app.services.ip_api_provider import IpApiProvider


@pytest.mark.asyncio
async def test_ip_api_provider_success(respx_mock) -> None:
    payload = {
        "status": "success",
        "query": "8.8.8.8",
        "country": "United States",
        "regionName": "California",
        "city": "Mountain View",
        "lat": 37.386,
        "lon": -122.084,
        "timezone": "America/Los_Angeles",
        "isp": "Google LLC",
    }
    respx_mock.get("http://ip-api.com/json/8.8.8.8").mock(
        return_value=httpx.Response(200, json=payload)
    )

    async with httpx.AsyncClient() as client:
        provider = IpApiProvider(client, "http://ip-api.com")
        result = await provider.lookup("8.8.8.8")

    assert result.ip == "8.8.8.8"
    assert result.country == "United States"
    assert result.source == "ip-api"


@pytest.mark.asyncio
async def test_ip_api_provider_invalid_query(respx_mock) -> None:
    respx_mock.get("http://ip-api.com/json/999").mock(
        return_value=httpx.Response(200, json={"status": "fail", "message": "invalid query"})
    )

    async with httpx.AsyncClient() as client:
        provider = IpApiProvider(client, "http://ip-api.com")
        with pytest.raises(InvalidIPError):
            await provider.lookup("999")


@pytest.mark.asyncio
async def test_ip_api_provider_not_found(respx_mock) -> None:
    respx_mock.get("http://ip-api.com/json/203.0.113.1").mock(
        return_value=httpx.Response(200, json={"status": "fail", "message": "private range"})
    )

    async with httpx.AsyncClient() as client:
        provider = IpApiProvider(client, "http://ip-api.com")
        with pytest.raises(NotFoundError):
            await provider.lookup("203.0.113.1")


@pytest.mark.asyncio
async def test_ip_api_provider_rate_limited(respx_mock) -> None:
    respx_mock.get("http://ip-api.com/json/8.8.4.4").mock(
        return_value=httpx.Response(429)
    )

    async with httpx.AsyncClient() as client:
        provider = IpApiProvider(client, "http://ip-api.com")
        with pytest.raises(RateLimitError):
            await provider.lookup("8.8.4.4")


@pytest.mark.asyncio
async def test_ip_api_provider_timeout(respx_mock) -> None:
    respx_mock.get("http://ip-api.com/json/1.1.1.1").mock(
        side_effect=httpx.TimeoutException("timeout")
    )

    async with httpx.AsyncClient() as client:
        provider = IpApiProvider(client, "http://ip-api.com")
        with pytest.raises(UpstreamError):
            await provider.lookup("1.1.1.1")
