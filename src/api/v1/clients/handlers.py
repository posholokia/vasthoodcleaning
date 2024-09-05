from django.http import HttpRequest
from ninja import Router

from core.security.jwt_auth import AuthBearer

from ..schema import ResponseStatusSchema


router = Router(tags=["Clients"])


@router.get(
    path="test_auth/",
    response=ResponseStatusSchema,
    auth=AuthBearer(),
    description="Тест проверка аутентификации",
)
async def test_auth(
    request: HttpRequest,
) -> ResponseStatusSchema:
    return ResponseStatusSchema(
        response=f"Successful auth {request.auth}"  # type: ignore
    )
