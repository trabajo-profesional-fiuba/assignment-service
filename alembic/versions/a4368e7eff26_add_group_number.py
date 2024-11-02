"""add group number

Revision ID: a4368e7eff26
Revises: 6b37846cb4de
Create Date: 2024-11-01 09:48:38.014590

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a4368e7eff26"
down_revision: Union[str, None] = "6b37846cb4de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("groups", sa.Column("group_number", sa.Integer(), nullable=True))
    # Bind the session to the connection
    bind = op.get_bind()

    Session = sessionmaker(bind=bind)
    groups_table = sa.table("groups", sa.column("id"), sa.column("group_number"))

    with Session() as session:
        # Update the group_number to match the id
        print(len(sa.table("groups").columns))
        groups = session.execute(sa.select(groups_table.c.id)).fetchall()
        for group in groups:
            session.execute(
                sa.update(groups_table)
                .where(groups_table.c.id == group[0])
                .values(group_number=group[0])
            )
        session.commit()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("groups", "group_number")
    # ### end Alembic commands ###
