"""adding comment field to defectera module

Revision ID: 805de9c71db5
Revises: 090039237459
Create Date: 2018-11-05 08:28:45.420354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '805de9c71db5'
down_revision = '090039237459'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('defectura_card', sa.Column('comment', sa.String(), nullable=True))
    op.drop_index('ix_drugstore_list_ds_name', table_name='drugstore_list')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_drugstore_list_ds_name', 'drugstore_list', ['ds_name'], unique=False)
    op.drop_column('defectura_card', 'comment')
    # ### end Alembic commands ###