"""empty message

Revision ID: 9f60152f8d3d
Revises: 
Create Date: 2019-07-04 18:20:43.644503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f60152f8d3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('form', sa.Column('fields', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('form', 'fields')
    # ### end Alembic commands ###