from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response


async def get_path(request: Request):
    pass

async def backup_old_data(request: Request):
    # generate path: /api/v{api version}/xx/{id}

    # get old data from db
    pass

async def init(request: Request):
    print("request['path'] = ", request['path'])
    print("request.url.path = ", request.url.path)
    request.state.oplog = dict()
    # check http mathod
    method = request.method
    if method == "PUT" or method == "DELETE":
        # backup old data
        # old_data =

        request.state.oplog['old_data'] = dict()
        request.state.oplog['enable'] = True
        pass
    elif method == "POST":
        request.state.oplog['enable'] = True
    else:
        request.state.oplog['enable'] = False


async def record(request: Request, response: Response):
    print("---record---")
    method = request.method
    if method == "POST":
        pass

async def rollback(request: Request):
    pass