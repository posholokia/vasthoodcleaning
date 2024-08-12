import json
from datetime import datetime, timedelta

from apps.clients.actions import AuthClientAction
from apps.clients.services.exceptions import NotExistsRefreshToken
from config.containers import get_container
from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import Router

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
async def send_sms(
    request: HttpRequest,
    client: ClientPhoneSchema,
) -> ResponseStatusSchema:
    container = get_container()
    action: AuthClientAction = container.resolve(AuthClientAction)

    await action.send_code(phone=client.phone)
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
async def login(
    request: HttpRequest,
    credentials: AuthRequestSchema,
) -> HttpResponse:
    container = get_container()
    action: AuthClientAction = container.resolve(AuthClientAction)

    refresh, access = await action.login(
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
        expires=datetime.now() + timedelta(days=1)
    )
    return response


@router.post(
    path="refresh/",
    response=AccessTokenSchema,
    description="Get new access token. "
    "Send the cookie with the refresh token.",
)
async def refresh_token(
    request: HttpRequest,
) -> AccessTokenSchema:
    refresh = request.COOKIES.get("refresh")

    if refresh is None:
        raise NotExistsRefreshToken()

    container = get_container()
    action: AuthClientAction = container.resolve(AuthClientAction)
    access = await action.refresh_token(refresh=refresh)
    return AccessTokenSchema(access=access)


@router.post(
    path="logout/",
    response=ResponseStatusSchema,
    description="Ban token. Send the cookie with the refresh token.",
)
async def logout(
    request: HttpRequest,
) -> ResponseStatusSchema:
    refresh = request.COOKIES.get("refresh")

    if refresh is None:
        raise NotExistsRefreshToken()

    container = get_container()
    action: AuthClientAction = container.resolve(AuthClientAction)

    await action.logout(
        refresh=refresh,
    )
    return ResponseStatusSchema(
        response="You have successfully logged out",
    )
