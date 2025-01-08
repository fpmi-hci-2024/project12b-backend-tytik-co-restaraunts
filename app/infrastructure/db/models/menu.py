import uuid

import sqlalchemy as sa
from sqlalchemy import String, UUID
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.db.models.base import TimeBaseModel


class Menu(TimeBaseModel):
    __tablename__ = "menu"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=sa.func.uuid_generate_v4()
    )
    name: Mapped[str] = mapped_column(String)
    restaurant_id: Mapped[uuid.UUID] = mapped_column(UUID)
    id_deleted: Mapped[bool] = mapped_column(default=False)
