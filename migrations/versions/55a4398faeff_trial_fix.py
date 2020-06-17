"""trial fix

Revision ID: 55a4398faeff
Revises: 
Create Date: 2020-06-17 17:49:06.475436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55a4398faeff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'poem', ['account_role'])
    op.create_unique_constraint(None, 'roles', ['role'])
    op.create_unique_constraint(None, 'song', ['account_role'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'song', type_='unique')
    op.drop_constraint(None, 'roles', type_='unique')
    op.drop_constraint(None, 'poem', type_='unique')
    # ### end Alembic commands ###
