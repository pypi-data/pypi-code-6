"""empty message

Revision ID: 1b1a5f6b42a
Revises: None
Create Date: 2014-02-05 05:27:08.986772

"""

# revision identifiers, used by Alembic.
revision = '1b1a5f6b42a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('apikey', sa.String(length=255), nullable=False),
                    sa.Column(
                        'secretkey',
                        sa.String(length=255),
                        nullable=True),
                    sa.PrimaryKeyConstraint('apikey'),
                    sa.UniqueConstraint('secretkey')
                    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###
