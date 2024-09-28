"""Add unique constraint on student_id in student_periods

Revision ID: 3a369462af3b
Revises: 0119449915bc
Create Date: 2024-09-19 17:56:38.125788

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "3a369462af3b"
down_revision: Union[str, None] = "0119449915bc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_primary_key("student_id_pkey", "student_periods", ["student_id"])
    op.create_unique_constraint("uq_student_period", "student_periods", ["student_id"])


def downgrade():
    op.create_primary_key(
        "student_periods_pkey", "student_periods", ["period_id", "student_id"]
    )
    op.drop_constraint("uq_student_period", "student_periods", type_="unique")
