"""initial: canchas y reservas

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-25 12:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "canchas",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("nombre", sa.String(length=100), nullable=False, unique=True),
        sa.Column("tipo", sa.String(length=50), nullable=False),
        sa.Column("precio_hora", sa.Numeric(10, 2), nullable=False),
        sa.Column("disponible", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "reservas",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("cancha_id", sa.Integer(), sa.ForeignKey("canchas.id"), nullable=False),
        sa.Column("nombre_cliente", sa.String(length=120), nullable=False),
        sa.Column("email_cliente", sa.String(length=120), nullable=False),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column("hora_inicio", sa.Time(), nullable=False),
        sa.Column("hora_fin", sa.Time(), nullable=False),
        sa.Column("estado", sa.String(length=20), nullable=False, server_default="confirmada"),
    )


def downgrade() -> None:
    op.drop_table("reservas")
    op.drop_table("canchas")
