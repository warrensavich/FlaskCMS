"""empty message

Revision ID: f6e59558984
Revises: 294c1d418a40
Create Date: 2016-01-11 11:42:03.263233

"""

# revision identifiers, used by Alembic.
revision = 'f6e59558984'
down_revision = '294c1d418a40'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dynamic_page',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('page_component',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('page_container_id', sa.Integer(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('component_type', sa.String(length=255), nullable=True),
    sa.Column('gallery_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('href', sa.String(length=512), nullable=True),
    sa.Column('link_to_page_id', sa.Integer(), nullable=True),
    sa.Column('link_to_paragraph_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gallery_id'], ['gallery.id'], ),
    sa.ForeignKeyConstraint(['link_to_page_id'], ['page.id'], ),
    sa.ForeignKeyConstraint(['link_to_paragraph_id'], ['paragraph.id'], ),
    sa.ForeignKeyConstraint(['page_container_id'], ['dynamic_page.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'image', sa.Column('link', sa.String(length=512), nullable=True))
    op.add_column(u'page', sa.Column('landing_page_data', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'page', 'landing_page_data')
    op.drop_column(u'image', 'link')
    op.drop_table('page_component')
    op.drop_table('dynamic_page')
    ### end Alembic commands ###
