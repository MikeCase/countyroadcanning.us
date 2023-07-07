"""empty message

Revision ID: 9c35b2965297
Revises: 891db5f233b4
Create Date: 2023-07-06 18:16:39.756407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c35b2965297'
down_revision = '891db5f233b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('soldproducts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sale_price', sa.Double(), nullable=True),
    sa.Column('sale_date', sa.DateTime(), nullable=True),
    sa.Column('sale_qty', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('sold_product')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sold_product',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('sale_price', sa.DOUBLE(), nullable=True),
    sa.Column('sale_date', sa.DATETIME(), nullable=True),
    sa.Column('sale_qty', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('soldproducts')
    # ### end Alembic commands ###
