"""added index for slugs

Revision ID: 93075f9e6a4a
Revises: c97b1b14450c
Create Date: 2020-08-16 20:20:24.463771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93075f9e6a4a'
down_revision = 'c97b1b14450c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_post_slug'), 'post', ['slug'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_slug'), table_name='post')
    # ### end Alembic commands ###