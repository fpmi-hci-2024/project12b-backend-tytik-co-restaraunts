from dataclasses import dataclass
from uuid import UUID

from app.application.exception import ApplicationError


@dataclass(eq=False)
class DishIdAlreadyExistsError(ApplicationError):
    dish_id: UUID

    @property
    def title(self) -> str:
        return f'A dish with the "{self.dish_id}" dish_id already exists'


@dataclass(eq=False)
class DishIdNotExistError(ApplicationError):
    dish_id: UUID

    @property
    def title(self) -> str:
        return f'A dish with "{self.dish_id}" dish_id doesn\'t exist'


@dataclass(eq=False)
class DishWithMenuIdNotExistError(ApplicationError):
    menu_id: UUID

    @property
    def title(self) -> str:
        return f'A dish with name "{self.menu_id}" menu_id doesn\'t exist'
