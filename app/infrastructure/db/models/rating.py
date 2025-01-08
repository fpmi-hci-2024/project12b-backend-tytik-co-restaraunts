import uuid
import sqlalchemy as sa
from sqlalchemy import String, UUID

from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.models.base import TimeBaseModel


class Rating(TimeBaseModel):
    __tablename__ = "rating"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=sa.func.uuid_generate_v4()
    )
    rating_value: Mapped[str] = mapped_column(String)
    restaurant_id: Mapped[uuid.UUID] = mapped_column(UUID)
    id_deleted: Mapped[bool] = mapped_column(default=False)
