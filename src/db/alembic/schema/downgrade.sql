BEGIN;

-- Running downgrade 0001 -> 

DROP TABLE user_group_role;

DROP TABLE user_group;

DROP TABLE role_permission;

DROP TABLE user_role;

DROP TABLE role;

DROP TABLE permission;

DROP TABLE login_log;

DROP TABLE language;

DROP TABLE release_log;

DROP TABLE operation_log;

DROP TABLE default_config;

DROP TABLE users;

DROP FUNCTION update_updated_column;

DROP EXTENSION if exists ltree;;

DELETE FROM alembic_version WHERE alembic_version.version_num = '0001';

DROP TABLE alembic_version;

COMMIT;

