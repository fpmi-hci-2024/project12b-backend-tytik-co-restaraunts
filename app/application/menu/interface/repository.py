import abc
import uuid
from typing import Protocol

from app.application import dto
from app.application.menu.interface.reader import GetMenusFilters
from app.domain import entity
from app.domain.common.pagination import Pagination


class MenuRepository(Protocol):
    @abc.abstractmethod
    async def get_menus(
        self, pagination: Pagination, filters: GetMenusFilters
    ) -> dto.Menus:
        pass

    @abc.abstractmethod
    async def get_menu_by_id(self, menu_id: uuid.UUID) -> dto.Menu:
        pass

    @abc.abstractmethod
    async def get_menu_by_restaurant_id(self, restaurant_id: uuid.UUID) -> dto.Menu:
        pass

    @abc.abstractmethod
    async def create_menu(self, menu: entity.Menu) -> None:
        pass

    @abc.abstractmethod
    async def update_menu(self, menu: entity.Menu) -> None:
        pass
