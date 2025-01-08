from typing import Sequence

from app.application.uow.common import UnitOfWork
from app.infrastructure.db.common.uow import SQLAlchemyUoW


def build_uow(db_uow: SQLAlchemyUoW) -> UnitOfWork:
    uow = UnitOfWorkImpl((db_uow,))
    return uow


class UnitOfWorkImpl(UnitOfWork):
    def __init__(self, uows: Sequence[UnitOfWork]) -> None:
        self._uows = uows

    async def commit(self) -> None:
        for uow in self._uows:
            await uow.commit()

    async def rollback(self) -> None:
        for uow in self._uows:
            await uow.rollback()
