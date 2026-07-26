from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import AppError

from . import models, schemas

router = APIRouter(prefix="/api/v1/canchas", tags=["Canchas"])


@router.post("/", response_model=schemas.CanchaOut, status_code=status.HTTP_201_CREATED)
def crear_cancha(data: schemas.CanchaCreate, db: Session = Depends(get_db)):
    """Registra una nueva cancha. Valida que el nombre no se repita."""
    existe = db.query(models.Cancha).filter(models.Cancha.nombre == data.nombre).first()
    if existe:
        raise AppError(400, f"La cancha '{data.nombre}' ya está registrada")
    cancha = models.Cancha(**data.model_dump())
    db.add(cancha)
    db.commit()
    db.refresh(cancha)
    return cancha


@router.get("/", response_model=list[schemas.CanchaOut])
def listar_canchas(
    tipo: str | None = None,
    disponible: bool | None = None,
    db: Session = Depends(get_db),
):
    """Lista canchas, con filtros opcionales por tipo y disponibilidad."""
    query = db.query(models.Cancha)
    if tipo is not None:
        query = query.filter(models.Cancha.tipo == tipo)
    if disponible is not None:
        query = query.filter(models.Cancha.disponible == disponible)
    return query.all()


@router.get("/{cancha_id}", response_model=schemas.CanchaOut)
def obtener_cancha(cancha_id: int, db: Session = Depends(get_db)):
    cancha = db.get(models.Cancha, cancha_id)
    if not cancha:
        raise AppError(404, "Cancha no encontrada")
    return cancha


@router.put("/{cancha_id}", response_model=schemas.CanchaOut)
def actualizar_cancha(
    cancha_id: int, data: schemas.CanchaUpdate, db: Session = Depends(get_db)
):
    cancha = db.get(models.Cancha, cancha_id)
    if not cancha:
        raise AppError(404, "Cancha no encontrada")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(cancha, campo, valor)
    db.commit()
    db.refresh(cancha)
    return cancha


@router.delete("/{cancha_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cancha(cancha_id: int, db: Session = Depends(get_db)):
    cancha = db.get(models.Cancha, cancha_id)
    if not cancha:
        raise AppError(404, "Cancha no encontrada")
    db.delete(cancha)
    db.commit()
