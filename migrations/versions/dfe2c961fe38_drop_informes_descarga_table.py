"""drop informes_descarga table

Revision ID: dfe2c961fe38
Revises: 6dd28b371014
Create Date: 2026-04-27 17:56:53.349587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfe2c961fe38'
down_revision = '6dd28b371014'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('informes_descarga')


def downgrade():
    op.create_table('informes_descarga',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha_descarga', sa.DateTime(), nullable=True),
    sa.Column('toneladas_entregadas_reales', sa.Float(), nullable=False),
    sa.Column('porcentaje_humedad', sa.Float(), nullable=True),
    sa.Column('viaje_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['viaje_id'], ['viajes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('viaje_id')
    )
