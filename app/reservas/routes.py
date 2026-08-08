from fastapi import APIRouter, Depends, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.canchas import models as cancha_models
from app.database import get_db
from app.errors import AppError

from . import models, schemas

router = APIRouter(prefix="/api/v1/reservas", tags=["Reservas"])

ESTADOS_VALIDOS = {"confirmada", "cancelada", "completada"}


def _validar_reserva(db: Session, data, reserva_id: int | None = None):
    """Valida que la cancha exista y esté disponible, que las horas tengan
    sentido, que el estado sea válido y que no haya empalme con otra reserva
    activa de la misma cancha."""
    cancha = db.get(cancha_models.Cancha, data.cancha_id)
    if not cancha:
        raise AppError(404, "La cancha indicada no existe")

    # Regla de negocio: no se puede reservar una cancha no disponible
    if not cancha.disponible:
        raise AppError(400, "La cancha no está disponible para reservar")

    # Validación: el estado debe ser uno de los permitidos
    if data.estado not in ESTADOS_VALIDOS:
        raise AppError(
            400,
            f"Estado inválido. Usa uno de: {', '.join(sorted(ESTADOS_VALIDOS))}",
        )

    if data.hora_fin <= data.hora_inicio:
        raise AppError(400, "La hora de fin debe ser posterior a la hora de inicio")

    # Buscar empalmes: misma cancha, misma fecha, horarios que se cruzan
    query = db.query(models.Reserva).filter(
        and_(
            models.Reserva.cancha_id == data.cancha_id,
            models.Reserva.fecha == data.fecha,
            models.Reserva.estado != "cancelada",
            models.Reserva.hora_inicio < data.hora_fin,
            models.Reserva.hora_fin > data.hora_inicio,
        )
    )
    if reserva_id is not None:
        query = query.filter(models.Reserva.id != reserva_id)
    if query.first():
        raise AppError(400, "La cancha ya tiene una reserva en ese horario")


@router.post("/", response_model=schemas.ReservaOut, status_code=status.HTTP_201_CREATED)
def crear_reserva(data: schemas.ReservaCreate, db: Session = Depends(get_db)):
    _validar_reserva(db, data)
    reserva = models.Reserva(**data.model_dump())
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


@router.get("/", response_model=list[schemas.ReservaOut])
def listar_reservas(
    cancha_id: int | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
):
    """Lista reservas, con filtros opcionales por cancha y por estado."""
    query = db.query(models.Reserva)
    if cancha_id is not None:
        query = query.filter(models.Reserva.cancha_id == cancha_id)
    if estado is not None:
        query = query.filter(models.Reserva.estado == estado)
    return query.all()


@router.get("/{reserva_id}", response_model=schemas.ReservaOut)
def obtener_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.get(models.Reserva, reserva_id)
    if not reserva:
        raise AppError(404, "Reserva no encontrada")
    return reserva


@router.put("/{reserva_id}", response_model=schemas.ReservaOut)
def actualizar_reserva(
    reserva_id: int, data: schemas.ReservaCreate, db: Session = Depends(get_db)
):
    reserva = db.get(models.Reserva, reserva_id)
    if not reserva:
        raise AppError(404, "Reserva no encontrada")
    _validar_reserva(db, data, reserva_id=reserva_id)
    for campo, valor in data.model_dump().items():
        setattr(reserva, campo, valor)
    db.commit()
    db.refresh(reserva)
    return reserva


@router.patch("/{reserva_id}", response_model=schemas.ReservaOut)
def actualizar_estado_reserva(
    reserva_id: int, data: schemas.ReservaUpdate, db: Session = Depends(get_db)
):
    reserva = db.get(models.Reserva, reserva_id)
    if not reserva:
        raise AppError(404, "Reserva no encontrada")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(reserva, campo, valor)
    db.commit()
    db.refresh(reserva)
    return reserva


@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.get(models.Reserva, reserva_id)
    if not reserva:
        raise AppError(404, "Reserva no encontrada")
    db.delete(reserva)
    db.commit()
