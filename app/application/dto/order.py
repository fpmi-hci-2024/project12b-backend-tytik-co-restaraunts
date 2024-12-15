import datetime
import decimal
import uuid

from dataclasses import dataclass
from typing import TypeAlias

from app.application.dto.base import ListItemsDTO


@dataclass(frozen=True)
class Order:
    id: uuid.UUID
    name_for_client: str
    order_date: datetime.datetime
    order_delivery_date: datetime.datetime | None
    order_status: str
    order_price: decimal.Decimal
    is_deleted: bool


Orders: TypeAlias = ListItemsDTO[Order]
