from typing import cast

from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, status_code: int, details: str):
        self._status_code = status_code
        self._details = details

    @property
    def status_code(self):
        return self._status_code

    @property
    def details(self):
        return self._details


class NotFoundException(AppException):
    def __init__(self, details: str | None = None):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            "Entity was not found" if details is None else details,
        )


class EntityAlreadyExistsException(AppException):
    def __init__(self, details: str | None = None):
        super().__init__(
            status.HTTP_409_CONFLICT,
            "Entity already exists" if details is None else details,
        )


def app_exception_handler(request: Request, exception: Exception):
    exc = cast(AppException, exception)
    return JSONResponse(status_code=exc.status_code, content={"details": exc.details})
