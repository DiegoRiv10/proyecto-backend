from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.canchas import models as cancha_models
from app.database import get_db
from app.errors import AppError
from app.reservas import models as reserva_models

from . import models, schemas

router = APIRouter(prefix="/api/v1/pagos", tags=["Pagos"])

METODOS_VALIDOS = {"efectivo", "tarjeta", "transferencia"}


def _calcular_monto(db: Session, reserva) -> Decimal:
    """Regla de negocio: el monto se calcula automáticamente según las horas
    reservadas multiplicadas por el precio por hora de la cancha."""
    cancha = db.get(cancha_models.Cancha, reserva.cancha_id)
    inicio = datetime.combine(reserva.fecha, reserva.hora_inicio)
    fin = datetime.combine(reserva.fecha, reserva.hora_fin)
    horas = Decimal((fin - inicio).total_seconds()) / Decimal(3600)
    return (cancha.precio_hora * horas).quantize(Decimal("0.01"))


@router.post("/", response_model=schemas.PagoOut, status_code=status.HTTP_201_CREATED)
def crear_pago(data: schemas.PagoCreate, db: Session = Depends(get_db)):
    # Validación: el método debe ser uno de los permitidos
    if data.metodo not in METODOS_VALIDOS:
        raise AppError(
            400,
            f"Método de pago inválido. Usa uno de: {', '.join(sorted(METODOS_VALIDOS))}",
        )

    # Validación: la reserva debe existir
    reserva = db.get(reserva_models.Reserva, data.reserva_id)
    if not reserva:
        raise AppError(404, "La reserva indicada no existe")

    # Regla de negocio: no se puede pagar una reserva cancelada
    if reserva.estado == "cancelada":
        raise AppError(400, "No se puede pagar una reserva cancelada")

    # Regla de negocio: una reserva no puede pagarse dos veces
    ya_pagada = (
        db.query(models.Pago).filter(models.Pago.reserva_id == data.reserva_id).first()
    )
    if ya_pagada:
        raise AppError(400, "Esta reserva ya tiene un pago registrado")

    # El monto se calcula solo, no lo manda el cliente
    monto = _calcular_monto(db, reserva)

    pago = models.Pago(reserva_id=data.reserva_id, metodo=data.metodo, monto=monto)
    db.add(pago)
    db.commit()
    db.refresh(pago)
    return pago


@router.get("/", response_model=list[schemas.PagoOut])
def listar_pagos(
    metodo: str | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
):
    """Lista pagos, con filtros/búsqueda opcionales por método y por estado."""
    query = db.query(models.Pago)
    if metodo is not None:
        query = query.filter(models.Pago.metodo == metodo)
    if estado is not None:
        query = query.filter(models.Pago.estado == estado)
    return query.all()


@router.get("/{pago_id}", response_model=schemas.PagoOut)
def obtener_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = db.get(models.Pago, pago_id)
    if not pago:
        raise AppError(404, "Pago no encontrado")
    return pago


@router.patch("/{pago_id}", response_model=schemas.PagoOut)
def actualizar_pago(
    pago_id: int, data: schemas.PagoUpdate, db: Session = Depends(get_db)
):
    pago = db.get(models.Pago, pago_id)
    if not pago:
        raise AppError(404, "Pago no encontrado")
    if data.metodo is not None:
        if data.metodo not in METODOS_VALIDOS:
            raise AppError(400, "Método de pago inválido")
        pago.metodo = data.metodo
    if data.estado is not None:
        pago.estado = data.estado
    db.commit()
    db.refresh(pago)
    return pago


@router.delete("/{pago_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = db.get(models.Pago, pago_id)
    if not pago:
        raise AppError(404, "Pago no encontrado")
    db.delete(pago)
    db.commit()
