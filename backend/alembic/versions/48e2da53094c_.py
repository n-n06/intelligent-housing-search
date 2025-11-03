"""empty message

Revision ID: 48e2da53094c
Revises: 34b2d19f4780
Create Date: 2025-11-03 16:23:42.300723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48e2da53094c'
down_revision: Union[str, Sequence[str], None] = '34b2d19f4780'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.drop_column('users', 'created_at')
    op.add_column(
        'users',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column('users', 'created_at')

