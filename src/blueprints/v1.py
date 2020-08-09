
from sanic import Blueprint
from sanic.response import text

bpv1 = Blueprint('v1', url_prefix='/api', version=1)

@bpv1.route('/', methods=["POST"])
async def api_v1_root(request):
    return text('Welcome to version 1 of our documentation')