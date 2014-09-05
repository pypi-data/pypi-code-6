"""creating user model

Revision ID: a927bafc28e
Revises: 5566da8254ae
Create Date: 2014-09-04 15:26:44.876595

"""

# revision identifiers, used by Alembic.
revision = 'a927bafc28e'
down_revision = '5566da8254ae'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.alter_column(
        u'testimonials', 'order',
        existing_type=mysql.INTEGER(display_width=11),
        nullable=True
    )


def downgrade():
    op.alter_column(
        u'testimonials', 'order',
        existing_type=mysql.INTEGER(display_width=11),
        nullable=False
    )
    op.drop_table('user')
