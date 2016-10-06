"""empty message

Revision ID: 57e89ee4bc0d
Revises: 24d91e87118c
Create Date: 2015-11-14 18:35:53.441908

"""

# revision identifiers, used by Alembic.
revision = '57e89ee4bc0d'
down_revision = '24d91e87118c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('layout', sa.Enum('content', 'blog', 'issue', 'fundraiser'), nullable=True))
    op.add_column('section', sa.Column('section_type', sa.Enum('content', 'blog', 'magazine', 'fundraiser'), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('section', 'section_type')
    op.drop_column('page', 'layout')
    ### end Alembic commands ###