"""empty message

Revision ID: 1eb0eec8ebc7
Revises: 2ced87a67b02
Create Date: 2015-04-27 22:45:03.581094

"""

# revision identifiers, used by Alembic.
revision = '1eb0eec8ebc7'
down_revision = '2ced87a67b02'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lager_data', sa.Column('stock', sa.Integer(), nullable=True))
    op.drop_column('lager_data', 'remaining_stock')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lager_data', sa.Column('remaining_stock', sa.INTEGER(), nullable=True))
    op.drop_column('lager_data', 'stock')
    ### end Alembic commands ###
