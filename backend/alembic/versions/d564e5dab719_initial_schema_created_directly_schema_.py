# script.py.mako
# Alembic revision script template

"""Initial schema created directly - Schema from models.py - 20250918_222128

Revision ID: d564e5dab719
Revises: 
Create Date: 2025-09-18 22:21:30.294418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd564e5dab719'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema"""
    pass


def downgrade() -> None:
    """Downgrade database schema"""
    pass