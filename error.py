from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base for all app errors. Each subclass sets its own status_code."""
    status_code: int = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NoArticlesError(AppError):
    status_code = 404


class ProviderConfigError(AppError):
    status_code = 500


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )