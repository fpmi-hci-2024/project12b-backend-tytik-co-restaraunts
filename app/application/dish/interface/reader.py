from dataclasses import dataclass

from app.domain.common.constant import Empty


@dataclass(frozen=True)
class GetDishesFilters:
    deleted: bool | Empty = Empty.UNSET
