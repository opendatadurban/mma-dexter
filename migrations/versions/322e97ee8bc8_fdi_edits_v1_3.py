"""FDI edits v1.3

Revision ID: 322e97ee8bc8
Revises: 455e2ffe5c2f
Create Date: 2016-11-14 09:56:00.187653

"""

# revision identifiers, used by Alembic.
revision = '322e97ee8bc8'
down_revision = '455e2ffe5c2f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('investments', sa.Column('invest_origin_city', sa.String(length=50), nullable=True))
    op.add_column('investments', sa.Column('value2', sa.Float(), nullable=True))
    op.add_column('investments', sa.Column('value_unit_id2', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_investments_value_unit_id2'), 'investments', ['value_unit_id2'], unique=False)
    op.create_foreign_key(None, 'investments', 'value_units', ['value_unit_id2'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'investments_ibfk_11', 'investments', type_='foreignkey')
    op.drop_index(op.f('ix_investments_value_unit_id2'), table_name='investments')
    op.drop_column('investments', 'value_unit_id2')
    op.drop_column('investments', 'value2')
    op.drop_column('investments', 'invest_origin_city')
    ### end Alembic commands ###