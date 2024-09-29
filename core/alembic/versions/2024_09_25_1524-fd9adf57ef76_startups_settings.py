"""startups_settings

Revision ID: fd9adf57ef76
Revises: 9a1b7c452b4a
Create Date: 2024-09-25 15:24:51.520574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd9adf57ef76'
down_revision: Union[str, None] = '9a1b7c452b4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('starting_settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uptime_threshold', sa.Integer(), nullable=False),
    sa.Column('enable', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('starting_settings')
    # ### end Alembic commands ###