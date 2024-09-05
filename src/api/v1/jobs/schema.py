from datetime import datetime

from ninja import Schema, Field

from apps.jobs.models import JobStatus, DiscountType


class MultipleSelect(Schema):
    name: str
    choices: list[str]
    kind: str = Field(init=False, default="multiple")


class SingleSelect(Schema):
    name: str
    choice: str
    kind: str = Field(init=False, default="single")


class QuantitySelect(Schema):
    name: str
    value: int
    kind: str = Field(init=False, default="quantity")


class JobSchema(Schema):
    id: str
    schedule: datetime | None
    address: str
    status: JobStatus
    total_cost: int


class MultipleSelectSchema(Schema):
    name: str
    choices: list[str]
    kind: str = Field(init=False, default="multiple")


class NumericalRangeSchema(Schema):
    name: str
    choice: str
    kind: str = Field(init=False, default="range")


class SingleSelectSchema(Schema):
    name: str
    choice: str
    kind: str = Field(init=False, default="single")


class QuantitySelectSchema(Schema):
    name: str
    value: int
    kind: str = Field(init=False, default="quantity")


class DiscountSchema(Schema):
    type: DiscountType
    value: int


class DetailMaterialSchema(Schema):
    name: str
    quantity: float


class MaterialsSchema(Schema):
    cost: int
    detail: list[DetailMaterialSchema]


class JobDetailSchema(Schema):
    name: str
    cost: int
    inlines: list[
        MultipleSelectSchema |
        NumericalRangeSchema |
        SingleSelectSchema |
        QuantitySelectSchema
    ]
    materials: MaterialsSchema
    discount: DiscountSchema
