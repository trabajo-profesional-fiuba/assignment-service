"""Add new columns to Periods

Revision ID: 0b1dfc0ed206
Revises: 3a369462af3b
Create Date: 2024-09-22 18:54:28.562727

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0b1dfc0ed206"
down_revision: Union[str, None] = "3a369462af3b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "periods",
        sa.Column(
            "groups_assignment_completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.add_column(
        "periods",
        sa.Column(
            "topics_tutors_assignment_completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.add_column(
        "periods",
        sa.Column(
            "presentation_dates_assignment_completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.execute(
        "UPDATE periods SET groups_assignment_completed = false WHERE groups_assignment_completed IS NULL"
    )
    op.execute(
        "UPDATE periods SET topics_tutors_assignment_completed = false WHERE topics_tutors_assignment_completed IS NULL"
    )
    op.execute(
        "UPDATE periods SET presentation_dates_assignment_completed = false WHERE presentation_dates_assignment_completed IS NULL"
    )


def downgrade():
    op.drop_column("periods", "groups_assignment_completed")
    op.drop_column("periods", "topics_tutors_assignment_completed")
    op.drop_column("periods", "presentation_dates_assignment_completed")
