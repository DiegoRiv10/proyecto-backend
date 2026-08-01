from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PagoCreate(BaseModel):
    """Para crear un pago solo se indica la reserva y el método.
    El monto lo calcula la API (regla de negocio), no lo manda el cliente."""
    reserva_id: int = Field(..., examples=[1])
    metodo: str = Field(..., examples=["tarjeta"])


class PagoUpdate(BaseModel):
    metodo: Optional[str] = None
    estado: Optional[str] = None


class PagoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    reserva_id: int
    monto: Decimal
    metodo: str
    estado: str
    fecha_pago: datetime
