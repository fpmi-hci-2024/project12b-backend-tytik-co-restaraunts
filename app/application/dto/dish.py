import decimal
import uuid
from dataclasses import dataclass
from typing import TypeAlias

from app.application.dto.base import ListItemsDTO


@dataclass(frozen=True)
class Order:
    id: uuid.UUID
    name: str
    price: decimal.Decimal
    menu_id: uuid.UUID
    is_deleted: bool


Orders: TypeAlias = ListItemsDTO[Order]
