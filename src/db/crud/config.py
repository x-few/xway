from db.crud.base import Base
# from models.config import Config as ConfigModel

class Config(Base):
    async def get_all_default_config(self):
        records = await self.exec("get_all_default_config")
        if records:
            print(records)
            return {record[0]: record[1] for record in records}

        # empty
        return dict()
