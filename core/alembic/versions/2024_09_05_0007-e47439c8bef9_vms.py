"""vms

Revision ID: e47439c8bef9
Revises: 0fe34dcc0fb0
Create Date: 2024-09-05 00:07:34.193300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e47439c8bef9'
down_revision: Union[str, None] = '0fe34dcc0fb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vm_startup_settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vm_id', sa.Integer(), nullable=False),
    sa.Column('node_name', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('enable_dependencies', sa.Boolean(), nullable=False),
    sa.Column('startup_timeout', sa.Integer(), nullable=False),
    sa.Column('dependencies', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('healthcheck',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vms_id', sa.Integer(), nullable=False),
    sa.Column('target_url', sa.String(), nullable=False),
    sa.Column('check_method', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['vms_id'], ['vm_startup_settings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('healthcheck')
    op.drop_table('vm_startup_settings')
    # ### end Alembic commands ###
