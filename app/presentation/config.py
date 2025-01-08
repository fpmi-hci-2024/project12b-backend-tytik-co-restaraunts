from dataclasses import dataclass, field

from di import bind_by_type
from di.dependent import Dependent
from didiator.interface.utils.di_builder import DiBuilder

from app.infrastructure.db.config import DBConfig


@dataclass
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = __debug__


@dataclass
class Config:
    db: DBConfig = field(default_factory=DBConfig)
    api: APIConfig = field(default_factory=APIConfig)


def setup_di_builder_config(di_builder: DiBuilder, config: Config) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: config, scope="app"), Config))
    di_builder.bind(
        bind_by_type(Dependent(lambda *args: config.db, scope="app"), DBConfig)
    )
    di_builder.bind(
        bind_by_type(Dependent(lambda *args: config.api, scope="app"), APIConfig)
    )
