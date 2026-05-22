"""сделал уникальным user_id в UserToken

Revision ID: e03daec06e5d
Revises: b0d447c8d64e
Create Date: 2026-05-23 01:22:25.000208

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e03daec06e5d"
down_revision: Union[str, Sequence[str], None] = "b0d447c8d64e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "user_tokens", ["user_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "user_tokens", type_="unique")
