BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 0001

CREATE EXTENSION if not exists ltree;;

CREATE FUNCTION update_updated_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';;

CREATE TABLE users (
    id BIGSERIAL NOT NULL, 
    username TEXT NOT NULL, 
    email TEXT, 
    salt TEXT NOT NULL, 
    password TEXT NOT NULL, 
    status INTEGER NOT NULL, 
    type TEXT NOT NULL, 
    creator BIGINT NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_users_username ON users (username);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE TRIGGER update_users_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_column();;

CREATE TABLE default_config (
    id BIGSERIAL NOT NULL, 
    key TEXT NOT NULL, 
    value TEXT NOT NULL, 
    comment TEXT, 
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_default_config_key ON default_config (key);

CREATE TABLE operation_log (
    id BIGSERIAL NOT NULL, 
    op VARCHAR(16) NOT NULL, 
    creator BIGINT NOT NULL, 
    path LTREE, 
    "new" JSONB, 
    "old" JSONB, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE release_log (
    id BIGSERIAL NOT NULL, 
    creator BIGINT NOT NULL, 
    start_opid BIGINT NOT NULL, 
    end_opid BIGINT NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE language (
    id BIGSERIAL NOT NULL, 
    name TEXT NOT NULL, 
    code VARCHAR(16) NOT NULL, 
    domain TEXT NOT NULL, 
    localedir TEXT NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE login_log (
    id BIGSERIAL NOT NULL, 
    user_id BIGINT NOT NULL, 
    host TEXT, 
    type INTEGER, 
    status INTEGER NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE permission (
    id BIGSERIAL NOT NULL, 
    name TEXT NOT NULL, 
    uri TEXT NOT NULL, 
    description TEXT, 
    method INTEGER, 
    status INTEGER, 
    creator BIGINT NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (uri, method), 
    UNIQUE (name)
);

CREATE TABLE role (
    id BIGSERIAL NOT NULL, 
    name TEXT NOT NULL, 
    description TEXT, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE user_role (
    id BIGSERIAL NOT NULL, 
    user_id BIGINT NOT NULL, 
    role_id BIGINT NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id), 
    FOREIGN KEY(role_id) REFERENCES role (id)
);

CREATE TABLE role_permission (
    id BIGSERIAL NOT NULL, 
    role_id BIGINT NOT NULL, 
    permission_id BIGINT NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(role_id) REFERENCES role (id), 
    FOREIGN KEY(permission_id) REFERENCES permission (id)
);

CREATE TABLE user_group (
    id BIGSERIAL NOT NULL, 
    name TEXT NOT NULL, 
    description TEXT, 
    creator BIGINT NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE user_group_role (
    id BIGSERIAL NOT NULL, 
    group_id BIGINT NOT NULL, 
    role_id BIGINT NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(group_id) REFERENCES user_group (id), 
    FOREIGN KEY(role_id) REFERENCES role (id)
);

INSERT INTO users (username, email, salt, type, password, status, creator) VALUES ('admin', 'admin@xway.com', '$2b$12$0nGbQiYmgsz5pYm0gS0EBu', 'admin', '$2b$12$S9uiHIDezEpJdFzbBcku6.EpE6Ozc4aOkUCG0ZDTdKirpl03jWQ2O', NULL, 0);

INSERT INTO default_config (key, value, comment) VALUES ('jwt_subject', 'access', 'jwt_subject for user authentication');

INSERT INTO default_config (key, value, comment) VALUES ('jwt_algorithm', 'HS256', 'jwt algorithm');

INSERT INTO default_config (key, value, comment) VALUES ('jwt_access_token_expire', '604800', 'one week, access token expire second');

INSERT INTO default_config (key, value, comment) VALUES ('secret_key', '12345abcde', 'TODO: Generated at initialization');

INSERT INTO default_config (key, value, comment) VALUES ('jwt_token_prefix', 'bearer', 'jwt token prefix');

INSERT INTO default_config (key, value, comment) VALUES ('auth_header', 'Authorization', 'http header of authorization');

INSERT INTO language (name, code, domain, localedir) VALUES ('简体中文', 'zh_CN', NULL, NULL);

INSERT INTO language (name, code, domain, localedir) VALUES ('English(US)', 'en_US', NULL, NULL);

INSERT INTO alembic_version (version_num) VALUES ('0001') RETURNING alembic_version.version_num;

COMMIT;

