from dataclasses import dataclass
from datetime import datetime
from typing import (
    Annotated,
)

from annotated_types import (
    MaxLen,
    MinLen,
)


@dataclass
class UserEntity:
    id: int
    password: str
    phone: Annotated[str, MinLen(1), MaxLen(16)]
    date_joined: datetime
    is_active: bool
    is_staff: bool
