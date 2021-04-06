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

POSTGRESQL = {
    "dsn": "postgres://postgres:postgres@127.0.0.1:5432/xway",
    "host": "127.0.0.2",
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