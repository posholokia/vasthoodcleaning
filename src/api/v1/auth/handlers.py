import json
from datetime import (
    datetime,
    timedelta,
    UTC,
)

from apps.clients.actions import AuthClientAction
from apps.clients.exceptions import NotExistsRefreshToken
from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import Router

from core.containers import get_container
from core.security.callable import client_jwt_auth

from ..schema import ResponseStatusSchema
from .schema import (
    AccessTokenSchema,
    AuthRequestSchema,
    ClientPhoneSchema,
    TokenObtainPairSchema,
)


router = Router(tags=["Auth"])


@router.post(
    path="sms_send/",
    response=ResponseStatusSchema,
    description="Request to send an SMS message with a verification code.",
)
def send_sms(
    request: HttpRequest,
    client: ClientPhoneSchema,
) -> ResponseStatusSchema:
    container = get_container()
    action: AuthClientAction = container.resolve(AuthClientAction)

    action.send_code(phone=client.phone)
    return ResponseStatusSchema(
        response=f"Message sent successfully to {client.phone}"
    )


@router.post(
    path="login/",
    response=TokenObtainPairSchema,
    description="Login with phone and verification code.\n"
    "Access token will be in the response from the api, "
    "refresh token will be set in cookies",
)
def login(
    request: HttpRequest,
    credentials: AuthRequestSchema,
) -> HttpResponse:
    container = get_container()
    action: AuthClientAction = container.resolve(AuthClientAction)

    refresh, access = action.login(
        phone=credentials.phone,
        code=credentials.code,
    )
    data = {"access": access}
    response = HttpResponse(content=json.dumps(data).encode())
    response.set_cookie(
        key="refresh",
        value=refresh,
        secure=True,
        httponly=True,
        samesite="Lax",
        expires=datetime.now(UTC) + timedelta(days=1),
    )
    return response


@router.post(
    path="refresh/",
    response=AccessTokenSchema,
    description="Get new access token. "
    "Send the cookie with the refresh token.",
)
def refresh_token(
    request: HttpRequest,
) -> AccessTokenSchema:
    refresh = request.COOKIES.get("refresh")

    if refresh is None:
        raise NotExistsRefreshToken()

    container = get_container()
    action: AuthClientAction = container.resolve(AuthClientAction)
    access = action.refresh_token(refresh=refresh)
    return AccessTokenSchema(access=access)


@router.post(
    path="logout/",
    response=ResponseStatusSchema,
    description="Ban token. Send the cookie with the refresh token.",
)
def logout(
    request: HttpRequest,
) -> HttpResponse:
    refresh = request.COOKIES.get("refresh")

    if refresh is None:
        raise NotExistsRefreshToken()

    container = get_container()
    action: AuthClientAction = container.resolve(AuthClientAction)

    action.logout(refresh=refresh)
    response_obj = ResponseStatusSchema(
        response="You have successfully logged out",
    )
    response = HttpResponse(content=response_obj.json())
    response.delete_cookie(key="refresh", samesite="Lax")
    return response


@router.get(
    path="profile/",
    response=ClientPhoneSchema,
    auth=client_jwt_auth(),
    description="Get client profile.",
)
def get_profile(request: HttpRequest):
    client_phone = request.auth  # type: ignore
    return ClientPhoneSchema(phone=f"+1{client_phone}")
