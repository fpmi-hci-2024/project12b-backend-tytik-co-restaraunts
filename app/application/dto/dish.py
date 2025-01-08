import decimal
import uuid
from dataclasses import dataclass
from typing import TypeAlias

from app.application.dto.base import ListItemsDTO
from app.domain.common.pagination import PaginatedItemsDTO


@dataclass(frozen=True)
class Dish:
    id: uuid.UUID
    name: str
    price: decimal.Decimal
    menu_id: uuid.UUID
    logo_url: str
    dishes_type: str
    ingredients: str
    is_deleted: bool


DishDTO: TypeAlias = ListItemsDTO[Dish]
Dishes: TypeAlias = PaginatedItemsDTO[DishDTO]
