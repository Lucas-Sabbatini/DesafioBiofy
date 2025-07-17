"""Cria usuário administrador padrão

Revision ID: 842cb399159a
Revises: 46edc9afbb3d
Create Date: 2025-07-17 10:45:13.271268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import os

from app.auth.utils import get_password_hash


# revision identifiers, used by Alembic.
revision: str = '842cb399159a'
down_revision: Union[str, Sequence[str], None] = '46edc9afbb3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_username = os.getenv("ADMIN_USERNAME")

    if not (admin_password and admin_username):
        raise ValueError("As variáveis de ambiente ADMIN_PASSWORD e USERNAME são necessárias para esta migração.")

    hashed_password = get_password_hash(admin_password)


    users_table = sa.table('users',
                           sa.column('id', sa.Integer),
                           sa.column('username', sa.String),
                           sa.column('hashed_password', sa.String),
                           sa.column('is_active', sa.Boolean)
                           )
    op.bulk_insert(users_table,
                   [
                       {
                           'username': admin_username,
                           'hashed_password': hashed_password,
                           'is_active': True
                       }
                   ]
                   )


def downgrade() -> None:
    """Downgrade schema."""
    admin_username = os.getenv("ADMIN_USERNAME")
    if not admin_username:
        raise ValueError("A variável de ambiente ADMIN_USERNAME é necessária para esta migração.")

    op.execute(
        f"DELETE FROM users WHERE username = '{admin_username}'"
    )
