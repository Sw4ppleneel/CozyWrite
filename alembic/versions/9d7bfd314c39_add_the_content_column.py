"""add the content column

Revision ID: 9d7bfd314c39
Revises: 25f20da87531
Create Date: 2025-11-02 12:58:03.587112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d7bfd314c39'
down_revision: Union[str, Sequence[str], None] = '25f20da87531'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts' , sa.Column('content' , sa.String() , nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts' , 'content')
    pass
