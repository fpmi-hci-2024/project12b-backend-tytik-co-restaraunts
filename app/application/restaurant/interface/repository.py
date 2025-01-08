import abc
import uuid
from typing import Protocol

from app.application import dto
from app.application.restaurant.interface.reader import GetRestaurantsFilters
from app.domain import entity
from app.domain.common.pagination import Pagination


class RestaurantRepository(Protocol):
    @abc.abstractmethod
    async def get_restaurants(
        self, pagination: Pagination, filters: GetRestaurantsFilters
    ) -> dto.Restaurants:
        pass

    @abc.abstractmethod
    async def get_restaurant_by_id(self, restaurant_id: uuid.UUID) -> dto.Restaurant:
        pass

    @abc.abstractmethod
    async def get_restaurant_by_name(self, name: str) -> dto.Restaurant:
        pass

    @abc.abstractmethod
    async def create_restaurant(self, restaurant: entity.Restaurant) -> None:
        pass

    @abc.abstractmethod
    async def update_restaurant(self, restaurant: entity.Restaurant) -> None:
        pass
