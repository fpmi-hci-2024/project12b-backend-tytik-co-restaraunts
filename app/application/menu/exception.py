from dataclasses import dataclass
from uuid import UUID

from app.application.exception import ApplicationError


@dataclass(eq=False)
class MenuIdAlreadyExistsError(ApplicationError):
    menu_id: UUID

    @property
    def title(self) -> str:
        return f'A menu with the "{self.menu_id}" menu_id already exists'


@dataclass(eq=False)
class MenuIdNotExistError(ApplicationError):
    menu_id: UUID

    @property
    def title(self) -> str:
        return f'A menu with "{self.menu_id}" menu_id doesn\'t exist'


@dataclass(eq=False)
class MenuWithRestaurantIdNotExistError(ApplicationError):
    restaurant_id: UUID

    @property
    def title(self) -> str:
        return f'A menu with name "{self.restaurant_id}" restaurant_id doesn\'t exist'
