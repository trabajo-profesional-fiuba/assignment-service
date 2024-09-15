"""add StudentPeriod table

Revision ID: 0119449915bc
Revises: 0121f8a608f6
Create Date: 2024-09-15 17:35:22.396316

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0119449915bc"
down_revision: Union[str, None] = "0121f8a608f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "student_periods",
        sa.Column("period_id", sa.String(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["period_id"],
            ["periods.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("period_id", "student_id"),
    )

    # ---------- init student_periods table ----------
    connection = op.get_bind()

    # verify if period exist
    period_id = "2C2024"
    result = connection.execute(
        sa.text("SELECT COUNT(*) FROM periods WHERE id = :period_id"),
        {"period_id": period_id},
    )
    period_exists = result.scalar() > 0

    # add period if does not exist
    if not period_exists:
        connection.execute(
            sa.text(
                "INSERT INTO periods (id, created_at, form_active, initial_project_active, intermediate_project_active, final_project_active) VALUES (:period_id, NOW(), TRUE, FALSE, FALSE, FALSE)"
            ),
            {"period_id": period_id},
        )

    # get students
    students = connection.execute(
        sa.text("SELECT id FROM users WHERE role = 'STUDENT'")
    ).fetchall()

    # add student - period rows
    if students:
        for student in students:
            connection.execute(
                sa.text(
                    "INSERT INTO student_periods (period_id, student_id) VALUES (:period_id, :student_id)"
                ),
                {"period_id": "2C2024", "student_id": student.id},
            )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("student_periods")
    # ### end Alembic commands ###
