"""add address_id to user table

Revision ID: cf247ffa9e57
Revises: bbf37b95d4ec
Create Date: 2024-12-23 20:21:46.717953

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cf247ffa9e57"
down_revision: Union[str, None] = "bbf37b95d4ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("address_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "address_users_fk",
        source_table="users",
        referent_table="address",
        local_cols=["address_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("address_users_fk", table_name="users")
    op.drop_column("users", "address_id")
