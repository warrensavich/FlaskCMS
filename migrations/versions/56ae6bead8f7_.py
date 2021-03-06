"""empty message

Revision ID: 56ae6bead8f7
Revises: 57e89ee4bc0d
Create Date: 2015-11-14 20:35:00.394900

"""

# revision identifiers, used by Alembic.
revision = '56ae6bead8f7'
down_revision = '57e89ee4bc0d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gallery', sa.Column('slug', sa.String(length=255), nullable=True))
    op.create_unique_constraint(None, 'gallery', ['slug'])
    op.add_column('image', sa.Column('order', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('image', 'order')
    op.drop_constraint(None, 'gallery')
    op.drop_column('gallery', 'slug')
    ### end Alembic commands ###
