from db.crud.base import Base
from models.language import LanguageInDB


class Language(Base):
    async def list(self):
        records = await self.exec("list_languages")
        # print("records = ", records)
        if records:
            self.langs = [LanguageInDB(**record) for record in records]

        return self.langs

    async def to_dict(self):
        if not self.langs:
            self.list()

        self.lang_dict = {
            lang['code']: lang for lang in self.langs
        }
