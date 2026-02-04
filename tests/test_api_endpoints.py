import httpx
import pytest


@pytest.mark.asyncio
async def test_geo_by_ip(async_client, respx_mock) -> None:
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

    response = await async_client.get("/v1/geo/8.8.8.8")

    assert response.status_code == 200
    assert response.json()["ip"] == "8.8.8.8"


@pytest.mark.asyncio
async def test_geo_for_client_uses_forwarded_for(async_client, respx_mock) -> None:
    payload = {
        "status": "success",
        "query": "1.1.1.1",
        "country": "Australia",
        "regionName": "Queensland",
        "city": "South Brisbane",
        "lat": -27.4748,
        "lon": 153.017,
        "timezone": "Australia/Brisbane",
        "isp": "Cloudflare",
    }
    respx_mock.get("http://ip-api.com/json/1.1.1.1").mock(
        return_value=httpx.Response(200, json=payload)
    )

    response = await async_client.get(
        "/v1/geo", headers={"x-forwarded-for": "1.1.1.1"}
    )

    assert response.status_code == 200
    assert response.json()["ip"] == "1.1.1.1"


@pytest.mark.asyncio
async def test_geo_by_ip_invalid(async_client) -> None:
    response = await async_client.get("/v1/geo/not-an-ip")

    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "invalid_ip"
