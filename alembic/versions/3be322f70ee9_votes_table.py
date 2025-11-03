"""votes table

Revision ID: 3be322f70ee9
Revises: 1800d8311c0d
Create Date: 2025-11-02 14:40:38.379096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3be322f70ee9'
down_revision: Union[str, Sequence[str], None] = '1800d8311c0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        
        # Define Foreign Keys
        sa.ForeignKeyConstraint(
            ['post_id'], ['posts.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], ondelete='CASCADE'
        ),
        
        # Define Composite Primary Key
        sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass
