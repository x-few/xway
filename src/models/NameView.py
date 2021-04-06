from sanic.views import HTTPMethodView
from sanic.response import text

class NameView(HTTPMethodView):

  async def get(self, request, name):
    return text("Hello {}".format(name))

    async def post(self, request, name):
        return text("Hello {}".format(name))

    async def put(self, request, name):
        return text("Hello {}".format(name))

