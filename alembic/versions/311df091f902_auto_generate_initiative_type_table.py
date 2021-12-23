"""auto-generate initiative_type table

Revision ID: 311df091f902
Revises: d3f4366dda5b
Create Date: 2021-12-23 17:04:53.568401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '311df091f902'
down_revision = 'd3f4366dda5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'initiative_type',
        sa.Column('initiative_type_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.Column('updated_by', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['created_by'],
            ['employee.employee_id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['updated_by'],
            ['employee.employee_id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('initiative_type_id')
    )
    op.create_index(
        op.f('ix_initiative_type_initiative_type_id'),
        'initiative_type',
        ['initiative_type_id'],
        unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f('ix_initiative_type_initiative_type_id'),
        table_name='initiative_type'
    )
    op.drop_table('initiative_type')
    # ### end Alembic commands ###