from ninja.security import APIKeyHeader

from config.containers import get_container


def crm_api_key_auth() -> APIKeyHeader:
    container = get_container()
    return container.resolve(APIKeyHeader)
