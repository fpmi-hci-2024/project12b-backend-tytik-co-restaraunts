import decimal
import uuid
from dataclasses import dataclass

from app.domain.common.value_object import ValueObject


@dataclass(frozen=True)
class DishId(ValueObject[uuid.UUID]):
    value: uuid.UUID


@dataclass(frozen=True)
class DishName(ValueObject[str]):
    value: str


@dataclass(frozen=True)
class DishPrice(ValueObject[decimal.Decimal]):
    value: decimal.Decimal


@dataclass(frozen=True)
class DishMenuId(ValueObject[uuid.UUID]):
    value: uuid.UUID


@dataclass(frozen=True)
class DishLogoUrl(ValueObject[str]):
    value: str


@dataclass(frozen=True)
class DishType(ValueObject[str]):
    value: str


@dataclass(frozen=True)
class DishIngredients(ValueObject[str]):
    value: str


@dataclass(frozen=True)
class IsDeleted(ValueObject[bool]):
    value: bool


@dataclass
class Dish:
    id: DishId
    name: DishName
    price: DishPrice
    menu_id: DishMenuId
    logo_url: DishLogoUrl
    dishes_type: DishType
    ingredients: DishIngredients
    is_deleted: bool

    @classmethod
    def create(
        cls,
        id: DishId,
        name: DishName,
        price: DishPrice,
        menu_id: DishMenuId,
        logo_url: DishLogoUrl,
        dishes_type: DishType,
        ingredients: DishIngredients,
        is_deleted: bool,
    ) -> "Dish":
        dish = cls(
            id, name, price, menu_id, logo_url, dishes_type, ingredients, is_deleted
        )
        return dish

    def delete(self) -> None:
        self.is_deleted = True

    def set_name(self, new_name) -> None:
        self._is_delete()
        self.name = new_name

    def _is_delete(self):
        return False
