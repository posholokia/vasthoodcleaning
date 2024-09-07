from ninja import (
    Field,
    Schema,
)


class ResponseStatusSchema(Schema):
    response: str = Field(default="Status: Ok")
