"""genres

Revision ID: 5ea0dd5775b6
Revises: b6a58bcbdf0f
Create Date: 2021-12-08 17:36:14.809149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ea0dd5775b6'
down_revision = 'b6a58bcbdf0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('movie_genre', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movie', 'movie_genre')
    # ### end Alembic commands ###