from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from apps.jobs.models.dataclasses_ import (
    DiscountType,
    JobStatus,
    NoneLessThanDate,
)


@dataclass
class JobEntity:
    id: str
    schedule: datetime | None
    address: str
    status: JobStatus
    total_cost: int
    paid: bool = field(default=False)
    last_updated: datetime = field(default_factory=datetime.now)

    @property
    def sort_by_schedule(self):
        """
        Работы должны быть отсортированы в порядке: сперва без
        schedule, затем от тех что раньше к тем что позже.
        None нельзя сравнить с datetime, поэтому для работ
        где schedule=None возвращает объект, который меньше
        datetime и равен None.
        """
        return self.schedule if self.schedule else NoneLessThanDate()


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
