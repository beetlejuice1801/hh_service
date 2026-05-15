"""изменил в модели вакансии work_format на schedule

Revision ID: 4b37a9059558
Revises: 833a2f2398db
Create Date: 2026-05-15 14:46:09.681321

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4b37a9059558"
down_revision: Union[str, Sequence[str], None] = "833a2f2398db"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("vacancies", sa.Column("schedule", sa.String(), nullable=False))
    op.drop_column("vacancies", "work_format")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "vacancies",
        sa.Column("work_format", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("vacancies", "schedule")
