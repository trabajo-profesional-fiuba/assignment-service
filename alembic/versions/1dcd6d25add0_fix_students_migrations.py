"""fix students migrations

Revision ID: 1dcd6d25add0
Revises: 20183e7d0b0c
Create Date: 2024-11-04 21:12:15.137062

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1dcd6d25add0"
down_revision: Union[str, None] = "20183e7d0b0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_constraint("uq_student_period", "student_periods", type_="unique")
    op.create_unique_constraint(
        "uq_student_period", "student_periods", ["student_id", "period_id"]
    )

    op.drop_constraint(
        "student_periods_period_id_fkey", "student_periods", type_="foreignkey"
    )
    op.drop_constraint(
        "student_periods_student_id_fkey", "student_periods", type_="foreignkey"
    )

    op.create_foreign_key(
        None, "student_periods", "periods", ["period_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "student_periods", "users", ["student_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "student_periods", type_="foreignkey")
    op.drop_constraint(None, "student_periods", type_="foreignkey")

    op.create_foreign_key(
        "student_periods_student_id_fkey",
        "student_periods",
        "users",
        ["student_id"],
        ["id"],
    )
    op.create_foreign_key(
        "student_periods_period_id_fkey",
        "student_periods",
        "periods",
        ["period_id"],
        ["id"],
    )

    op.drop_constraint("uq_student_period", "student_periods", type_="unique")
    op.create_unique_constraint("uq_student_period", "student_periods", ["student_id"])
    # ### end Alembic commands ###
