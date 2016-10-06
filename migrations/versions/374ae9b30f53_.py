"""empty message

Revision ID: 374ae9b30f53
Revises: 4585727a01f6
Create Date: 2016-03-27 23:06:36.260627

"""

# revision identifiers, used by Alembic.
revision = '374ae9b30f53'
down_revision = '4585727a01f6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('company', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'company')
    ### end Alembic commands ###