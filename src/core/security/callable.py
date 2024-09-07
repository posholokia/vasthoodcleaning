from ninja.security import APIKeyHeader

from core.containers import get_container
from core.security.auth.jwt_auth import AuthBearer


def crm_api_key_auth() -> APIKeyHeader:
    container = get_container()
    return container.resolve(APIKeyHeader)


def client_jwt_auth() -> AuthBearer:
    return AuthBearer()
