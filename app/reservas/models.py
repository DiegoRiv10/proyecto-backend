from sqlalchemy import (
    Column, Date, ForeignKey, Integer, String, Time
)
from sqlalchemy.orm import relationship

from app.database import Base


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    cancha_id = Column(Integer, ForeignKey("canchas.id"), nullable=False)
    nombre_cliente = Column(String(120), nullable=False)
    email_cliente = Column(String(120), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado = Column(String(20), default="confirmada", nullable=False)

    cancha = relationship("Cancha", back_populates="reservas")
    pago = relationship(
        "Pago", back_populates="reserva", uselist=False,
        cascade="all, delete-orphan",
    )
