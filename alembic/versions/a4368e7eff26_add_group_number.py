"""add group number

Revision ID: a4368e7eff26
Revises: 6b37846cb4de
Create Date: 2024-11-01 09:48:38.014590

"""
from typing import Sequence, Union

from alembic import op
from pytest import Session
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4368e7eff26'
down_revision: Union[str, None] = '6b37846cb4de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('group_number', sa.Integer(), nullable=True))
    # Bind the session to the connection
    bind = op.get_bind()
    session = Session(bind=bind)

    # Update the group_number to match the id
    groups = session.execute(sa.select([sa.table('groups')])).fetchall()
    for group in groups:
        session.execute(
            sa.update(sa.table('group'))
            .where(sa.table('group').c.id == group.id)
            .values(group_number=group.id)
        )
    session.commit()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('groups', 'group_number')
    # ### end Alembic commands ###
