"""удалил колонку schedule

Revision ID: b0d447c8d64e
Revises: 6953779fd2e7
Create Date: 2026-05-15 20:06:23.926045

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b0d447c8d64e"
down_revision: Union[str, Sequence[str], None] = "6953779fd2e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "vacancies", sa.Column("snippet_requirement", sa.String(), nullable=True)
    )
    op.add_column(
        "vacancies", sa.Column("snippet_responsibility", sa.String(), nullable=True)
    )
    op.alter_column(
        "vacancies",
        "first_seen_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "vacancies",
        "last_updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.drop_column("vacancies", "schedule")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "vacancies",
        sa.Column("schedule", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.alter_column(
        "vacancies",
        "last_updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.alter_column(
        "vacancies",
        "first_seen_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.drop_column("vacancies", "snippet_responsibility")
    op.drop_column("vacancies", "snippet_requirement")
