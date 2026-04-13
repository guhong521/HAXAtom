"""add disabled_models to model_configs

Revision ID: 002
Revises: 001
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 添加 disabled_models 列
    op.add_column('model_configs', sa.Column('disabled_models', sa.JSON(), nullable=True))
    
    # 更新默认值为空列表（对于现有记录）
    op.execute("UPDATE model_configs SET disabled_models = '[]' WHERE disabled_models IS NULL")


def downgrade() -> None:
    # 删除 disabled_models 列
    op.drop_column('model_configs', 'disabled_models')
