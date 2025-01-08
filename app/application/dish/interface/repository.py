import abc
import uuid
from typing import Protocol

from app.application.dish.interface.reader import GetDishesFilters
from app.domain.common.pagination import Pagination


class DishRepository(Protocol):
    @abc.abstractmethod
    async def get_dishes(
        self, pagination: Pagination, filters: GetDishesFilters
    ) -> dto.Menus:
        pass

    @abc.abstractmethod
    async def get_dish_by_id(self, dish_id: uuid.UUID) -> dto.Menu:
        pass

    @abc.abstractmethod
    async def get_dish_by_menu_id(self, menu_id: uuid.UUID) -> dto.Menu:
        pass

    @abc.abstractmethod
    async def create_menu(self, menu: entity.Menu) -> None:
        pass

    @abc.abstractmethod
    async def update_menu(self, menu: entity.Menu) -> None:
        pass
