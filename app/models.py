from pydantic import BaseModel, Field


class GeoResponse(BaseModel):
    ip: str = Field(..., description="The IP address that was looked up.")
    country: str | None = Field(default=None, description="Country name.")
    region: str | None = Field(default=None, description="Region or state.")
    city: str | None = Field(default=None, description="City name.")
    latitude: float | None = Field(default=None, description="Latitude coordinate.")
    longitude: float | None = Field(default=None, description="Longitude coordinate.")
    timezone: str | None = Field(default=None, description="Timezone identifier.")
    isp: str | None = Field(default=None, description="Internet service provider.")
    source: str | None = Field(
        default=None, description="Upstream provider identifier."
    )
