import uuid

from dataclasses import dataclass, field
from typing import TypeAlias

from app.application.dto.base import ListItemsDTO
from app.domain.common.pagination import PaginatedItemsDTO


@dataclass(frozen=True)
class Menu:
    id: uuid.UUID
    name: str
    restaurant_id: uuid.UUID
    logo_url: str = field(default="")
    is_deleted: bool = field(default=False)


@dataclass(frozen=True)
class DeletedMenu:
    id: uuid.UUID
    name: str
    restaurant_id: uuid.UUID
    logo_url: str
    is_deleted: bool


MenuDTO: TypeAlias = ListItemsDTO[Menu]
Menus: TypeAlias = PaginatedItemsDTO[MenuDTO]
