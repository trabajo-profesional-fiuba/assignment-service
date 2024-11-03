"""presentation dates init value

Revision ID: 3fd918400333
Revises: 2af912a15ee6
Create Date: 2024-11-02 19:12:08.085112

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3fd918400333"
down_revision: Union[str, None] = "2af912a15ee6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "UPDATE periods SET presentation_dates_assignment_completed = false WHERE initial_project_active IS NULL"
    )


def downgrade() -> None:
    pass
