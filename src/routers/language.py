from fastapi import APIRouter, Depends, Body, Request

from models.language import LanguageInResponse, LanguageInDB
from db.crud.language import Language as LanguageCRUD
from services.localization import get_gettext

router = APIRouter()


@router.get("/languages", response_model=LanguageInResponse)
async def get_languages(
        request: Request,
        _=Depends(get_gettext),
) -> LanguageInResponse:
    lang_crud = LanguageCRUD(request.app.state.pgpool)
    langs: LanguageInDB = await lang_crud.get_languages()
    return LanguageInResponse(
        data=langs,
    )
