"""empty message

Revision ID: 4585727a01f6
Revises: 38c12e0291f6
Create Date: 2016-03-27 22:50:48.890323

"""

# revision identifiers, used by Alembic.
revision = '4585727a01f6'
down_revision = '38c12e0291f6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('experiences', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('most_interested', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('preferred_resource', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'preferred_resource')
    op.drop_column('user', 'most_interested')
    op.drop_column('user', 'experiences')
    ### end Alembic commands ###