"""fix: username -> user_id in Action

Revision ID: a89eeb46e2d7
Revises: 3e5951a401e3
Create Date: 2022-12-19 21:41:08.941623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a89eeb46e2d7'
down_revision = '3e5951a401e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('action', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_column('action', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('action', sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('action', 'user_id')
    # ### end Alembic commands ###