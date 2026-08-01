import os

from fastapi import FastAPI

from app.canchas.routes import router as canchas_router
from app.errors import AppError, app_error_handler
from app.pagos.routes import router as pagos_router
from app.reservas.routes import router as reservas_router

app = FastAPI(
    title=os.getenv("APP_TITLE", "CanchApp API"),
    description="Sistema de Reservas de Canchas Deportivas — API REST con FastAPI.",
    version="1.0.0",
)

app.add_exception_handler(AppError, app_error_handler)

app.include_router(canchas_router)
app.include_router(reservas_router)
app.include_router(pagos_router)


@app.get("/", tags=["default"])
def home():
    return {"mensaje": "CanchApp API en funcionamiento. Visita /docs"}
