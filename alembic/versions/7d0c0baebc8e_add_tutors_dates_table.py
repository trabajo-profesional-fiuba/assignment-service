"""add tutors dates table

Revision ID: 7d0c0baebc8e
Revises: 7d3fb66aaa9e
Create Date: 2024-10-09 22:55:48.741259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d0c0baebc8e'
down_revision: Union[str, None] = '7d3fb66aaa9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tutors_dates_slots',
    sa.Column('tutor_id', sa.Integer(), nullable=False),
    sa.Column('slot', sa.DateTime(), nullable=False),
    sa.Column('period_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['period_id'], ['periods.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['slot'], ['dates_slots.slot'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tutor_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tutor_id', 'slot')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tutors_dates_slots')
    # ### end Alembic commands ###
