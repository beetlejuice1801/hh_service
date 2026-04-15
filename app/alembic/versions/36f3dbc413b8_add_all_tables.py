"""add all tables

Revision ID: 36f3dbc413b8
Revises:
Create Date: 2026-04-15 22:31:09.557584

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "36f3dbc413b8"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
