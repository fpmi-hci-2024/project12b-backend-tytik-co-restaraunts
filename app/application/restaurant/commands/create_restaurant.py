import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator, Command, CommandHandler

from app.application.restaurant.interface.repository import RestaurantRepository
from app.application.uow.common import UnitOfWork
from app.domain.entity import Restaurant
from app.domain.entity.restaurant import (
    RestaurantId,
    RestaurantName,
    RestaurantCuisineName,
    RestaurantLogoUrl,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateRestaurant(Command[UUID]):
    restaurant_id: UUID
    name: str
    cuisine_name: str
    logo_url: str


class CreateRestaurantHandler(CommandHandler[CreateRestaurant, UUID]):
    def __init__(
        self,
        repo: RestaurantRepository,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self.repo = repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateRestaurant) -> UUID:
        restaurant_id = RestaurantId(command.restaurant_id)
        name = RestaurantName(command.name)
        cuisine_name = RestaurantCuisineName(command.cuisine_name)
        logo_url = RestaurantLogoUrl(command.logo_url)
        is_deleted = False

        restaurant = Restaurant.create(
            restaurant_id, name, cuisine_name, logo_url, is_deleted
        )

        await self.repo.create_restaurant(restaurant)
        await self._uow.commit()

        logger.info("Restaurant created", extra={"restaurant": restaurant})

        return command.restaurant_id
