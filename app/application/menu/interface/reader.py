from dataclasses import dataclass

from app.domain.common.constant import Empty


@dataclass(frozen=True)
class GetMenusFilters:
    deleted: bool | Empty = Empty.UNSET
