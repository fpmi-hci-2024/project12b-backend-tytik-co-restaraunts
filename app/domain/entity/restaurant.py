import uuid

from dataclasses import dataclass
from app.domain.common.value_object import ValueObject
from app.domain.exceptions.restaurant import RestaurantIsDeletedError


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


@dataclass(frozen=True)
class RestaurantLogoUrl(ValueObject[str]):
    value: str


@dataclass
class Restaurant:
    id: RestaurantId
    name: RestaurantName
    cuisine_name: RestaurantCuisineName
    logo_url: RestaurantLogoUrl
    is_deleted: bool

    @classmethod
    def create(
        cls,
        id: RestaurantId,
        name: RestaurantName,
        cuisine_name: RestaurantCuisineName,
        logo_url: RestaurantLogoUrl,
        is_deleted: bool,
    ) -> "Restaurant":
        restaurant = cls(id, name, cuisine_name, logo_url, is_deleted)
        return restaurant

    def delete(self) -> None:
        self.is_deleted = True

    def set_name(self, new_name) -> None:
        self._is_delete()
        self.name = new_name

    def _is_delete(self):
        if self.is_deleted:
            raise RestaurantIsDeletedError(self.id.to_raw())
