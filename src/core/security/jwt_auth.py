from typing import Any

from apps.clients.services.jwt_tokens.models import BlacklistRefreshToken
from config.containers import get_container
from django.http import HttpRequest
from ninja.security import HttpBearer
from services.jwt_token.exceptions import BaseJWTException


class AuthBearer(HttpBearer):
    def __init__(self):
        super().__init__()
        container = get_container()
        token_service = container.resolve(BlacklistRefreshToken)
        self.token_service = token_service

    def authenticate(self, request: HttpRequest, token: str) -> Any | None:
        try:
            payload = self.token_service.decode(token)
            return payload.get("client")
        except BaseJWTException:
            return None
