from typing import ClassVar

from app.domain.common.exception import AppError


class ApplicationError(AppError):
    """Base Application Exception."""

    @property
    def title(self) -> str:
        return "An application error occurred"


class UnexpectedError(ApplicationError):
    pass


class RepoError(UnexpectedError):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass
