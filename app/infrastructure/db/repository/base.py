from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyRepository(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
