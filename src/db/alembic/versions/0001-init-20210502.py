"""init.

Revision ID: 0001
Revises:
Create Date: 2021-05-02 23:01:00.322410

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from typing import Tuple
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import LtreeType
from sqlalchemy.engine.reflection import Inspector

from utils.const import AUTH_TYPE_OAUTH2_BEARER_JWT, \
    PERMISSIONS_STATUS_ENABLE, \
    PERMISSIONS_METHOD_ALL


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def create_extensions():
    op.execute("CREATE EXTENSION if not exists ltree;")


def drop_extensions():
    op.execute("DROP EXTENSION if exists ltree;")


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
        sa.Column("username", sa.Text, unique=True,
                  nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, index=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False,),
        sa.Column("status", sa.Integer, nullable=False,
                  default=1),  # 0: disabled, 1: enabled
        sa.Column("creator", sa.Integer, nullable=False),
        *timestamps(),
    )

    create_updated_trigger(table_name)


def insert_default_users() -> None:
    table_name = "users"
    table = sa.table(
        table_name,
        sa.Column("username", sa.Text),
        sa.Column("email", sa.Text),
        sa.Column("salt", sa.Text),
        sa.Column("password", sa.Text),
        sa.Column("status", sa.Integer, default=1),
        sa.Column("creator", sa.Integer, nullable=False),
    )

    op.bulk_insert(table,
                   [
                       {
                           'username': 'admin',
                           'email': 'admin@xway.com',
                           'salt': '$2b$12$0nGbQiYmgsz5pYm0gS0EBu',
                           # password: pwd@xway
                           'password': '$2b$12$S9uiHIDezEpJdFzbBcku6.EpE6Ozc4aOkUCG0ZDTdKirpl03jWQ2O',
                           'creator': 0,   # default user
                       },
                   ]
                   )


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
    table_name = "default_config"
    table = sa.table(
        table_name,
        sa.Column("key", sa.Text),
        sa.Column("value", sa.Text),
        sa.Column("comment", sa.Text),
    )

    op.bulk_insert(table,
                   [
                       {'key': 'jwt_subject', 'value': 'access',
                           'comment': 'jwt_subject for user authentication'},
                       {'key': 'jwt_algorithm', 'value': 'HS256',
                           'comment': 'jwt algorithm'},
                       {'key': 'jwt_access_token_expire', 'value': '604800',
                           'comment': 'one week, access token expire second'},
                       {'key': 'secret_key', 'value': '12345abcde',
                           'comment': 'TODO: Generated at initialization'},
                       {'key': 'jwt_token_prefix', 'value': 'bearer',
                           'comment': 'jwt token prefix'},
                       {'key': 'auth_header', 'value': 'Authorization',
                           'comment': 'http header of authorization'},
                   ]
                   )


def create_operation_log_table() -> None:
    table_name = "operation_log"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("op", sa.String(length=16), nullable=False, ),
        sa.Column("creator", sa.Integer, nullable=False),
        sa.Column("path", LtreeType, nullable=True),
        sa.Column("new", JSONB, nullable=True),
        sa.Column("old", JSONB, nullable=True),
        *timestamps(),
    )


def create_release_log_table() -> None:
    table_name = "release_log"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("creator", sa.Integer, nullable=False),
        sa.Column("start_opid", sa.Integer, nullable=False),
        sa.Column("end_opid", sa.Integer, nullable=False),
        *timestamps(),
    )


def create_language_table() -> None:
    table_name = "language"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),      # 简体中文、English(US)
        sa.Column("code", sa.String(length=16),
                  nullable=False),      # zh_CN、en_US
        sa.Column("domain", sa.Text, nullable=False, default="base"),
        sa.Column("localedir", sa.Text, nullable=False, default="locales"),
    )


def insert_language_table() -> None:
    table_name = "language"
    table = sa.table(
        table_name,
        sa.Column("name", sa.Text),
        sa.Column("code", sa.Text),
        sa.Column("domain", sa.Text, default="base"),
        sa.Column("localedir", sa.Text, default="locales"),
    )

    op.bulk_insert(table,
                   [
                       {'name': '简体中文', 'code': 'zh_CN'},
                       {'name': 'English(US)', 'code': 'en_US'},
                   ]
                   )


def get_all_tables():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    return tables


def create_login_record_table() -> None:
    table_name = "login_record"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("creator", sa.Integer, sa.ForeignKey(
            'users.id'), nullable=False),
        sa.Column("host", sa.Text, nullable=True),
        sa.Column("type", sa.Integer, nullable=True,
                  default=AUTH_TYPE_OAUTH2_BEARER_JWT),
        sa.Column("token", sa.Text, nullable=True),
        sa.Column(
            "created",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )


def create_permission_table() -> None:
    table_name = "permission"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("uri", sa.Text, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("method", sa.Integer, nullable=True,
                  default=PERMISSIONS_METHOD_ALL),
        sa.Column("status", sa.Integer, nullable=True,
                  default=PERMISSIONS_STATUS_ENABLE),
        *timestamps(),
    )


def create_role_table() -> None:
    table_name = "role"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        *timestamps(),
    )


def create_user_role_table() -> None:
    table_name = "user_role"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey(
            'users.id'), nullable=False, ),
        sa.Column("role_id", sa.Integer, sa.ForeignKey(
            'role.id'), nullable=False),
        *timestamps(),
    )


def create_role_permission_table() -> None:
    table_name = "role_permission"
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("role_id", sa.Integer, sa.ForeignKey(
            'role.id'), nullable=False),
        sa.Column("permission_id", sa.Integer, sa.ForeignKey(
            'permission.id'), nullable=False),
        *timestamps(),
    )


def upgrade():
    # tables = get_all_tables()
    create_extensions()
    create_updated_function()
    create_users_table()
    insert_default_users()
    create_default_config_table()
    insert_default_config_table()
    create_operation_log_table()
    create_release_log_table()
    create_language_table()
    insert_language_table()
    create_login_record_table()
    create_permission_table()
    create_role_table()
    create_user_role_table()
    create_role_permission_table()


def downgrade():
    op.drop_table('role_permission')
    op.drop_table('user_role')
    op.drop_table('role')
    op.drop_table('permission')
    op.drop_table('login_record')
    op.drop_table('language')
    op.drop_table('release_log')
    op.drop_table('operation_log')
    op.drop_table('default_config')
    op.drop_table('users')
    drop_updated_function()
    drop_extensions()
