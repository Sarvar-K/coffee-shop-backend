"""init

Revision ID: eff959dd47dd
Revises: 
Create Date: 2025-06-08 21:19:03.685613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eff959dd47dd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_role',
    sa.Column('alias', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=300), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('alias'),
    schema='coffee_shop_backend'
    )


def downgrade() -> None:
    op.drop_table('user_role', schema='coffee_shop_backend')
