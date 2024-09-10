from typing import Any

from apps.clients.services.jwt_tokens.models import BlacklistRefreshToken
from django.http import HttpRequest
from ninja.security import HttpBearer

from core.containers import get_container
from core.jwt_token.exceptions import BaseJWTException


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Any | None:
        try:
            container = get_container()
            token_service = container.resolve(BlacklistRefreshToken)
            payload = token_service.decode(token)
            return payload.get("client").lstrip("+1")
        except BaseJWTException:
            return None
