"""Add subcategories

Revision ID: 3ae0783e86c6
Revises: None
Create Date: 2014-10-19 17:06:04.269233

"""

# revision identifiers, used by Alembic.
revision = '3ae0783e86c6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # sqlite doesn't support adding a ForeignKey column, so instead...
    # 1. Rename existing table
    op.rename_table('categories', 'categories_old')

    # 2. Create new table with additional column
    op.create_table('categories',
        sa.Column('id', sa.Integer()),
        sa.Column('parent_id', sa.Integer()),
        sa.Column('name', sa.Unicode(), unique=True, nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['parent.id']),
        sa.PrimaryKeyConstraint('id'))

    # 3. Copy data from old table to new table
    conn = op.get_bind()
    res = conn.execute("select id, name from categories_old;")
    results = res.fetchall()
    if len(results) > 0:
        # op.bulk_insert requires a table object but it was too difficult to
        # create with constraints, so copy data using sql. The following
        # alembic issue suggests a fix to make this easier:
        # https://bitbucket.org/zzzeek/alembic/issue/205/return-the-table-in-create_table
        for r in results:
            sql_stmt = "insert into categories (id, name) values (?, ?);"
            result = conn.execute(sql_stmt, (r[0], r[1]))

    # 4. Drop old table
    op.drop_table('categories_old')


def downgrade():
    op.drop_column('categories', 'parent_id')
