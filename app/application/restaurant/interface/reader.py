from dataclasses import dataclass

from app.domain.common.constant import Empty


@dataclass(frozen=True)
class GetRestaurantsFilters:
    deleted: bool | Empty = Empty.UNSET
