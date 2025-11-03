"""create post table

Revision ID: 25f20da87531
Revises: 
Create Date: 2025-11-02 12:41:30.666345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25f20da87531'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column("id", sa.Integer(), nullable=False , primary_key=True,
                                        ), sa.Column("Title" , sa.String() , nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
