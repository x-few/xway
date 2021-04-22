"""init

Revision ID: 69371d7f8bde
Revises:
Create Date: 2021-04-08 00:06:38.939036

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from typing import Tuple

# revision identifiers, used by Alembic.
revision = '69371d7f8bde'
down_revision = None
branch_labels = None
depends_on = None

def create_updated_function() -> None:
    op.execute(
        """
        CREATE FUNCTION update_updated_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def drop_updated_function() -> None:
    op.execute("DROP FUNCTION update_updated_column")


def create_updated_trigger(table_name) -> None:
    op.execute(
        """
        CREATE TRIGGER update_{0}_modtime
            BEFORE UPDATE
            ON {0}
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_column();
        """.format(table_name)
    )


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )


def create_users_table() -> None:
    table_name = "users"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, index=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False,),
        sa.Column("status", sa.Text, nullable=False, default="enable"),
        *timestamps(),
    )

    create_updated_trigger(table_name)


# this table is for all users
def create_default_config_table() -> None:
    table_name = "default_config"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("key", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("value", sa.Text, nullable=False),
        sa.Column("comment", sa.Text, nullable=True),
    )

def insert_default_config_table() -> None:
    config_table = sa.table('default_config',
        sa.Column("key", sa.Text),
        sa.Column("value", sa.Text),
        sa.Column("comment", sa.Text),
    )

    op.bulk_insert(config_table,
        [
            {'key':'jwt_subject', 'value': 'access', 'comment': 'jwt_subject for user authentication'},
            {'key':'jwt_algorithm', 'value': 'HS256', 'comment': 'jwt algorithm'},
            {'key':'jwt_access_token_expire', 'value': '648000', 'comment': 'access token expire second'},
            {'key':'secret_key', 'value': '12345abcde', 'comment': 'TODO: Generated at initialization'},
        ]
    )


def upgrade():
    create_updated_function()
    create_users_table()
    create_default_config_table()
    insert_default_config_table()


def downgrade():
    op.drop_table('default_config')
    op.drop_table('users')
    drop_updated_function()
