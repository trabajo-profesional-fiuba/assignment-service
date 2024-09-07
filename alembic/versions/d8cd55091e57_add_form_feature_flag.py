"""Add form feature flag

Revision ID: d8cd55091e57
Revises: 
Create Date: 2024-09-05 23:29:23.794122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd8cd55091e57'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Get the current database inspector
    inspector = sa.inspect(op.get_bind())
    table_names = inspector.get_table_names()

    # Check if the table already exists
    if 'categories' not in table_names :
        op.create_table('categories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        )
    if 'periods' not in table_names :
        op.create_table('periods',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        )
        op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('role', sa.Enum('STUDENT', 'TUTOR', 'ADMIN', name='role'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        )
    
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True, if_not_exists=True)
    if 'topics' not in table_names :
        op.create_table('topics',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
        )
    if 'tutor_periods' not in table_names :
        op.create_table('tutor_periods',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('period_id', sa.String(), nullable=True),
        sa.Column('tutor_id', sa.Integer(), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('is_evaluator', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['period_id'], ['periods.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['tutor_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('period_id', 'tutor_id', name='tutor_period_const')
        )
    op.create_index(op.f('ix_tutor_periods_tutor_id'), 'tutor_periods', ['tutor_id'], unique=False, if_not_exists=True)
    if 'form_preferences' not in table_names :
        op.create_table('form_preferences',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('answer_id', sa.DateTime(), nullable=False),
        sa.Column('topic_1', sa.Integer(), nullable=False),
        sa.Column('topic_2', sa.Integer(), nullable=False),
        sa.Column('topic_3', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['topic_1'], ['topics.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['topic_2'], ['topics.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['topic_3'], ['topics.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )
    if 'groups' not in table_names :
        op.create_table('groups',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('assigned_topic_id', sa.Integer(), nullable=True),
        sa.Column('tutor_period_id', sa.Integer(), nullable=True),
        sa.Column('pre_report_date', sa.DateTime(), nullable=True),
        sa.Column('pre_report_approved', sa.Boolean(), nullable=True),
        sa.Column('intermediate_assigment_date', sa.DateTime(), nullable=True),
        sa.Column('intermediate_assigment_approved', sa.Boolean(), nullable=True),
        sa.Column('final_report_approved', sa.Boolean(), nullable=True),
        sa.Column('exhibition_date', sa.DateTime(), nullable=True),
        sa.Column('preferred_topics', postgresql.ARRAY(sa.Integer(), dimensions=1), nullable=True),
        sa.ForeignKeyConstraint(['assigned_topic_id'], ['topics.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['tutor_period_id'], ['tutor_periods.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
    if 'topics_tutor_periods' not in table_names :
        op.create_table('topics_tutor_periods',
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('tutor_period_id', sa.Integer(), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tutor_period_id'], ['tutor_periods.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('topic_id', 'tutor_period_id')
        )
    if 'groups_students' not in table_names :
        op.create_table('groups_students',
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('student_id')
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('groups_students')
    op.drop_table('topics_tutor_periods')
    op.drop_table('groups')
    op.drop_table('form_preferences')
    op.drop_index(op.f('ix_tutor_periods_tutor_id'), table_name='tutor_periods')
    op.drop_table('tutor_periods')
    op.drop_table('topics')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('periods')
    op.drop_table('categories')
