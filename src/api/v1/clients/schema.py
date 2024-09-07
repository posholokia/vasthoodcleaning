# from typing import Annotated
#
# from annotated_types import (
#     MaxLen,
#     MinLen,
# )
# from ninja import Schema
#
#
# class ClientPhoneSchema(Schema):
#     phone: Annotated[str, MinLen(10), MaxLen(16)]
#
#
# class AuthRequestSchema(ClientPhoneSchema):
#     code: Annotated[str, MinLen(6), MaxLen(6)]
#
#
# class AccessTokenSchema(Schema):
#     access: str
#
#
# class RefreshTokenSchema(Schema):
#     refresh: str
#
#
# class TokenObtainPairSchema(AccessTokenSchema, RefreshTokenSchema):
#     pass
