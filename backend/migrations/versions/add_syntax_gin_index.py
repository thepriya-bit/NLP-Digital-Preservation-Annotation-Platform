"""Add GIN index for annotation syntax JSONB

Revision ID: a2f5c9d4e7b1
Revises: 1229a9b732b1
Create Date: 2026-07-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a2f5c9d4e7b1"
down_revision: Union[str, None] = "1229a9b732b1"
branch_labels: Union[Sequence[str], None] = None
depends_on: Union[Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_annotations_syntax_gin",
        "annotations",
        ["syntax"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index("ix_annotations_syntax_gin", table_name="annotations")
