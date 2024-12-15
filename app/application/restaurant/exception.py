from dataclasses import dataclass
from uuid import UUID

from app.application.exception import ApplicationError


@dataclass(eq=False)
class RestaurantIdAlreadyExistsError(ApplicationError):
    restaurant_id: UUID

    @property
    def title(self) -> str:
        return f'A restaurant with the "{self.restaurant_id}" restaurant_id already exists'


@dataclass(eq=False)
class RestaurantIdNotExistError(ApplicationError):
    restaurant_id: UUID

    @property
    def title(self) -> str:
        return f'A restaurant with "{self.restaurant_id}" restaurant_id doesn\'t exist'


@dataclass(eq=False)
class RestaurantNameNotExistError(ApplicationError):
    name: str

    @property
    def title(self) -> str:
        return f'A restaurant with name "{self.name}" doesn\'t exist'


@dataclass(eq=False)
class RestaurantNameAlreadyExistsError(ApplicationError):
    name: str

    @property
    def title(self) -> str:
        return f'A restaurant with the name "{self.name}" already exists'
