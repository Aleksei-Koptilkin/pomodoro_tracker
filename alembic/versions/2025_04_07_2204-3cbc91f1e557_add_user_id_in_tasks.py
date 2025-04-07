"""Add User id in Tasks

Revision ID: 3cbc91f1e557
Revises: 8e81ca7c1f35
Create Date: 2025-04-07 22:04:22.622837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cbc91f1e557'
down_revision: Union[str, None] = '8e81ca7c1f35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tasks', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Tasks', 'UserProfile', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Tasks', type_='foreignkey')
    op.drop_column('Tasks', 'user_id')
    # ### end Alembic commands ###
