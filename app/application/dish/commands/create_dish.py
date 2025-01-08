import decimal
import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import Command, CommandHandler, EventMediator

from app.application.dish.interface.repository import DishRepository
from app.application.uow.common import UnitOfWork
from app.domain.entity.dish import (
    DishId,
    DishName,
    DishPrice,
    DishMenuId,
    DishLogoUrl,
    DishType,
    DishIngredients,
    Dish,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateDish(Command[UUID]):
    id: UUID
    name: str
    price: decimal.Decimal
    menu_id: UUID
    logo_url: str
    dishes_type: str
    ingredients: str


class CreateDishHandler(CommandHandler[CreateDish, UUID]):
    def __init__(
        self,
        repo: DishRepository,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self.repo = repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateDish) -> UUID:
        id = DishId(command.id)
        name = DishName(command.name)
        price = DishPrice(command.price)
        menu_id = DishMenuId(command.menu_id)
        logo_url = DishLogoUrl(command.logo_url)
        dishes_type = DishType(command.dishes_type)
        ingredients = DishIngredients(command.ingredients)
        is_deleted = False

        dish = Dish.create(
            id, name, price, menu_id, logo_url, dishes_type, ingredients, is_deleted
        )

        await self.repo.create_dish(dish)
        await self._uow.commit()

        logger.info("Dish created", extra={"dish": dish})

        return command.id
