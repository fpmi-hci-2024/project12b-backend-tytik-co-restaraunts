from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from uuid import uuid4


async def set_request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request.state.request_id = uuid4()
    response = await call_next(request)
    return response
