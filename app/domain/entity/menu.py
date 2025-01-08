import uuid
from dataclasses import dataclass

from app.domain.common.value_object import ValueObject


@dataclass(frozen=True)
class MenuId(ValueObject[uuid.UUID]):
    value: uuid.UUID


@dataclass(frozen=True)
class MenuName(ValueObject[str]):
    value: str


@dataclass(frozen=True)
class MenuRestaurantId(ValueObject[uuid.UUID]):
    value: uuid.UUID


@dataclass(frozen=True)
class IsDeleted(ValueObject[bool]):
    value: bool


@dataclass(frozen=True)
class MenuLogoUrl(ValueObject[str]):
    value: str


@dataclass
class Menu:
    id: MenuId
    name: MenuName
    restaurant_id: MenuRestaurantId
    logo_url: MenuLogoUrl
    is_deleted: bool

    @classmethod
    def create(
        cls,
        id: MenuId,
        name: MenuName,
        restaurant_id: MenuRestaurantId,
        logo_url: MenuLogoUrl,
        is_deleted: bool,
    ) -> "Menu":
        menu = cls(id, name, restaurant_id, logo_url, is_deleted)
        return menu

    def delete(self) -> None:
        self.is_deleted = True

    def set_name(self, new_name) -> None:
        self._is_delete()
        self.name = new_name

    def _is_delete(self):
        return False
