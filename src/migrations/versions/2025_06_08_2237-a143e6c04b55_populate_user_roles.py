"""populate user roles

Revision ID: a143e6c04b55
Revises: eff959dd47dd
Create Date: 2025-06-08 22:37:34.404534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from models.user import UserRole


# revision identifiers, used by Alembic.
revision: str = 'a143e6c04b55'
down_revision: Union[str, None] = 'eff959dd47dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = sessionmaker(bind=bind)()

    entities = [
        UserRole(alias='admin', name='This is the admin user'),
        UserRole(alias='client', name='This is the client user'),
    ]
    session.bulk_save_objects(entities)
    session.commit()


def downgrade() -> None:
    pass
