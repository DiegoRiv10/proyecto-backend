"""agrega tabla pagos

Revision ID: 0002_pagos
Revises: 0001_initial
Create Date: 2026-08-01 12:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_pagos"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pagos",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "reserva_id", sa.Integer(),
            sa.ForeignKey("reservas.id"), nullable=False, unique=True,
        ),
        sa.Column("monto", sa.Numeric(10, 2), nullable=False),
        sa.Column("metodo", sa.String(length=20), nullable=False),
        sa.Column("estado", sa.String(length=20), nullable=False, server_default="pagado"),
        sa.Column(
            "fecha_pago", sa.DateTime(),
            server_default=sa.func.now(), nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("pagos")
