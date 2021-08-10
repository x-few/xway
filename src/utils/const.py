
USER_TYPE_SYSTEM_MAINTAINER = 0
USER_TYPE_ADMIN_USER = 1
USER_TYPE_NORMAL_USER = 2

USER_STATUS_ENABLED = 1
USER_STATUS_DISABLED = 2

AUTH_TYPE_OAUTH2_BEARER_JWT = 1
AUTH_TYPE_OAUTH2_BEARER_JWT_PREFIX = "bearer"

AUTH_TYPES = {
    AUTH_TYPE_OAUTH2_BEARER_JWT_PREFIX : AUTH_TYPE_OAUTH2_BEARER_JWT
}

PERMISSIONS_STATUS_ENABLE = 1
PERMISSIONS_STATUS_DISABLE = 2
PERMISSIONS_STATUS_DEPRECATE = 3

PERMISSIONS_METHOD_ALL = 1
PERMISSIONS_METHOD_GET = 2
PERMISSIONS_METHOD_POST = 3
PERMISSIONS_METHOD_PUT = 4
PERMISSIONS_METHOD_DELETE = 5


def is_system_maintainer(user_type):
    return user_type == USER_TYPE_SYSTEM_MAINTAINER

def is_admin_user(user_type):
    return user_type == USER_TYPE_ADMIN_USER

def is_normal_user(user_type):
    return user_type == USER_TYPE_NORMAL_USER

def get_user_type_system_maintainer():
    return USER_TYPE_SYSTEM_MAINTAINER

def get_user_type_admin_user():
    return USER_TYPE_ADMIN_USER

def get_user_type_normal_user():
    return USER_TYPE_NORMAL_USER