"""add table datasets

Revision ID: c185de16327e
Revises: 
Create Date: 2024-03-04 03:49:53.261159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c185de16327e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datatsets',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('items', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.Date(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.Date(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('datatsets')
    # ### end Alembic commands ###