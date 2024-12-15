from dataclasses import dataclass
from typing import Generic, TypeVar

Item = TypeVar("Item")


@dataclass(frozen=True)
class ListItemsDTO(Generic[Item]):
    data: list[Item]
