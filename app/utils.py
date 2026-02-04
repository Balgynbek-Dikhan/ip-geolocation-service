import ipaddress
from typing import cast

from fastapi import Request


def validate_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
    except ValueError:
        return False
    return True


def get_request_ip(request: Request) -> str:
    forwarded_for = cast(str | None, request.headers.get("x-forwarded-for"))
    if forwarded_for:
        return cast(str, forwarded_for.split(",")[0].strip())

    client = request.client
    if client is None or client.host is None:
        return ""

    return str(client.host)
