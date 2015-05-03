"""empty message

Revision ID: 477f8bf52d3
Revises: 40cf3d21c6eb
Create Date: 2015-05-03 12:21:44.344624

"""

# revision identifiers, used by Alembic.
revision = '477f8bf52d3'
down_revision = '40cf3d21c6eb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('puffer_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('temperature_top', sa.Integer(), nullable=True),
    sa.Column('temperature_bottom', sa.Integer(), nullable=True),
    sa.Column('hot_water_storage_temp', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'kessel_data', sa.Column('exhaust_blower', sa.Integer(), nullable=True))
    op.add_column(u'kessel_data', sa.Column('exhaust_temperature', sa.Integer(), nullable=True))
    op.add_column(u'kessel_data', sa.Column('feed_line_temperature', sa.Integer(), nullable=True))
    op.add_column(u'kessel_data', sa.Column('pressure', sa.Float(), nullable=True))
    op.add_column(u'kessel_data', sa.Column('residual_oxygen', sa.Float(), nullable=True))
    op.add_column(u'kessel_data', sa.Column('temperature', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'kessel_data', 'temperature')
    op.drop_column(u'kessel_data', 'residual_oxygen')
    op.drop_column(u'kessel_data', 'pressure')
    op.drop_column(u'kessel_data', 'feed_line_temperature')
    op.drop_column(u'kessel_data', 'exhaust_temperature')
    op.drop_column(u'kessel_data', 'exhaust_blower')
    op.drop_table('puffer_data')
    ### end Alembic commands ###