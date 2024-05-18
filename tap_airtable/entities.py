from dataclasses import dataclass
from typing import Any

from singer_sdk import typing as th

from tap_airtable.types import AIRTABLE_TO_SINGER_MAPPING


@dataclass
class AirtableField:
    field_type: str
    id: str
    name: str

    @property
    def singer_type(self) -> type[th.JSONTypeHelper[Any]]:
        return AIRTABLE_TO_SINGER_MAPPING[self.field_type]

    def to_singer_property(self) -> th.Property[Any]:
        return th.Property(self.name, self.singer_type, required=False)


@dataclass
class AirtableTable:
    id: str
    name: str
    fields: list[AirtableField]

    def to_singer_schema(self) -> th.PropertiesList:
        return th.PropertiesList(
            th.Property("id", th.StringType, required=True),
            th.Property("createdTime", th.DateTimeType, required=True),
            *(field.to_singer_property() for field in self.fields),
        )


@dataclass
class AirtableBase:
    id: str
    name: str
    tables: list[AirtableTable]
