import decimal
import uuid

import sqlalchemy as sa
from sqlalchemy import String, Numeric, UUID
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.db.models.base import TimeBaseModel


class Dish(TimeBaseModel):
    __tablename__ = "dish"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=sa.func.uuid_generate_v4()
    )
    name: Mapped[str] = mapped_column(String)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric)
    menu_id: Mapped[uuid.UUID] = mapped_column(UUID)
    id_deleted: Mapped[bool] = mapped_column(default=False)
