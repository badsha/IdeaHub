"""Add workspace URL field and reporting schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create reporting schema
    op.execute('CREATE SCHEMA IF NOT EXISTS reporting')
    
    # Add URL column to workspaces table
    op.add_column('workspaces', sa.Column('url', sa.String(255), nullable=True))
    
    # Create unique index on workspace URL
    op.create_index('ix_workspaces_url', 'workspaces', ['url'], unique=True)


def downgrade() -> None:
    # Drop workspace URL column
    op.drop_index('ix_workspaces_url', table_name='workspaces')
    op.drop_column('workspaces', 'url')
    
    # Drop reporting schema
    op.execute('DROP SCHEMA IF EXISTS reporting')
