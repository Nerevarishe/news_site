"""creating deferred table

Revision ID: 1a2ef1342a32
Revises: 6b5d4bd70189
Create Date: 2019-05-05 21:41:06.798521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a2ef1342a32'
down_revision = '6b5d4bd70189'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deferred_drug',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('drug_name', sa.String(), nullable=True),
    sa.Column('drug_amount', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deferred_drug')
    # ### end Alembic commands ###
