import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.canchas.routes import router as canchas_router
from app.errors import AppError, app_error_handler, validation_error_handler
from app.pagos.routes import router as pagos_router
from app.reservas.routes import router as reservas_router

# Descripciones de los módulos, para mejorar la documentación en /docs
tags_metadata = [
    {"name": "Canchas", "description": "Gestión de las canchas deportivas."},
    {"name": "Reservas", "description": "Reservas de canchas, con validación de horarios."},
    {"name": "Pagos", "description": "Pagos de las reservas. El monto se calcula automáticamente."},
]

app = FastAPI(
    title=os.getenv("APP_TITLE", "CanchApp API"),
    description=(
        "Sistema de Reservas de Canchas Deportivas.\n\n"
        "API REST construida con FastAPI, SQLAlchemy, Alembic, PostgreSQL y Docker. "
        "Gestiona canchas, reservas y pagos, con validaciones de negocio."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
)

# Manejo consistente de errores en toda la API
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)

app.include_router(canchas_router)
app.include_router(reservas_router)
app.include_router(pagos_router)


@app.get("/", tags=["default"])
def home():
    """Mensaje de bienvenida de la API."""
    return {"mensaje": "CanchApp API en funcionamiento. Visita /docs"}


@app.get("/health", tags=["default"])
def health_check():
    """Verifica que la API esté en funcionamiento (útil para Docker)."""
    return {"status": "ok"}
