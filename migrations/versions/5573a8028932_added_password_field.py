"""added password field

Revision ID: 5573a8028932
Revises: 13345523d3ef
Create Date: 2023-11-22 20:16:46.165461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5573a8028932'
down_revision = '13345523d3ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
