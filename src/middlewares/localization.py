import gettext
import typing

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from services.localization import get_gettext


class LocalizationMiddleware(BaseHTTPMiddleware):
    """
    creates gettext by Accept-Language and save to request.state.
    """

    async def dispatch(self, request: Request, call_next):
        language_code = request.headers.get('accept-language')
        if language_code:
            language_code = language_code.split(',')[0]

        request.state.language = language_code
        request.state.get_gettext = await get_gettext(request)

        response = await call_next(request)
        return response
