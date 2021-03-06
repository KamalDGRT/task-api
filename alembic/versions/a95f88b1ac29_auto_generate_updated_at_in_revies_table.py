"""auto-generate updated_at in revies table

Revision ID: a95f88b1ac29
Revises: 3f5df9b9c5dc
Create Date: 2021-12-25 12:57:52.465155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a95f88b1ac29'
down_revision = '3f5df9b9c5dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'review',
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('review', 'updated_at')
    # ### end Alembic commands ###
