"""initial users px settings

Revision ID: 324ab630e3f6
Revises: 
Create Date: 2024-09-01 21:17:45.480801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '324ab630e3f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('proxmox_settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hostname', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('token_value', sa.String(), nullable=False),
    sa.Column('validated', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hostname')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('proxmox_extra_settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('proxmox_settings_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['proxmox_settings_id'], ['proxmox_settings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('user_settings')
    op.drop_table('proxmox_extra_settings')
    op.drop_table('users')
    op.drop_table('proxmox_settings')
    # ### end Alembic commands ###
