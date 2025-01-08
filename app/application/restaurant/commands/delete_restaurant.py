import logging
from dataclasses import dataclass

from uuid import UUID

from didiator import EventMediator, CommandHandler, Command

from app.application import dto
from app.application.restaurant.interface.repository import RestaurantRepository
from app.application.uow.common import UnitOfWork
from app.infrastructure.db.mappers.restaurant.convert_db_restaurant_to_entity import (
    convert_db_event_model_to_entity,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeleteRestaurant(Command[None]):
    restaurant_id: UUID


class DeleteRestaurantHandler(CommandHandler[DeleteRestaurant, None]):
    def __init__(
        self,
        repo: RestaurantRepository,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self.repo = repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: DeleteRestaurant) -> dto.Restaurant:
        restaurant = await self.repo.get_restaurant_by_id(command.restaurant_id)
        entity_restaurant = convert_db_event_model_to_entity(restaurant)
        entity_restaurant.delete()

        await self.repo.update_restaurant(entity_restaurant)

        await self._uow.commit()
        restaurant = await self.repo.get_restaurant_by_id(command.restaurant_id)

        logger.info("Restaurant deleted", extra={"restaurant": restaurant})
        return restaurant
