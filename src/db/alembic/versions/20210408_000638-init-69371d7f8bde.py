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
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, index=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False,),
        sa.Column("status", sa.Text, nullable=False, default="enable"),
        *timestamps(),
    )

    create_updated_trigger(table_name)


def upgrade():
    create_updated_function()
    create_users_table()


def downgrade():
    op.drop_table('users')
    drop_updated_function()
