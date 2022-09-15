"""Added damage int to Enemy

Revision ID: 943da7d3e46d
Revises: 4995d9601000
Create Date: 2022-09-14 21:27:47.350329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '943da7d3e46d'
down_revision = '4995d9601000'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('enemies', sa.Column('damage', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('enemies', 'damage')
    # ### end Alembic commands ###