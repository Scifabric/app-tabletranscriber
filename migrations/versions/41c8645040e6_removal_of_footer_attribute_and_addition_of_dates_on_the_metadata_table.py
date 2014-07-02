"""removal of footer attribute and addition of initial/final date on the metadata table

Revision ID: 41c8645040e6
Revises: 51a9f64a7a2
Create Date: 2014-05-28 18:20:31.473181

"""

# revision identifiers, used by Alembic.
revision = '41c8645040e6'
down_revision = '51a9f64a7a2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("page_table", "initialDate")
    op.drop_column("page_table", "finalDate")
    op.drop_column("metadata", "footer")
    op.add_column("metadata", sa.Column("initial_date", sa.VARCHAR(length=10)))
    op.add_column("metadata", sa.Column("final_date", sa.VARCHAR(length=10)))
    op.drop_constraint("page_book_id_key", "page", "unique")
    
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('page',
    sa.Column('id', sa.INTEGER(), server_default="nextval('page_id_seq'::regclass)", nullable=False),
    sa.Column('book_id', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('archiveURL', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('page_num', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], [u'book.id'], name=u'page_book_id_fkey', onupdate=u'CASCADE', ondelete=u'CASCADE'),
    sa.PrimaryKeyConstraint('id', name=u'page_pkey')
    )
    op.create_table('facts',
    sa.Column('id', sa.INTEGER(), server_default="pseudo_encrypt((nextval('fact_id_seq'::regclass))::integer)", nullable=False),
    sa.Column('user_id', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('book_id', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('page_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('top_pos', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('left_pos', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('bottom_pos', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('right_pos', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('fact_text', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'fact_pkey')
    )
    op.create_table('report',
    sa.Column('id', sa.INTEGER(), server_default="nextval('report_id_seq'::regclass)", nullable=False),
    sa.Column('message', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('app_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'report_pkey')
    )
    op.create_table('workflow_transaction',
    sa.Column('id', sa.INTEGER(), server_default="nextval('workflow_transaction_id_seq'::regclass)", nullable=False),
    sa.Column('task_id_1', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('task_id_2', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('task_id_3', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('task_id_4', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'workflow_transaction_pkey')
    )
    op.create_table('book',
    sa.Column('id', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('publisher', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('contributor', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('volume', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('img_url', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'book_pkey')
    )
    op.create_table('cell',
    sa.Column('id', sa.INTEGER(), server_default="nextval('cell_id_seq'::regclass)", nullable=False),
    sa.Column('x0', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('y0', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('x1', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('y1', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('text', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('page_table_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('page_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('book_id', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], [u'book.id'], name=u'fk_cell_book_id', onupdate=u'CASCADE', ondelete=u'CASCADE'),
    sa.ForeignKeyConstraint(['page_id'], [u'page.id'], name=u'fk_cell_page_id', onupdate=u'CASCADE', ondelete=u'CASCADE'),
    sa.ForeignKeyConstraint(['page_table_id'], [u'page_table.id'], name=u'fk_cell_page_table_id', onupdate=u'CASCADE', ondelete=u'CASCADE'),
    sa.PrimaryKeyConstraint('id', name=u'cell_pkey')
    )
    op.create_table('metadata',
    sa.Column('id', sa.INTEGER(), server_default="nextval('metadata_id_seq'::regclass)", nullable=False),
    sa.Column('page_table_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('page_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('book_id', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('source', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('footer', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('subtitle', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('subject', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['book_id'], [u'book.id'], name=u'fk_metadata_book_id', onupdate=u'CASCADE', ondelete=u'CASCADE'),
    sa.ForeignKeyConstraint(['page_id'], [u'page.id'], name=u'fk_metadata_page_id', onupdate=u'CASCADE', ondelete=u'CASCADE'),
    sa.ForeignKeyConstraint(['page_table_id'], [u'page_table.id'], name=u'fk_metadata_page_table_id', onupdate=u'CASCADE', ondelete=u'CASCADE'),
    sa.PrimaryKeyConstraint('id', name=u'metadata_pkey')
    )
    op.create_table('page_table',
    sa.Column('id', sa.INTEGER(), server_default="nextval('page_table_id_seq'::regclass)", nullable=False),
    sa.Column('page_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('book_id', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('initialDate', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('finalDate', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('local_url', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('top_pos', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('left_pos', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('right_pos', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('bottom_pos', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['book_id'], [u'book.id'], name=u'fk_page_table_book_id', onupdate=u'CASCADE', ondelete=u'CASCADE'),
    sa.ForeignKeyConstraint(['page_id'], [u'page.id'], name=u'fk_page_table_page_id', onupdate=u'CASCADE', ondelete=u'CASCADE'),
    sa.PrimaryKeyConstraint('id', name=u'page_table_pkey')
    )
    ### end Alembic commands ###
