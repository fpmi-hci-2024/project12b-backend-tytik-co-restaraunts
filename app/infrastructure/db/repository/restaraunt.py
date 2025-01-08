import uuid
from typing import Iterable

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError, DBAPIError, SQLAlchemyError

from app.application import dto
from app.application.exception import RepoError
from app.application.restaurant.exception import (
    RestaurantIdNotExistError,
    RestaurantNameNotExistError,
    RestaurantIdAlreadyExistsError,
    RestaurantNameAlreadyExistsError,
)
from app.application.restaurant.interface.reader import GetRestaurantsFilters
from app.application.restaurant.interface.repository import RestaurantRepository
from app.domain import entity
from app.domain.common.constant import SortOrder, Empty
from app.domain.common.pagination import PaginationResult, Pagination
from app.infrastructure.db.exception_wrapper import exception_mapper
from app.infrastructure.db.mappers.restaurant.convert_db_restaurant_to_dto import (
    convert_db_event_model_to_dto,
)
from app.infrastructure.db.mappers.restaurant.convert_restaurant_entity_to_db import (
    convert_restaurant_dto_to_db_model,
)
from app.infrastructure.db.models.restaurant import Restaurant
from app.infrastructure.db.repository.base import SqlAlchemyRepository


class RestaurantRepositoryImpl(SqlAlchemyRepository, RestaurantRepository):
    @exception_mapper
    async def get_restaurants(
        self, pagination: Pagination, filters: GetRestaurantsFilters
    ) -> dto.Restaurants:
        query = select(Restaurant)
        if pagination.order is SortOrder.ASC:
            query = query.order_by(Restaurant.id.desc())
        else:
            query = query.order_by(Restaurant.id.asc())

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(Restaurant.is_deleted.is_not(False))
            else:
                query = query.where(Restaurant.is_deleted.is_(False))

        if pagination.offset is not Empty.UNSET:
            query = query.offset(pagination.offset)
        if pagination.limit is not Empty.UNSET:
            query = query.limit(pagination.limit)

        res: Iterable[Restaurant] = await self.session.scalars(query)
        restaurants = [convert_db_event_model_to_dto(restaurant) for restaurant in res]
        groups_count = await self._get_restaurants_count(filters)
        return dto.Restaurants(
            data=restaurants,
            pagination=PaginationResult.from_pagination(pagination, total=groups_count),
        )

    @exception_mapper
    async def get_restaurant_by_id(self, restaurant_id: uuid.UUID) -> dto.Restaurant:
        restaurant: Restaurant | None = await self.session.get(
            Restaurant, restaurant_id
        )

        if restaurant is None:
            raise RestaurantIdNotExistError(restaurant_id)

        return convert_db_event_model_to_dto(restaurant)

    @exception_mapper
    async def get_restaurant_by_name(self, name: str) -> dto.Restaurant:
        restaurant: Restaurant | None = await self.session.scalar(
            select(Restaurant).where(Restaurant.name == name)
        )
        if restaurant is None:
            raise RestaurantNameNotExistError(name)

        return convert_db_event_model_to_dto(restaurant)

    @exception_mapper
    async def create_restaurant(self, restaurant: entity.Restaurant) -> None:
        db_restaurant = convert_restaurant_dto_to_db_model(restaurant)
        self.session.add(db_restaurant)
        try:
            await self.session.flush((db_restaurant,))
        except IntegrityError as err:
            self._parse_error(err, restaurant)

    @exception_mapper
    async def update_restaurant(self, restaurant: entity.Restaurant) -> None:
        db_restaurant = convert_restaurant_dto_to_db_model(restaurant)
        try:
            await self.session.merge(db_restaurant)
        except IntegrityError as err:
            self._parse_error(err, restaurant)

    async def _get_restaurants_count(self, filters: GetRestaurantsFilters) -> int:
        query = select(func.count(Restaurant.id))

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(Restaurant.is_deleted.is_not(False))
            else:
                query = query.where(Restaurant.is_deleted.is_(False))

        restaurants_count: int = await self.session.scalar(query)
        return restaurants_count

    def _parse_error(self, err: DBAPIError, restaurant: entity.Restaurant) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "restaurant_pkey":
                raise RestaurantIdAlreadyExistsError(restaurant.id.to_raw()) from err
            case "restaurant_name_key":
                raise RestaurantNameAlreadyExistsError(str(restaurant.name)) from err
            case _:
                raise RepoError from err
