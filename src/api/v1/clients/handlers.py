from django.http import HttpRequest
from ninja import Router

from core.security.callable import client_jwt_auth

from ..schema import ResponseStatusSchema


router = Router(tags=["Clients"])


@router.get(
    path="test_auth/",
    response=ResponseStatusSchema,
    auth=client_jwt_auth(),
    description="Тест проверка аутентификации",
)
def test_auth(
    request: HttpRequest,
) -> ResponseStatusSchema:
    return ResponseStatusSchema(
        response=f"Successful auth {request.auth}"  # type: ignore
    )
