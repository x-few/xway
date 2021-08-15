import gettext
import typing
from fastapi import FastAPI
from starlette.requests import Request

from db.crud.language import Language as LanguageCRUD


async def init_translation_object(app: FastAPI) -> None:
    # get languages from db
    languages_crud = LanguageCRUD(app.state.pgpool)
    langs = await languages_crud.list()
    app.state.languages = dict()
    for lang in langs:
        gnu = gettext.translation(
            lang.domain,
            localedir=lang.localedir,
            languages=[lang.code]
        )
        # We can’t use this because the language required for each request may be different
        # gnu.install()
        app.state.languages[lang.code] = gnu.gettext


# dependency
async def get_gettext(request: Request):
    langs = request.app.state.languages
    code = request.state.language

    if code not in langs.keys():
        code = "zh_CN"

    return langs[code]
