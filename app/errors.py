from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Error de negocio controlado, con código HTTP y mensaje claro."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.message},
    )
