APP = {
    "host": "0.0.0.0",
    "port": 9394,
    "access_log": True,
    "debug": True,
    "workers": 1,
    "backlog": 128,
    "lifespan": "on",
    "reload": True,
}

ROUTER_PREFIX = "/api"

# openssl rand -hex 32
SECRET_KEY = "5a5c2b24d662362c1f36e083dd38d8b8724a9523a946bc68c31f9245b46da855"

JWT = {
    "SUBJECT": "access",
    "ALGORITHM": "HS256",
    "TOKEN_EXPIRE": 24 * 60 * 60,   # 1 day
}

POSTGRESQL = {
    # "dsn": "postgres://postgres:postgres@127.0.0.1:5432/xway",
    "host": "127.0.0.1",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "passfile": None,
    "database": "xway",
    "min_size": 10,
    "max_size": 100,
    "timeout": 60,
    "command_timeout": 60,
}


REDIS = {}

MONGODB = {}

DBSQL = {}