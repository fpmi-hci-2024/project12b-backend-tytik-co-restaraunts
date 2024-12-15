import datetime
from sqlalchemy import MetaData, sql
from sqlalchemy.orm import DeclarativeBase, registry
from sqlalchemy.orm import Mapped, mapped_column


mapper_registry = registry(metadata=MetaData())


class BaseModel(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata


class TimeBaseModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default=sql.func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        server_default=sql.func.now(),
        onupdate=sql.func.now(),
    )
