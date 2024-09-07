from datetime import datetime
from typing import Union

from apps.jobs.models import (
    DiscountType,
    JobStatus,
)
from ninja import (
    Field,
    Schema,
)


T = Union[
    "MultipleSelectSchema",
    "SingleSelectSchema",
    "NumericalRangeSchema",
    "QuantitySelectSchema",
]


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
    status: JobStatus
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


class JobPartSchema(Schema):
    name: str
    cost: int
    inlines: list[T] = Field(default_factory=list)


class JobDetailSchema(Schema):
    parts: list[JobPartSchema]
    materials: MaterialsSchema | None = Field(default=None)
    discount: DiscountSchema | None = Field(default=None)
