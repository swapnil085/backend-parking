"""empty message

Revision ID: 5450b878e1e4
Revises: 2e2621e4c820
Create Date: 2018-11-19 16:10:20.410072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5450b878e1e4'
down_revision = '2e2621e4c820'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slot_id', sa.Integer(), nullable=True),
    sa.Column('car_no', sa.String(length=255), nullable=False),
    sa.Column('reservation_no', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['slot_id'], ['slots.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    # ### end Alembic commands ###
