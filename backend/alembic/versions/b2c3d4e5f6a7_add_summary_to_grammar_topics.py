"""add summary to grammar_topics

Revision ID: b2c3d4e5f6a7
Revises: 9dddb31f08cc
Create Date: 2026-02-20 10:21:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = '9dddb31f08cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('grammar_topics', sa.Column('summary', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('grammar_topics', 'summary')
