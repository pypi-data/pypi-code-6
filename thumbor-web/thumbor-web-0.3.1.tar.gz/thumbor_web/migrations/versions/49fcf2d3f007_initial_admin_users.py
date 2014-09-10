"""initial admin users

Revision ID: 49fcf2d3f007
Revises: a927bafc28e
Create Date: 2014-09-04 15:31:43.791143

"""

# revision identifiers, used by Alembic.
revision = '49fcf2d3f007'
down_revision = 'a927bafc28e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table
from werkzeug.security import generate_password_hash


def upgrade():
    users_table = table(
        'user',
        sa.Column('username', sa.String(length=80)),
        sa.Column('email', sa.String(length=120)),
        sa.Column('password', sa.String(length=255)),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "username": "heynemann",
                "email": "heynemann@gmail.com",
                "password": generate_password_hash("changeme"),
            },
        ]
    )


def downgrade():
    pass
