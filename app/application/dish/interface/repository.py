import abc
import uuid
from typing import Protocol

from app.application import dto
from app.application.dish.interface.reader import GetDishesFilters
from app.domain import entity
from app.domain.common.pagination import Pagination


class DishRepository(Protocol):
    @abc.abstractmethod
    async def get_dishes(
        self, pagination: Pagination, filters: GetDishesFilters
    ) -> dto.Dishes:
        pass

    @abc.abstractmethod
    async def get_dish_by_id(self, dish_id: uuid.UUID) -> dto.Dish:
        pass

    @abc.abstractmethod
    async def get_dish_by_menu_id(
        self,
        menu_id: uuid.UUID,
        pagination: Pagination,
        filters: GetDishesFilters
    ) -> dto.Dishes:
        pass

    @abc.abstractmethod
    async def create_dish(self, dish: entity.Dish) -> None:
        pass

    @abc.abstractmethod
    async def update_dish(self, dish: entity.Dish) -> None:
        pass
