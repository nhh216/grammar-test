"""add question_bank table

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-02-20 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'question_bank',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('options', JSON(), nullable=False),
        sa.Column('correct_answer', sa.String(length=1), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('difficulty', sa.String(length=10), nullable=False, server_default='medium'),
        sa.ForeignKeyConstraint(['topic_id'], ['grammar_topics.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_question_bank_topic_id', 'question_bank', ['topic_id'])


def downgrade() -> None:
    op.drop_index('ix_question_bank_topic_id', table_name='question_bank')
    op.drop_table('question_bank')
