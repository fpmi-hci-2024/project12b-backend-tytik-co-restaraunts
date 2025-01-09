import uuid
from typing import Iterable

from sqlalchemy import select, func
from sqlalchemy.exc import DBAPIError, IntegrityError

from app.application import dto
from app.application.dish.exception import (
    DishIdNotExistError,
    DishWithMenuIdNotExistError,
    DishIdAlreadyExistsError,
)
from app.application.dish.interface.reader import GetDishesFilters
from app.application.dish.interface.repository import DishRepository
from app.application.exception import RepoError
from app.domain import entity
from app.domain.common.constant import SortOrder, Empty
from app.domain.common.pagination import Pagination, PaginationResult
from app.infrastructure.db.exception_wrapper import exception_mapper
from app.infrastructure.db.mappers.dish.convert_db_dish_to_dto import (
    convert_db_event_model_to_dto,
)
from app.infrastructure.db.mappers.dish.convert_dish_dto_to_db_model import (
    convert_dish_dto_to_db_model,
)
from app.infrastructure.db.models import Dish
from app.infrastructure.db.repository.base import SqlAlchemyRepository


class DishRepositoryImpl(SqlAlchemyRepository, DishRepository):
    @exception_mapper
    async def get_dishes(
        self,
        pagination: Pagination,
        filters: GetDishesFilters,
        menu_id: uuid.UUID | None = None,
    ) -> dto.Dishes:
        if menu_id:
            query = select(Dish).where(Dish.menu_id == menu_id)
        else:
            query = select(Dish)
        if pagination.order is SortOrder.ASC:
            query = query.order_by(Dish.id.desc())
        else:
            query = query.order_by(Dish.id.asc())

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(Dish.is_deleted.is_not(False))
            else:
                query = query.where(Dish.is_deleted.is_(False))

        if pagination.offset is not Empty.UNSET:
            query = query.offset(pagination.offset)
        if pagination.limit is not Empty.UNSET:
            query = query.limit(pagination.limit)

        res: Iterable[Dish] = await self.session.scalars(query)
        dishes = [convert_db_event_model_to_dto(dish) for dish in res]
        groups_count = await self._get_dishes_count(filters)
        return dto.Dishes(
            data=dishes,
            pagination=PaginationResult.from_pagination(pagination, total=groups_count),
        )

    @exception_mapper
    async def get_dish_by_id(self, dish_id: uuid.UUID) -> dto.Dish:
        dish: Dish | None = await self.session.get(Dish, dish_id)

        if dish is None:
            raise DishIdNotExistError(dish_id)

        return convert_db_event_model_to_dto(dish)

    @exception_mapper
    async def get_dish_by_menu_id(
        self, menu_id: uuid.UUID, pagination: Pagination, filters: GetDishesFilters
    ) -> dto.Dishes:
        return await self.get_dishes(
            pagination=pagination, filters=filters, menu_id=menu_id
        )

    @exception_mapper
    async def create_dish(self, dish: entity.Dish) -> None:
        db_dish = convert_dish_dto_to_db_model(dish)
        self.session.add(db_dish)
        try:
            await self.session.flush((db_dish,))
        except IntegrityError as err:
            self._parse_error(err, dish)

    @exception_mapper
    async def update_dish(self, dish: entity.Dish) -> None:
        db_dish = convert_dish_dto_to_db_model(dish)
        try:
            await self.session.merge(db_dish)
        except IntegrityError as err:
            self._parse_error(err, dish)

    async def _get_dishes_count(self, filters: GetDishesFilters) -> int:
        query = select(func.count(Dish.id))

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(Dish.is_deleted.is_not(False))
            else:
                query = query.where(Dish.is_deleted.is_(False))

        dishes_count: int = await self.session.scalar(query)
        return dishes_count

    def _parse_error(self, err: DBAPIError, dish: entity.Dish) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "dish_pkey":
                raise DishIdAlreadyExistsError(dish.id.to_raw()) from err
            case _:
                raise RepoError from err
