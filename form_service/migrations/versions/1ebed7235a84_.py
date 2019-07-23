"""empty message

Revision ID: 1ebed7235a84
Revises: 
Create Date: 2019-07-17 17:09:39.932571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ebed7235a84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('form',
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.Column('fields', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('form_id'),
    sa.UniqueConstraint('title', 'owner', 'fields')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('form')
    # ### end Alembic commands ###