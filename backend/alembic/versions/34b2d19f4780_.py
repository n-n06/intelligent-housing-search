"""empty message

Revision ID: 34b2d19f4780
Revises: 08497592847f
Create Date: 2025-11-03 15:59:59.413720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34b2d19f4780'
down_revision: Union[str, Sequence[str], None] = '08497592847f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define the enum in Python
userrole_enum = sa.Enum('ADMIN', 'CUSTOMER', name='userrole')

def upgrade() -> None:
    # Create the enum type in PostgreSQL
    userrole_enum.create(op.get_bind(), checkfirst=True)

    # Apply the column alteration
    op.add_column('users', sa.Column('first_name', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(length=255), nullable=False))
    op.alter_column(
        'users',
        'role',
        existing_type=sa.VARCHAR(length=100),
        type_=userrole_enum,
        existing_nullable=False,
        postgresql_using="role::userrole"
    )
    op.drop_column('users', 'firstname')
    op.drop_column('users', 'lastname')


def downgrade() -> None:
    # Revert to VARCHAR and drop the enum type
    op.add_column('users', sa.Column('lastname', sa.VARCHAR(length=255), nullable=False))
    op.add_column('users', sa.Column('firstname', sa.VARCHAR(length=255), nullable=False))
    op.alter_column(
        'users',
        'role',
        existing_type=userrole_enum,
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
        postgresql_using="role::text"
    )
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')

    # Drop the enum type if not used elsewhere
    userrole_enum.drop(op.get_bind(), checkfirst=True)


