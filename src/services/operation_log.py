import json
from typing import AsyncIterator
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.status import HTTP_200_OK, HTTP_300_MULTIPLE_CHOICES

from db.crud.operation_log import OperationLog as OperationLogCRUD
from db.crud.users import User
from models.errors import HttpNotFound, HttpServerError

# TODO support multiple level(like: user/1/xxx/1) in the future
GET_DATA_CLASS_MAP = {
    # router: crud classname, crud method
    "users": {"classname": User, "method": "get_user_by_id"},
    "owner_user": {"classname": User, "method": "get_user_by_id"},
    "register": {"classname": User, "method": "get_user_by_id"},
}

RECORD_METHOD = {
    "PUT": True,
    "POST": True,
    "DELETE": True,
}


async def get_path_segs(path: str):
    return path.split("/")


async def gen_btree_path(path_segs: list):
    path = ".".join(path_segs[3:])
    # if len(path_segs) == 4 and id:
    #     path = "{}.{}".format(path, id)

    return path


async def get_data(name: str, id: int, pgpool):
    if name not in GET_DATA_CLASS_MAP.keys():
        raise HttpNotFound("bad uri")

    info = GET_DATA_CLASS_MAP[name]
    obj = info['classname'](pgpool)
    func = getattr(obj, info['method'])

    return await func(id)


async def get_old_data(request: Request):
    # generate path: /api/v{api version}/xx/{id}
    path_segs = await get_path_segs(request['path'])
    if len(path_segs) < 5:
        raise HttpNotFound("bad uri")

    id = int(path_segs[-1])
    if id <= 0:
        raise HttpNotFound("bad uri")

    name = str(path_segs[-2])
    if not name:
        raise HttpNotFound("bad uri")

    # btree_path = gen_btree_path(path_segs)
    return await get_data(name, id, request.app.state.pgpool)


async def set_new_data(request: Request, data: str):
    request.state.oplog['new'] = data


async def set_new_data_id(request: Request, id: int):
    request.state.oplog['id'] = id


async def get_new_data_id(request: Request):
    return request.state.oplog['id']


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


async def enable(request: Request):
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


async def read_bytes(generator: AsyncIterator[bytes]) -> bytes:
    body = b""
    async for data in generator:
        body += data
    return body


async def get_body_from_streaming_response(streaming: StreamingResponse):
    return await read_bytes(streaming.body_iterator)


async def record(request: Request, response: StreamingResponse):
    if response.status_code < HTTP_200_OK \
            or response.status_code >= HTTP_300_MULTIPLE_CHOICES:
        return response

    try:
        oplog_enable = request.state.oplog['enable']
    except AttributeError:
        oplog_enable = False

    if not oplog_enable:
        return response

    method = request.method
    if not is_need_record(method):
        return response

    if method == "PUT" or method == "POST":
        if response.headers['content-type'] != "application/json" \
                and response.media_type != "application/json":
            # TODO warning log
            pass

        content = await get_body_from_streaming_response(response)
        response = Response(
            content,
            response.status_code,
            response.headers,
            response.media_type,
            response.background
        )

    pool = request.app.state.pgpool

    oplog = request.state.oplog
    path_segs = await get_path_segs(request['path'])

    old: str = None
    if method == "PUT" or method == "DELETE":
        old = oplog['old'].json()

    new: str = None
    if method == "PUT" or method == "POST":
        body = response.body.decode("utf-8")
        body_json = json.loads(body)
        id = body_json['id']

        if method == "POST":
            path_segs.append(str(id))

        new = await get_data(path_segs[-2], id, pool)
        new = new.json()

    # record oplog to db
    oplog_crud = OperationLogCRUD(pool)
    path = await gen_btree_path(path_segs)
    current_user = request.state.current_user

    creator = 0
    if current_user:
        creator = current_user.id

    await oplog_crud.add_operation_log(op=method, path=path, new=new,
                                       old=old, creator=creator)

    return response
