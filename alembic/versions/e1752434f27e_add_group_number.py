"""add group number

Revision ID: e1752434f27e
Revises: a4368e7eff26
Create Date: 2024-11-01 23:02:21.754357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1752434f27e'
down_revision: Union[str, None] = 'a4368e7eff26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('periods', sa.Column('presentation_dates_available', sa.Boolean(), nullable=True))
    op.alter_column('periods', 'initial_project_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('periods', 'intermediate_project_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('periods', 'final_project_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('periods', 'groups_assignment_completed',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.alter_column('periods', 'topics_tutors_assignment_completed',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.alter_column('periods', 'presentation_dates_assignment_completed',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('periods', 'presentation_dates_assignment_completed',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.alter_column('periods', 'topics_tutors_assignment_completed',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.alter_column('periods', 'groups_assignment_completed',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.alter_column('periods', 'final_project_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('periods', 'intermediate_project_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('periods', 'initial_project_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_column('periods', 'presentation_dates_available')
    # ### end Alembic commands ###
