"""Airtable tap class."""

import logging

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_airtable.client import AirtableClient
from tap_airtable.streams import BaseAirtableStream, airtable_stream_factory

logger = logging.getLogger(__name__)


class TapAirtable(Tap):
    """Airtable tap class."""

    name = "tap-airtable"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            description="The token to authenticate against Airtable API",
        ),
        th.Property(
            "base_ids",
            th.ArrayType(th.StringType),
            required=False,
            description="Selected base ids (all if not specified)",
        ),
        th.Property(
            "table_mapping",
            th.ObjectType(additional_properties=th.StringType),
            description="Mapping of table_id => custom_table_name",
            required=False,
        ),
    ).to_dict()

    def discover_streams(self) -> list[BaseAirtableStream]:
        """Return a list of discovered streams."""
        client = AirtableClient(self.config["token"])
        streams: list[BaseAirtableStream] = []
        mapping: dict[str, str] = self.config.get("table_mapping", {})
        for base in client.get_bases(self.config.get("base_ids", [])):
            for table in base.tables:
                if table.id in mapping:
                    logger.debug(f"Renaming table {table.name} => {mapping[table.id]}")
                    table.name = mapping[table.id]
                streams.append(airtable_stream_factory(base.id, table)(tap=self))
        return streams
