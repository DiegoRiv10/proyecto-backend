from datetime import date, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ReservaBase(BaseModel):
    cancha_id: int = Field(..., examples=[1])
    nombre_cliente: str = Field(..., min_length=1, max_length=120, examples=["Diego Rivera"])
    email_cliente: EmailStr = Field(..., examples=["diego@example.com"])
    fecha: date = Field(..., examples=["2026-07-25"])
    hora_inicio: time = Field(..., examples=["18:00"])
    hora_fin: time = Field(..., examples=["19:00"])
    estado: str = Field("confirmada", examples=["confirmada"])


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    nombre_cliente: Optional[str] = Field(None, min_length=1, max_length=120)
    email_cliente: Optional[EmailStr] = None
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    estado: Optional[str] = None


class ReservaOut(ReservaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
