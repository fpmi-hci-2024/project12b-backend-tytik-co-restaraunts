import uuid
from typing import Iterable

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError, DBAPIError

from app.application import dto
from app.application.exception import RepoError
from app.application.menu.exception import (
    MenuIdAlreadyExistsError,
    MenuIdNotExistError,
    MenuWithRestaurantIdNotExistError,
)
from app.application.menu.interface.reader import GetMenusFilters
from app.application.menu.interface.repository import MenuRepository
from app.domain import entity
from app.domain.common.constant import SortOrder, Empty
from app.domain.common.pagination import Pagination, PaginationResult
from app.infrastructure.db.exception_wrapper import exception_mapper
from app.infrastructure.db.mappers.menu.convert_db_menu_to_dto import (
    convert_db_event_model_to_dto,
)
from app.infrastructure.db.mappers.menu.convert_menu_dto_to_db_model import (
    convert_menu_dto_to_db_model,
)
from app.infrastructure.db.models import Menu
from app.infrastructure.db.repository.base import SqlAlchemyRepository


class MenuRepositoryImpl(SqlAlchemyRepository, MenuRepository):
    @exception_mapper
    async def get_menus(
        self, pagination: Pagination, filters: GetMenusFilters
    ) -> dto.Menus:
        query = select(Menu)
        if pagination.order is SortOrder.ASC:
            query = query.order_by(Menu.id.desc())
        else:
            query = query.order_by(Menu.id.asc())

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(Menu.is_deleted.is_not(False))
            else:
                query = query.where(Menu.is_deleted.is_(False))

        if pagination.offset is not Empty.UNSET:
            query = query.offset(pagination.offset)
        if pagination.limit is not Empty.UNSET:
            query = query.limit(pagination.limit)

        res: Iterable[Menu] = await self.session.scalars(query)
        menus = [convert_db_event_model_to_dto(menu) for menu in res]
        groups_count = await self._get_menus_count(filters)
        return dto.Menus(
            data=menus,
            pagination=PaginationResult.from_pagination(pagination, total=groups_count),
        )

    @exception_mapper
    async def get_menu_by_id(self, menu_id: uuid.UUID) -> dto.Menu:
        menu: Menu | None = await self.session.get(Menu, menu_id)

        if menu is None:
            raise MenuIdNotExistError(menu_id)

        return convert_db_event_model_to_dto(menu)

    @exception_mapper
    async def get_menu_by_restaurant_id(self, restaurant_id: uuid.UUID) -> dto.Menu:
        menu: Menu | None = await self.session.scalar(
            select(Menu).where(Menu.restaurant_id == restaurant_id)
        )

        if menu is None:
            raise MenuWithRestaurantIdNotExistError(restaurant_id)
        print("^^", menu)
        return convert_db_event_model_to_dto(menu)

    @exception_mapper
    async def create_menu(self, menu: entity.Menu) -> None:
        db_menu = convert_menu_dto_to_db_model(menu)
        self.session.add(db_menu)
        try:
            await self.session.flush((db_menu,))
        except IntegrityError as err:
            self._parse_error(err, menu)

    @exception_mapper
    async def update_menu(self, menu: entity.Menu) -> None:
        db_menu = convert_menu_dto_to_db_model(menu)
        try:
            await self.session.merge(db_menu)
        except IntegrityError as err:
            self._parse_error(err, menu)

    async def _get_menus_count(self, filters: GetMenusFilters) -> int:
        query = select(func.count(Menu.id))

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(Menu.is_deleted.is_not(False))
            else:
                query = query.where(Menu.is_deleted.is_(False))

        menus_count: int = await self.session.scalar(query)
        return menus_count

    def _parse_error(self, err: DBAPIError, menu: entity.Menu) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "menu_pkey":
                raise MenuIdAlreadyExistsError(menu.id.to_raw()) from err
            case _:
                raise RepoError from err
