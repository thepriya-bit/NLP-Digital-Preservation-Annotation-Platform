"""Add is_banned column to users table

Revision ID: b3c6e8f1a2d4
Revises: a2f5c9d4e7b1
Create Date: 2026-07-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b3c6e8f1a2d4"
down_revision: Union[str, None] = "a2f5c9d4e7b1"
branch_labels: Union[Sequence[str], None] = None
depends_on: Union[Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_banned", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    op.alter_column("users", "is_banned", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "is_banned")
