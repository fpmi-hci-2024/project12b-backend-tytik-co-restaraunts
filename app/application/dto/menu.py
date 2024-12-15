import uuid

from dataclasses import dataclass, field
from typing import TypeAlias

from app.application.dto.base import ListItemsDTO


@dataclass(frozen=True)
class Menu:
    id: uuid.UUID
    name: str
    restaurant_id: uuid.UUID
    is_deleted: bool = field(default=False)


Menus: TypeAlias = ListItemsDTO[Menu]
