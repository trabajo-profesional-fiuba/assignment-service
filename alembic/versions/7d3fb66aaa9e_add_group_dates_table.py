"""add group dates table

Revision ID: 7d3fb66aaa9e
Revises: 140c542d2c01
Create Date: 2024-10-09 22:20:55.937472

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7d3fb66aaa9e"
down_revision: Union[str, None] = "140c542d2c01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "group_dates_slots",
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("slot", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["slot"], ["dates_slots.slot"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("group_id", "slot"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("group_dates_slots")
    # ### end Alembic commands ###
