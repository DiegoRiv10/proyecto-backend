from sqlalchemy import Boolean, Column, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Cancha(Base):
    __tablename__ = "canchas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    tipo = Column(String(50), nullable=False)          # futbol, basquet, tenis...
    precio_hora = Column(Numeric(10, 2), nullable=False)
    disponible = Column(Boolean, default=True, nullable=False)

    reservas = relationship(
        "Reserva", back_populates="cancha", cascade="all, delete-orphan"
    )
