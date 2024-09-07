from ninja import Schema, Field


class ResponseStatusSchema(Schema):
    response: str = Field(default="Status: Ok")
