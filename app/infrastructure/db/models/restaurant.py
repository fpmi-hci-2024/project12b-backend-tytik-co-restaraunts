import uuid

import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.db.models.base import TimeBaseModel


class Restaurant(TimeBaseModel):
    __tablename__ = "restaurant"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=sa.func.uuid_generate_v4()
    )
    name: Mapped[str] = mapped_column(String, unique=True)
    cuisine_name: Mapped[str] = mapped_column(String)
    logo_url: Mapped[str] = mapped_column(String, default="")
    is_deleted: Mapped[bool] = mapped_column(default=False)
