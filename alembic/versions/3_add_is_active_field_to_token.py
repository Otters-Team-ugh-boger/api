"""add is_active field to token

Revision ID: 3
Revises: 2
Create Date: 2019-12-01 12:31:21.869865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3'
down_revision = '2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_tokens', sa.Column('is_active', sa.Boolean(), server_default=sa.text('1'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_tokens', 'is_active')
    # ### end Alembic commands ###
