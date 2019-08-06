"""修改错误

Revision ID: 394af8f82441
Revises: a17493940cb3
Create Date: 2019-08-06 14:52:04.580926

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '394af8f82441'
down_revision = 'a17493940cb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.drop_column('roles', 'permission')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('permission', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('roles', 'permissions')
    # ### end Alembic commands ###
