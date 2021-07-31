from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from db.crud.operation_log import OperationLog as OperationLogCRUD
from db.crud.users import User
from models.errors import HttpNotFound, HttpServerError

# TODO support multiple level(like: user/1/xxx/1) in the future
GET_DATA_CLASS_MAP = {
    # router: crud classname, crud method
    "users": { "classname": User, "method": "get_user_by_id"},
    "owner_user": { "classname": User, "method": "get_user_by_id"},
    "register": { "classname": User, "method": "get_user_by_id"},
}

RECORD_METHOD = {
    "PUT": True,
    "POST": True,
    "DELETE": True,
}

async def get_path_segs(path: str):
    return path.split("/")

# async def get_path(request: Request):
#     pass

async def get_data(module_name, id, dbpool):
    info = GET_DATA_CLASS_MAP[module_name]
    obj = info['classname'](dbpool)
    func = getattr(obj, info['method'])
    # try:
    return await func(id)
    # except Exception as e:
    #     print(repr(e))

    return None


# async def get_data(module_name, id, dbpool):
#     func = await get_func(module_name, id)
#     return

async def gen_btree_path(path_segs: list, id):
    path = ".".join(path_segs[3:])
    if len(path_segs) == 4 and id:
        path = "{}.{}".format(path, id)

    return path


async def get_old_data(request: Request):
    # generate path: /api/v{api version}/xx/{id}
    path_segs = await get_path_segs(request['path'])
    if len(path_segs) < 5:
        # TODO ...
        print("---ERROR---")
        return

    # btree_path = gen_btree_path(path_segs)
    # get old data from db
    data = await get_data(path_segs[3], int(path_segs[4]), request.app.state.pgpool)
    # request.state.oplog['old'] = data   # note: not string

    return data


async def set_new_data(request: Request, data: str):
    request.state.oplog['new'] = data


async def set_new_data_id(request: Request, id: int):
    request.state.oplog['id'] = id


async def get_new_data_id(request: Request):
    return request.state.oplog['id']


async def init(request: Request):
    request.state.oplog = dict()

    # check http mathod
    method = request.method
    if method == "PUT" or method == "DELETE":
        # backup old data
        request.state.oplog['old'] = await get_old_data(request)
        request.state.oplog['enable'] = True
    elif method == "POST":
        request.state.oplog['enable'] = True
    else:
        request.state.oplog['enable'] = False


def get_data_id(path_segs, oplog):
    if len(path_segs) > 4:
        return int(path_segs[4])

    if 'id' in oplog:
        return oplog['id']

    raise HttpNotFound("id not found")


def is_need_record(method):
    if method in RECORD_METHOD:
        return True

    return False


async def record(request: Request, response: Response):
    if response.status_code < 200 or response.status_code >= 300:
        return

    try:
        oplog_enable = request.state.oplog['enable']
    except AttributeError:
        oplog_enable = False

    if not oplog_enable:
        return

    method = request.method
    if not is_need_record(method):
        return

    dbpool = request.app.state.pgpool

    oplog = request.state.oplog
    path_segs = await get_path_segs(request['path'])
    data_id = get_data_id(path_segs, oplog)

    old: str = None
    if method == "PUT" or method == "DELETE":
        old = oplog['old'].json()

    new: str = None
    if method == "PUT" or method == "POST":
        data = await get_data(path_segs[3], data_id, dbpool)
        new = data.json()

    # record oplog to db
    oplog_crud = OperationLogCRUD(dbpool)
    path = await gen_btree_path(path_segs, data_id)
    current_user = request.state.current_user

    owner = 0
    creator = 0
    if current_user:
        owner = current_user.owner or current_user.id
        creator = current_user.id

    await oplog_crud.add_oplog(op=method, path=path, new=new, old=old, owner=owner, creator=creator)


async def rollback(request: Request):
    # get all operation records that need to be rollback

    # do rollback

    # add new record
    pass