from fastapi import APIRouter, Depends, Body, Request

from models.language import LanguagesInResponse, LanguageInDB
from db.crud.language import Language as LanguageCRUD

router = APIRouter()


@router.get("/languages", response_model=LanguagesInResponse)
async def list_languages(
        request: Request,
) -> LanguagesInResponse:
    """Get all supported languages.

    Args:
        request (Request): http request.

    Returns:
        LanguagesInResponse: list of languages.
    """
    _ = request.state.get_gettext
    languages_crud = LanguageCRUD(request.app.state.pgpool)
    langs: LanguageInDB = await languages_crud.list_languages()
    return LanguagesInResponse(
        data=langs,
    )
