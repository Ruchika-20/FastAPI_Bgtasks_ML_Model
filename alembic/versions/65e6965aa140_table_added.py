"""Table added

Revision ID: 65e6965aa140
Revises: e93b05d211f4
Create Date: 2023-01-18 16:00:16.491459

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '65e6965aa140'
down_revision = 'e93b05d211f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('job', 'updated_by',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('job', 'accuracy',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('job', 'estimated_time',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('job', 'download',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('job', 'download',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('job', 'estimated_time',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('job', 'accuracy',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('job', 'updated_by',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###
