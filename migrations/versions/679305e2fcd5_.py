"""empty message

Revision ID: 679305e2fcd5
Revises: 8b44c7f968d7
Create Date: 2020-05-25 07:31:20.804528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '679305e2fcd5'
down_revision = '8b44c7f968d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('guards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('slots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slot_no', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('AVAILABLE', 'RESERVED', 'OCCUPIED'), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('contact_number', sa.String(length=255), nullable=False),
    sa.Column('gender', sa.Enum('M', 'F'), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('slot_id', sa.Integer(), nullable=True),
    sa.Column('car_no', sa.String(length=255), nullable=False),
    sa.Column('reservation_no', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['slot_id'], ['slots.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedbacks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comments', sa.String(length=255), nullable=True),
    sa.Column('rating', sa.Enum('1', '2', '3', '4', '5'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('walkins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('reservation_no', sa.String(length=255), nullable=False),
    sa.Column('car_no', sa.String(length=255), nullable=False),
    sa.Column('slot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['slot_id'], ['slots.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('walkins')
    op.drop_table('feedbacks')
    op.drop_table('bookings')
    op.drop_table('users')
    op.drop_table('slots')
    op.drop_table('guards')
    op.drop_table('admins')
    # ### end Alembic commands ###
