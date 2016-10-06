"""empty message

Revision ID: 3565b16d313e
Revises: 559565b45d06
Create Date: 2016-01-09 00:12:41.375256

"""

# revision identifiers, used by Alembic.
revision = '3565b16d313e'
down_revision = '559565b45d06'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('title', sa.String(length=512), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('paragraph', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.ForeignKeyConstraint(['paragraph'], ['paragraph.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    ### end Alembic commands ###