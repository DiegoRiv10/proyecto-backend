from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CanchaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, examples=["Cancha 1"])
    tipo: str = Field(..., min_length=1, max_length=50, examples=["futbol"])
    precio_hora: Decimal = Field(..., gt=0, examples=[350.00])
    disponible: bool = True


class CanchaCreate(CanchaBase):
    pass


class CanchaUpdate(BaseModel):
    """Todos opcionales: sirve para PUT y PATCH."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)
    precio_hora: Optional[Decimal] = Field(None, gt=0)
    disponible: Optional[bool] = None


class CanchaOut(CanchaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
