
from typing import Optional
from starlette import status as slstatus
from fastapi import Depends, HTTPException, Security

from db.crud.base import Base
from db.queries import queries
from models.language import LanguageInDB
from models.errors import HttpServerError, HttpClientError, HttpForbidden, HttpNotFound


class Language(Base):
    async def get_languages(self):

        records = await self.exec("get_languages")
        print("records = ", records)
        if records:
            self.langs = [LanguageInDB(**record) for record in records]

        return self.langs

    async def to_dict(self):
        if not self.langs:
            self.get_languages()

        self.lang_dict = {
            lang['code']: lang for lang in self.langs
        }
