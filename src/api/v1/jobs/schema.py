from datetime import datetime

from apps.jobs.models import DiscountType
from ninja import (
    Field,
    Schema,
)


class MultipleSelectSchema(Schema):
    name: str
    choices: list[str]
    kind: str = Field(init=False, default="multiple")


class SingleSelectSchema(Schema):
    name: str
    choice: str
    kind: str = Field(init=False, default="single")


class NumericalRangeSchema(Schema):
    name: str
    choice: str
    kind: str = Field(init=False, default="range")


class QuantitySelectSchema(Schema):
    name: str
    value: int
    kind: str = Field(init=False, default="quantity")


class JobSchema(Schema):
    id: str
    schedule: datetime | None
    address: str
    status: str
    paid: bool
    total_cost: int


class DiscountSchema(Schema):
    kind: DiscountType
    value: int


class DetailMaterialSchema(Schema):
    name: str
    quantity: float


class MaterialsSchema(Schema):
    total_cost: int
    detail: list[DetailMaterialSchema]


T = list[
    MultipleSelectSchema
    | SingleSelectSchema
    | NumericalRangeSchema
    | QuantitySelectSchema
]


class JobPartSchema(Schema):
    name: str
    cost: int
    inlines: T = Field(default_factory=list)


class JobDetailSchema(Schema):
    parts: list[JobPartSchema]
    cost_before_discount: int
    materials: MaterialsSchema | None = Field(default=None)
    discount: DiscountSchema | None = Field(default=None)
