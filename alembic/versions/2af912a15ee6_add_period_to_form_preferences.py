"""add period to form preferences

Revision ID: 2af912a15ee6
Revises: e1752434f27e
Create Date: 2024-11-02 17:04:26.230755

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2af912a15ee6"
down_revision: Union[str, None] = "e1752434f27e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "form_preferences", sa.Column("period_id", sa.String(), nullable=True)
    )
    op.create_foreign_key(
        None, "form_preferences", "periods", ["period_id"], ["id"], ondelete="CASCADE"
    )

    # Actualizo las respuestas existentes
    op.execute(
        "UPDATE form_preferences SET period_id = '2C2024' WHERE period_id IS NULL"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "form_preferences", type_="foreignkey")
    op.drop_column("form_preferences", "period_id")

    # ### end Alembic commands ###
