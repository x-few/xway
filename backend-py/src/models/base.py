import datetime
from pydantic import BaseConfig, BaseModel, Field, validator
import orjson


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
        # alias_generator = convert_field_to_camel_case
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class DateTimeModel(BaseModel):
    created: datetime.datetime = None  # type: ignore
    updated: datetime.datetime = None  # type: ignore

    @validator("created", "updated", pre=True)
    def default_datetime(cls, value: datetime.datetime, ) -> datetime.datetime:
        return value or datetime.datetime.now()


class IDModel(BaseModel):
    id: int = Field(0, alias="id")
