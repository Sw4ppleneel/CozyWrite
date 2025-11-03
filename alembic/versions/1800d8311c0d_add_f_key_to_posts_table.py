"""add f key to posts table

Revision ID: 1800d8311c0d
Revises: 56ad2fc46a79
Create Date: 2025-11-02 14:36:18.470873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '1800d8311c0d'
down_revision: Union[str, Sequence[str], None] = '56ad2fc46a79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add Content column
    op.add_column(
        'posts', 
        sa.Column('Content', sa.String(), nullable=False)
    )
    
    # Add Published column
    op.add_column(
        'posts', 
        sa.Column(
            'Published', 
            sa.Boolean(), 
            nullable=False, 
            server_default=text('True') # Use text()
        )
    )
    
    # Add Created_at column
    op.add_column(
        'posts', 
        sa.Column(
            'Created_at', 
            sa.TIMESTAMP(timezone=True),
            nullable=False, 
            server_default=text('now()') # Use text()
        )
    )
    
    # Add user_id column
    op.add_column(
        'posts', 
        sa.Column('user_id', sa.Integer(), nullable=False)
    )
    
    # Create the Foreign Key constraint
    # We give it an explicit name 'posts_users_fk' so we can drop it later.
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')
    op.drop_column('posts', 'Created_at')
    op.drop_column('posts', 'Published')
    op.drop_column('posts', 'Content')
    pass
