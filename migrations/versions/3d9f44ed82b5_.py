"""empty message

Revision ID: 3d9f44ed82b5
Revises: 354bd1d391c3
Create Date: 2015-11-14 06:39:05.396556

"""

# revision identifiers, used by Alembic.
revision = '3d9f44ed82b5'
down_revision = '354bd1d391c3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('layout', sa.Enum('content', 'blog'), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page', 'layout')
    ### end Alembic commands ###