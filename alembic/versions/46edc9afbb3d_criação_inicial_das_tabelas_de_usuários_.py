"""Criação inicial das tabelas de usuários e contratos

Revision ID: 46edc9afbb3d
Revises: 
Create Date: 2025-07-17 10:35:53.525687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46edc9afbb3d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=1)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    op.create_table('contracts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('file_name', sa.VARCHAR(), nullable=True),
    sa.Column('uploaded_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('parties', sa.TEXT(), nullable=True),
    sa.Column('monetary_values', sa.TEXT(), nullable=True),
    sa.Column('main_obligations', sa.TEXT(), nullable=True),
    sa.Column('additional_data', sa.TEXT(), nullable=True),
    sa.Column('termination_clause', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contracts_id'), 'contracts', ['id'], unique=False)
    op.create_index(op.f('ix_contracts_file_name'), 'contracts', ['file_name'], unique=1)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_contracts_file_name'), table_name='contracts')
    op.drop_index(op.f('ix_contracts_id'), table_name='contracts')
    op.drop_table('contracts')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
