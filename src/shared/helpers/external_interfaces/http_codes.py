from typing import Any

from src.shared.helpers.enum.http_status_code import HttpStatusCode
from src.shared.helpers.external_interfaces.http_models import HttpResponse

class OK(HttpResponse):
    def __init__(self, body: Any = None) -> None:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
        }

        super().__init__(HttpStatusCode.OK.value, body, headers=headers)

class Created(HttpResponse):
    def __init__(self, body: Any = None) -> None:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
        }

        super().__init__(HttpStatusCode.CREATED.value, body, headers=headers)

class NoContent(HttpResponse):
    def __init__(self) -> None:
        super().__init__(HttpStatusCode.NO_CONTENT.value, None)

class BadRequest(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCode.BAD_REQUEST.value, body)

class InternalServerError(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCode.INTERNAL_SERVER_ERROR.value, body)

class NotFound(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCode.NOT_FOUND.value, body)

class Conflict(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCode.CONFLICT.value, body)

class RedirectResponse(HttpResponse):
    def __init__(self, body: dict) -> None:
        super().__init__(HttpStatusCode.REDIRECT.value, None)
        self.location = body

class Forbidden(HttpResponse):
    def __init__(self, body: dict) -> None:
        super().__init__(HttpStatusCode.FORBIDDEN.value, body)
