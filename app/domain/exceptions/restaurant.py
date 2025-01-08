from dataclasses import dataclass
from uuid import UUID

from app.domain.common.exception import DomainError


@dataclass(eq=False)
class RestaurantIsDeletedError(DomainError):
    restaurant_id: UUID

    @property
    def title(self) -> str:
        return f'The restaurant with "{self.restaurant_id}" restaurant_id is deleted'


@dataclass(eq=False)
class RestaurantAlreadyExistsError(DomainError):
    name: str | None = None

    @property
    def title(self) -> str:
        if self.name is None:
            return "A restaurant with the name already exists"
        return f'A restaurant with the "{self.name}" name already exists'
