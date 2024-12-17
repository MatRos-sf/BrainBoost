"""init

Revision ID: 27cca1f759b1
Revises: 
Create Date: 2024-12-17 21:48:56.036242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '27cca1f759b1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('language', sa.Enum('PL', 'EN', name='language'), nullable=False),
    sa.Column('point', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('associative_changing_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('game_name', sa.Enum('RESULT_KEEPER', 'ASSOCIATIVE_CHANGING', name='gamename'), nullable=False),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('login_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('login_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('points_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('category', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('point', sa.Integer(), nullable=False),
    sa.Column('saved_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('result_keeper_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('game_name', sa.Enum('RESULT_KEEPER', 'ASSOCIATIVE_CHANGING', name='gamename'), nullable=False),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('associative_changing_session_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('points_earned', sa.Integer(), nullable=False),
    sa.Column('started_level', sa.Integer(), nullable=False),
    sa.Column('finished_level', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('finished_datetime', sa.DateTime(), nullable=False),
    sa.Column('wrong_answers', sa.Integer(), nullable=False),
    sa.Column('correct_answers', sa.Integer(), nullable=False),
    sa.Column('associative_changing_id', sa.Integer(), nullable=False),
    sa.Column('words', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_answers', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('amt_words', sa.Integer(), nullable=False),
    sa.Column('skip_answers', sa.Integer(), nullable=False),
    sa.Column('memorization_time', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['associative_changing_id'], ['associative_changing_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('result_keeper_session_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('points_earned', sa.Integer(), nullable=False),
    sa.Column('started_level', sa.Integer(), nullable=False),
    sa.Column('finished_level', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('finished_datetime', sa.DateTime(), nullable=False),
    sa.Column('wrong_answers', sa.Integer(), nullable=False),
    sa.Column('correct_answers', sa.Integer(), nullable=False),
    sa.Column('result_keeper_id', sa.Integer(), nullable=False),
    sa.Column('range_min', sa.Integer(), nullable=False),
    sa.Column('range_max', sa.Integer(), nullable=False),
    sa.Column('steps', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['result_keeper_id'], ['result_keeper_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('result_keeper_session_table')
    op.drop_table('associative_changing_session_table')
    op.drop_table('result_keeper_table')
    op.drop_table('points_table')
    op.drop_table('login_table')
    op.drop_table('associative_changing_table')
    op.drop_table('user_table')
    # ### end Alembic commands ###