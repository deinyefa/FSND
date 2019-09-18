"""empty message

Revision ID: ba42c7f4b616
Revises: d3bf37a42982
Create Date: 2019-09-17 06:50:36.418228

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ba42c7f4b616'
down_revision = 'd3bf37a42982'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genre')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genre', postgresql.BYTEA(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###