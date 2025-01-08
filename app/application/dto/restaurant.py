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
    logo_url: str
    is_deleted: bool = field(default=False)


@dataclass(frozen=True)
class DeletedRestaurant:
    id: UUID
    name: str
    cuisine_name: str
    logo_url: str
    is_deleted: bool


RestaurantDTO: TypeAlias = ListItemsDTO[Restaurant]
Restaurants: TypeAlias = PaginatedItemsDTO[RestaurantDTO]
