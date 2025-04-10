"""fix form flag

Revision ID: 069cdd65470b
Revises: d8cd55091e57
Create Date: 2024-09-07 09:59:13.204860

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "069cdd65470b"
down_revision: Union[str, None] = "d8cd55091e57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("periods", sa.Column("form_active", sa.Boolean(), nullable=True))

    op.execute("UPDATE periods SET form_active = true WHERE form_active IS NULL")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("periods", "form_active")
    # ### end Alembic commands ###
