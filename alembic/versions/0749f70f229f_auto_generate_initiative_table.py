"""auto-generate initiative table

Revision ID: 0749f70f229f
Revises: 311df091f902
Create Date: 2021-12-23 17:12:52.849764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0749f70f229f'
down_revision = '311df091f902'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'initiative',
        sa.Column('initiative_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('initiative_type', sa.Integer(), nullable=False),
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
        sa.Column('status_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['created_by'],
            ['employee.employee_id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['initiative_type'],
            ['initiative_type.initiative_type_id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['status_id'],
            ['status_code.status_id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['updated_by'],
            ['employee.employee_id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('initiative_id')
    )
    op.create_index(
        op.f('ix_initiative_initiative_id'),
        'initiative',
        ['initiative_id'],
        unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_initiative_initiative_id'), table_name='initiative')
    op.drop_table('initiative')
    # ### end Alembic commands ###
