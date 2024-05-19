from dataclasses import dataclass
from typing import Any, cast

from singer_sdk import typing as th
from slugify import slugify

from tap_airtable.types import AIRTABLE_TO_SINGER_MAPPING


@dataclass
class AirtableField:
    field_type: str
    id: str
    name: str

    @property
    def singer_type(self) -> type[th.JSONTypeHelper[Any]]:
        return cast(type[th.JSONTypeHelper[Any]], AIRTABLE_TO_SINGER_MAPPING[self.field_type])

    def to_singer_property(self) -> th.Property[Any]:
        return th.Property(slugify(self.name, separator="_"), self.singer_type, required=False)


@dataclass
class AirtableTable:
    id: str
    name: str
    fields: list[AirtableField]

    def to_singer_schema(self) -> th.PropertiesList:
        return th.PropertiesList(
            th.Property("id", th.StringType, required=True),
            th.Property("createdtime", th.DateTimeType, required=True),
            *(field.to_singer_property() for field in self.fields),
        )


@dataclass
class AirtableBase:
    id: str
    name: str
    tables: list[AirtableTable]
