from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Stable error code for programmatic handling.")
    message: str = Field(..., description="Human-readable error message.")
    details: Any | None = Field(
        default=None, description="Optional details for debugging or client display."
    )


class ErrorResponse(BaseModel):
    error: ErrorDetail


class AppError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: Any | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


class InvalidIPError(AppError):
    def __init__(self, ip: str) -> None:
        super().__init__(
            status_code=400,
            code="invalid_ip",
            message="Invalid IP address.",
            details={"ip": ip},
        )


class NotFoundError(AppError):
    def __init__(self, ip: str, reason: str | None = None) -> None:
        super().__init__(
            status_code=404,
            code="ip_not_found",
            message="IP address not found.",
            details={"ip": ip, "reason": reason} if reason else {"ip": ip},
        )


class UpstreamError(AppError):
    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(
            status_code=502,
            code="upstream_error",
            message=message,
            details=details,
        )


class RateLimitError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=429,
            code="rate_limited",
            message=message,
        )
