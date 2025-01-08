import datetime
import decimal
import uuid

import sqlalchemy as sa
from sqlalchemy import String, UUID, Date, Numeric
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.db.models.base import TimeBaseModel


class Order(TimeBaseModel):
    __tablename__ = "order"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=sa.func.uuid_generate_v4()
    )
    # client_name: str
    # phone: str
    # address: str
    # comment
    order_name: Mapped[str] = mapped_column(String)
    creation_date: Mapped[datetime.datetime] = mapped_column(Date)
    delivery_date: Mapped[datetime.datetime | None] = mapped_column(Date, default=None)
    status: Mapped[str] = mapped_column(String)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric)
    is_deleted: Mapped[bool] = mapped_column(default=False)
