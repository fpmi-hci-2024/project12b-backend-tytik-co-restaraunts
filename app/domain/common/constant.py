from dataclasses import dataclass
from enum import Enum


class Empty(Enum):
    UNSET = "UNSET"


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"
