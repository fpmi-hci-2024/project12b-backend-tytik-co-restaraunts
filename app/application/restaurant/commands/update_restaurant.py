import logging
from dataclasses import dataclass

from uuid import UUID
from didiator import Command, CommandHandler, EventMediator

from app.application import dto
from app.application.restaurant.interface.repository import RestaurantRepository
from app.application.uow.common import UnitOfWork
from app.domain.entity.restaurant import RestaurantName, RestaurantCuisineName
from app.infrastructure.db.mappers.restaurant.convert_db_restaurant_to_entity import (
    convert_db_event_model_to_entity,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetRestaurantName(Command[dto.Restaurant]):
    restaurant_id: UUID
    name: str


class SetRestaurantNameHandler(CommandHandler[SetRestaurantName, None]):
    def __init__(
        self,
        user_repo: RestaurantRepository,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self.repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetRestaurantName) -> dto.Restaurant:
        restaurant = await self.repo.get_restaurant_by_id(command.restaurant_id)
        entity_restaurant = convert_db_event_model_to_entity(restaurant)
        entity_restaurant.set_name(RestaurantName(command.name))
        await self.repo.update_restaurant(entity_restaurant)

        await self._uow.commit()
        restaurant = await self.repo.get_restaurant_by_id(command.restaurant_id)

        logger.info("Restaurant deleted", extra={"restaurant": restaurant})
        return restaurant


@dataclass(frozen=True)
class SetCuisineName(Command[dto.Restaurant]):
    restaurant_id: UUID
    cuisine_name: str


class SetRestaurantCuisineNameHandler(CommandHandler[SetCuisineName, None]):
    def __init__(
        self,
        user_repo: RestaurantRepository,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self.repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetCuisineName) -> dto.Restaurant:
        restaurant = await self.repo.get_restaurant_by_id(command.restaurant_id)
        entity_restaurant = convert_db_event_model_to_entity(restaurant)
        entity_restaurant.set_name(RestaurantCuisineName(command.cuisine_name))
        await self.repo.update_restaurant(entity_restaurant)

        await self._uow.commit()
        restaurant = await self.repo.get_restaurant_by_id(command.restaurant_id)

        logger.info("Restaurant deleted", extra={"restaurant": restaurant})
        return restaurant
