"""empty message

Revision ID: 02f807661508
Revises: 534558effd0c
Create Date: 2019-09-20 08:51:50.026859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02f807661508'
down_revision = '534558effd0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True, default=False))
    op.add_column('Artist', sa.Column('website', sa.String(length=120), nullable=True))
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('Artist', 'website')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###