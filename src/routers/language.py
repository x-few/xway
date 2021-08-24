from fastapi import APIRouter, Depends, Body, Request

from models.language import LanguagesInResponse, LanguageInDB
from db.crud.language import Language as LanguageCRUD
from services.localization import get_gettext

router = APIRouter()


@router.get("/languages", response_model=LanguagesInResponse)
async def list_languages(
        request: Request,
        _=Depends(get_gettext),
) -> LanguagesInResponse:
    """Get all supported languages.

    Args:
        request (Request): http request.
        _ ([type], optional): translation function. Defaults to Depends(get_gettext).

    Returns:
        LanguagesInResponse: list of languages.
    """
    languages_crud = LanguageCRUD(request.app.state.pgpool)
    langs: LanguageInDB = await languages_crud.list_languages()
    return LanguagesInResponse(
        data=langs,
    )
