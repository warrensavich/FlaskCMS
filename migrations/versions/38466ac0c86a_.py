"""empty message

Revision ID: 38466ac0c86a
Revises: 3872d597a811
Create Date: 2015-11-12 22:59:39.089711

"""

# revision identifiers, used by Alembic.
revision = '38466ac0c86a'
down_revision = '3872d597a811'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('section', sa.Column('creator', sa.Integer(), nullable=True))
    op.add_column('section', sa.Column('theme', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('section', 'theme')
    op.drop_column('section', 'creator')
    ### end Alembic commands ###
