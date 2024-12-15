from dataclasses import dataclass, field
from typing import TypeAlias
from uuid import UUID

from app.application.dto.base import ListItemsDTO
from app.domain.common.pagination import PaginatedItemsDTO


@dataclass(frozen=True)
class Restaurant:
    id: UUID
    name: str
    cuisine_name: str
    is_deleted: bool = field(default=False)


RestaurantDTO: TypeAlias = ListItemsDTO[Restaurant]
Restaurants: TypeAlias = PaginatedItemsDTO[RestaurantDTO]
