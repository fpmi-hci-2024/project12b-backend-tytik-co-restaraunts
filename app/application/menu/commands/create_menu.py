import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import Command, CommandHandler, EventMediator

from app.application.menu.interface.repository import MenuRepository
from app.application.uow.common import UnitOfWork
from app.domain.entity.menu import MenuId, MenuLogoUrl, MenuRestaurantId, MenuName, Menu

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateMenu(Command[UUID]):
    menu_id: UUID
    name: str
    restaurant_id: UUID
    logo_url: str


class CreateMenuHandler(CommandHandler[CreateMenu, UUID]):
    def __init__(
        self,
        repo: MenuRepository,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self.repo = repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateMenu) -> UUID:
        menu_id = MenuId(command.menu_id)
        name = MenuName(command.name)
        restaurant_id = MenuRestaurantId(command.restaurant_id)
        logo_url = MenuLogoUrl(command.logo_url)
        is_deleted = False

        menu = Menu.create(menu_id, name, restaurant_id, logo_url, is_deleted)

        await self.repo.create_menu(menu)
        await self._uow.commit()

        logger.info("Menu created", extra={"menu": menu})

        return command.menu_id
