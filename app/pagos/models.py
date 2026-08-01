from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False, unique=True)
    monto = Column(Numeric(10, 2), nullable=False)          # calculado por la API
    metodo = Column(String(20), nullable=False)             # efectivo, tarjeta, transferencia
    estado = Column(String(20), default="pagado", nullable=False)  # pagado, reembolsado
    fecha_pago = Column(DateTime, server_default=func.now(), nullable=False)

    # Relación: un pago pertenece a una reserva
    reserva = relationship("Reserva", back_populates="pago")
