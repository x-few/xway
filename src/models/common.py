import datetime

from pydantic import BaseModel, Field, validator


class DateTimeModel(BaseModel):
    created: datetime.datetime = None  # type: ignore
    updated: datetime.datetime = None  # type: ignore

    @validator("created", "updated", pre=True)
    def default_datetime(cls, value: datetime.datetime, ) -> datetime.datetime:
        return value or datetime.datetime.now()


class IDModel(BaseModel):
    id: int = Field(0, alias="id")