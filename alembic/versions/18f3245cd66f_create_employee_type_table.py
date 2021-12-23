"""create employee_type table

Revision ID: 18f3245cd66f
Revises: 
Create Date: 2021-12-23 15:34:07.650392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18f3245cd66f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'employee_type',
        sa.Column('employee_type_id', sa.Integer(), nullable=False),
        sa.Column('role_name', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('employee_type_id'),
        sa.UniqueConstraint('role_name')
    )
    pass


def downgrade():
    op.drop_table('employee_type')
    pass
