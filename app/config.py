from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    ip_api_base_url: str
    http_timeout_seconds: float


def get_settings() -> Settings:
    return Settings(
        ip_api_base_url=os.getenv("IP_API_BASE_URL", "http://ip-api.com"),
        http_timeout_seconds=float(os.getenv("HTTP_TIMEOUT_SECONDS", "5.0")),
    )
