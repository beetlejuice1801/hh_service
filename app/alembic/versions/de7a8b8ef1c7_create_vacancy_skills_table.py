"""create vacancy_skills table

Revision ID: de7a8b8ef1c7
Revises: d91cabcf7d1f
Create Date: 2026-04-28 17:09:23.522374

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "de7a8b8ef1c7"
down_revision: Union[str, Sequence[str], None] = "d91cabcf7d1f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vacancy_skills",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("vacancy_id", sa.String(), nullable=False),
        sa.Column("skill_name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["vacancy_id"],
            ["vacancies.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_column("vacancies", "requirements")
    op.drop_column("vacancies", "responsibility")


def downgrade() -> None:
    op.add_column(
        "vacancies",
        sa.Column("responsibility", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "vacancies",
        sa.Column("requirements", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_table("vacancy_skills")
