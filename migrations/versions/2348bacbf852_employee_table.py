"""Employee table

Revision ID: 2348bacbf852
Revises: 805de9c71db5
Create Date: 2018-11-15 13:07:51.380860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2348bacbf852'
down_revision = '805de9c71db5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('patronymic', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('preferred_time', sa.String(), nullable=True),
    sa.Column('work_hours_in_day', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employee_last_name'), 'employee', ['last_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_employee_last_name'), table_name='employee')
    op.drop_table('employee')
    # ### end Alembic commands ###