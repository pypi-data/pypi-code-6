"""creating testimonial model

Revision ID: 53ef6444c12
Revises: None
Create Date: 2014-09-03 17:17:34.987763

"""

# revision identifiers, used by Alembic.
revision = '53ef6444c12'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'testimonials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sender_name', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('company_name', sa.String(length=200), nullable=False),
        sa.Column('company_url', sa.String(length=2000), nullable=False),
        sa.Column('company_logo', sa.String(length=2000), nullable=True),
        sa.Column('approved', sa.Boolean, server_default="0", nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('testimonials')
