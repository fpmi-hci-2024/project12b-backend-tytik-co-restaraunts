import datetime
import uuid

from dataclasses import dataclass
from app.domain.common.value_object import ValueObject


@dataclass(frozen=True)
class RestaurantId(ValueObject[uuid.UUID]):
    value: uuid.UUID


@dataclass(frozen=True)
class RestaurantName(ValueObject[str]):
    value: str


@dataclass(frozen=True)
class RestaurantCuisineName(ValueObject[str]):
    value: str


@dataclass(frozen=True)
class IsDeleted(ValueObject[bool]):
    value: bool


@dataclass
class Restaurant:
    id: RestaurantId
    name: RestaurantName
    cuisine_name: RestaurantCuisineName
    is_deleted: IsDeleted

    @classmethod
    def create(
        cls,
        id: RestaurantId,
        name: RestaurantName,
        cuisine_name: RestaurantCuisineName,
        is_deleted: IsDeleted
    ) -> "Restaurant":
        restaurant = cls(id, name, cuisine_name, is_deleted)

        return restaurant
