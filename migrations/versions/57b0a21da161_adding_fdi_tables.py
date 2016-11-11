"""adding FDI tables

Revision ID: 57b0a21da161
Revises: 3ac1923eb5b3
Create Date: 2016-10-07 10:08:04.592892

"""

# revision identifiers, used by Alembic.
revision = '57b0a21da161'
down_revision = '3ac1923eb5b3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currencies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currencies_name'), 'currencies', ['name'], unique=True)
    op.create_table('investment_locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_investment_locations_name'), 'investment_locations', ['name'], unique=True)
    op.create_table('investment_origins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_investment_origins_name'), 'investment_origins', ['name'], unique=True)
    op.create_table('investment_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_investment_types_name'), 'investment_types', ['name'], unique=True)
    op.create_table('phases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_phases_name'), 'phases', ['name'], unique=True)
    op.create_table('sectors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=130), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sectors_name'), 'sectors', ['name'], unique=True)
    op.create_table('investments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('temp_opps', sa.Integer(), nullable=True),
    sa.Column('perm_opps', sa.Integer(), nullable=True),
    sa.Column('company', sa.String(length=1024), nullable=True),
    sa.Column('government', sa.String(length=1024), nullable=True),
    sa.Column('additional_place', sa.String(length=1024), nullable=True),
    sa.Column('investment_begin', sa.Date(), nullable=True),
    sa.Column('investment_end', sa.Date(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=True),
    sa.Column('phase_id', sa.Integer(), nullable=True),
    sa.Column('invest_origin_id', sa.Integer(), nullable=True),
    sa.Column('invest_loc_id', sa.Integer(), nullable=True),
    sa.Column('invest_type_id', sa.Integer(), nullable=True),
    sa.Column('sector_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    sa.ForeignKeyConstraint(['doc_id'], ['documents.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['invest_loc_id'], ['investment_locations.id'], ),
    sa.ForeignKeyConstraint(['invest_origin_id'], ['investment_origins.id'], ),
    sa.ForeignKeyConstraint(['invest_type_id'], ['investment_types.id'], ),
    sa.ForeignKeyConstraint(['phase_id'], ['phases.id'], ),
    sa.ForeignKeyConstraint(['sector_id'], ['sectors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_investments_currency_id'), 'investments', ['currency_id'], unique=False)
    op.create_index(op.f('ix_investments_doc_id'), 'investments', ['doc_id'], unique=False)
    op.create_index(op.f('ix_investments_invest_loc_id'), 'investments', ['invest_loc_id'], unique=False)
    op.create_index(op.f('ix_investments_invest_origin_id'), 'investments', ['invest_origin_id'], unique=False)
    op.create_index(op.f('ix_investments_invest_type_id'), 'investments', ['invest_type_id'], unique=False)
    op.create_index(op.f('ix_investments_investment_begin'), 'investments', ['investment_begin'], unique=False)
    op.create_index(op.f('ix_investments_investment_end'), 'investments', ['investment_end'], unique=False)
    op.create_index(op.f('ix_investments_name'), 'investments', ['name'], unique=False)
    op.create_index(op.f('ix_investments_phase_id'), 'investments', ['phase_id'], unique=False)
    op.create_index(op.f('ix_investments_sector_id'), 'investments', ['sector_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('investments')
    op.drop_table('sectors')
    op.drop_table('phases')
    op.drop_table('investment_types')
    op.drop_table('investment_origins')
    op.drop_table('investment_locations')
    op.drop_table('currencies')
    ### end Alembic commands ###