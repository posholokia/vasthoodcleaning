from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from enum import Enum


class JobStatus(Enum):
    pending: str = "Pending"
    scheduled: str = "Scheduled"
    in_progress: str = "In Progress"
    completed: str = "Completed"
    canceled: str = "canceled"  # не отображается


@dataclass
class JobEntity:
    id: str
    schedule: datetime | None
    address: str
    status: JobStatus
    total_cost: int
    paid: bool = field(default=False)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class MultipleSelectEntity:
    name: str
    choices: list[str]
    kind: str = field(init=False, default="multiple")


@dataclass
class NumericalRangeEntity:
    name: str
    choice: str
    kind: str = field(init=False, default="range")


@dataclass
class SingleSelectEntity:
    name: str
    choice: str
    kind: str = field(init=False, default="single")


@dataclass
class QuantitySelectEntity:
    name: str
    value: int
    kind: str = field(init=False, default="quantity")


class DiscountType(Enum):
    fixed: str = "fixed discount"
    percent: str = "percent discount"


@dataclass
class DiscountEntity:
    kind: DiscountType
    value: int


@dataclass
class DetailMaterialEntity:
    name: str
    quantity: float
    cost: int


@dataclass
class MaterialsEntity:
    total_cost: int
    detail: list[DetailMaterialEntity]

    def __bool__(self) -> bool:
        return bool(self.total_cost or self.detail)


T = list[
    SingleSelectEntity
    | MultipleSelectEntity
    | NumericalRangeEntity
    | QuantitySelectEntity
]


@dataclass
class JobPartEntity:
    name: str
    cost: int
    inlines: T = field(default_factory=list)


@dataclass
class JobDetailEntity:
    parts: list[JobPartEntity]
    cost_before_discount: int
    materials: MaterialsEntity | None = field(default=None)
    discount: DiscountEntity | None = field(default=None)
