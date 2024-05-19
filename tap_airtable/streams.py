"""Stream type classes for tap-airtable."""

from collections.abc import Iterable
from typing import Any, ClassVar, Optional, Union

from singer_sdk.streams import Stream
from slugify import slugify

from tap_airtable.client import AirtableClient
from tap_airtable.entities import AirtableTable


class BaseAirtableStream(Stream):
    primary_keys: ClassVar = ["id"]
    original_airtable_table: AirtableTable
    base_id: str
    replication_key = None

    def get_records(
        self, context: Optional[dict[str, Any]]
    ) -> Iterable[Union[dict[str, Any], tuple[dict[str, Any], dict[str, Any]]]]:
        client = AirtableClient(self.config["token"])
        for record in client.get_records(self.base_id, self.original_airtable_table.id):
            fields = record.pop("fields", {})
            yield {slugify(key, separator="_"): value for key, value in {**record, **fields}.items()}


def airtable_stream_factory(table_base_id: str, table: AirtableTable) -> type[BaseAirtableStream]:
    class AirtableStream(BaseAirtableStream):
        original_airtable_table = table
        name = slugify(table.name, separator="_")
        base_id = table_base_id

        @property
        def schema(self) -> dict[str, Any]:
            return table.to_singer_schema().to_dict()

    AirtableStream.__name__ = f"{table.name.title()}AirtableStream"
    return AirtableStream
