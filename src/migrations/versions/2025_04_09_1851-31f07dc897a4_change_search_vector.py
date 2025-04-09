"""change search_vector

Revision ID: 31f07dc897a4
Revises: e39102b576e7
Create Date: 2025-04-09 18:51:38.455402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import storage.file_type


# revision identifiers, used by Alembic.
revision: str = '31f07dc897a4'
down_revision: Union[str, None] = 'e39102b576e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Удаляем старый столбец (если нужно)
    op.drop_column('study_material', 'search_vector')

    # Добавляем новый вычисляемый столбец
    op.add_column('study_material',
                  sa.Column('search_vector',
                            sa.dialects.postgresql.TSVECTOR(),
                            sa.Computed("to_tsvector('russian', name || ' ' || text)", persisted=True),
                            nullable=False
                            )
                  )

    # Создаем индекс
    op.create_index('study_material_search_idx', 'study_material', ['search_vector'],
                    postgresql_using='gin')


def downgrade():
    op.drop_index('study_material_search_idx', table_name='study_material')
    op.drop_column('study_material', 'search_vector')

    # Вернуть обычный столбец при откате (если нужно)
    op.add_column('study_material',
                  sa.Column('search_vector',
                            sa.dialects.postgresql.TSVECTOR(),
                            nullable=True
                            )
                  )
