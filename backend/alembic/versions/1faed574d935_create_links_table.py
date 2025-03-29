"""create links table

Revision ID: 1faed574d935
Revises: 
Create Date: 2025-03-28 19:57:06.247429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1faed574d935'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('links',
    sa.Column('short_code', sa.String(), nullable=False),
    sa.Column('original_url', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('clicks_count', sa.Integer(), nullable=False),
    sa.Column('last_clicked_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('short_code')
    )
    op.create_index(op.f('ix_links_short_code'), 'links', ['short_code'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_links_short_code'), table_name='links')
    op.drop_table('links')
    # ### end Alembic commands ###
