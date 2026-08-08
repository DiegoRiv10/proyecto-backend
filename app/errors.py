from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Error de negocio controlado, con código HTTP y mensaje claro."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


async def app_error_handler(request: Request, exc: AppError):
    """Maneja los errores de negocio con un formato consistente."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.message},
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Unifica los errores de validación de Pydantic al mismo formato
    que el resto de la API (success: false + mensaje claro)."""
    errores = exc.errors()
    if errores:
        primer = errores[0]
        campo = primer.get("loc", ["campo"])[-1]
        detalle = primer.get("msg", "dato inválido")
        mensaje = f"Dato inválido en '{campo}': {detalle}"
    else:
        mensaje = "Datos de entrada inválidos"
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": mensaje},
    )
