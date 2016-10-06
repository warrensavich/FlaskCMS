"""empty message

Revision ID: 24d91e87118c
Revises: e82d441bcc4
Create Date: 2015-11-14 18:35:36.667367

"""

# revision identifiers, used by Alembic.
revision = '24d91e87118c'
down_revision = 'e82d441bcc4'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page', 'layout')
    op.drop_column('section', 'section_type')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('section', sa.Column('section_type', mysql.ENUM(u'content', u'blog'), nullable=True))
    op.add_column('page', sa.Column('layout', mysql.ENUM(u'content', u'blog'), nullable=True))
    ### end Alembic commands ###
