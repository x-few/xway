import os
from sanic import Sanic
from sanic.response import json
from blueprints.v1 import bpv1
from interfaces import interfaces

def get_my_path():
    """
    获取当前文件所在的路径
    :return:
    """
    return os.path.dirname(os.path.realpath(__file__))


app = Sanic("iwaf-backend")
app.config.from_pyfile("{}/../conf/config.py".format(get_my_path()))


@app.listener('before_server_start')
async def before_server_start(app, loop):
    print("---in before_server_start---")
    pass


@app.listener('after_server_start')
async def after_server_start(app, loop):
    print("---in after_server_start---")
    pass


@app.listener('before_server_stop')
async def before_server_stop(app, loop):
    print("---in before_server_stop---")
    pass


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    print("---in after_server_stop---")
    pass


@app.middleware('request')
async def request_middleware(request):
    print("---in request_middleware---")
    pass


@app.middleware('response')
async def response_middleware(request, response):
    print("---in response_middleware---")
    pass


@app.route("/", methods=["GET"])
async def helloword(request):
    return json({"hello": "world"})

def response(data="", code=0, message="success"):
    return json({
        "code": code,
        "message": message,
        "data": data
    })


@app.route("/api", methods=["POST"])
async def api(request):
    """
    {
      "action": "add_rule", ...
      "uid": "user id",
      "data": "request data",
    }
    :param request:
    :return:
    """
    req = request.json
    if 'interface' not in req:
        return response("interface not found", 400, "error")
    print(req)
    if 'data' not in req:
        return response("data not found", 400, "error")
    interface = interfaces[req['interface']]
    ret = await interface(req['data'])
    return response(ret)


if __name__ == "__main__":
    app.blueprint(bpv1)
    app.run(**app.config.APP)