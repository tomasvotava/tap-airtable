"""REST client handling, including AirtableStream base class."""

import logging
from collections.abc import Iterable
from typing import Any, Optional, cast
from urllib.parse import urljoin

import backoff
import requests

from tap_airtable.entities import AirtableBase, AirtableField, AirtableTable

logger = logging.getLogger(__name__)


class NonRetryableError(ValueError): ...


class AirtableClient:
    base_url = "https://api.airtable.com/v0/"

    def __init__(self, token: str) -> None:
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"authorization": f"Bearer {self.token}"})

    @backoff.on_exception(backoff.expo, (requests.HTTPError,), max_tries=7, max_time=120)
    def _get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> requests.Response:
        response = self.session.get(urljoin(self.base_url, endpoint), params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            if response.status_code == 429 or response.status_code >= 500:
                raise
            raise NonRetryableError(f"Server response: {response.status_code}, {response.text}") from error
        return response

    def _get_base_schema(self, base_id: str) -> list[dict[str, Any]]:
        response = self._get(f"meta/bases/{base_id}/tables")
        response.raise_for_status()
        return cast(list[dict[str, Any]], response.json()["tables"])

    def get_bases(self, base_ids: Optional[list[str]] = None) -> list[AirtableBase]:
        response = self._get("meta/bases")
        data = response.json()
        server_base_ids = {base["id"] for base in data["bases"]}
        missing_base_ids = set(base_ids or []) - server_base_ids
        if missing_base_ids:
            raise ValueError(f"Base ids missing {missing_base_ids}")
        bases: list[AirtableBase] = []
        for base in data["bases"]:
            tables: list[AirtableTable] = []
            if base_ids and base["id"] not in base_ids:
                logger.debug(f"Skipping base {base['id']}")
                continue
            base_schema = self._get_base_schema(base["id"])
            for table in base_schema:
                tables.append(
                    AirtableTable(
                        table["id"],
                        table["name"],
                        [AirtableField(field["type"], field["id"], field["name"]) for field in table["fields"]],
                    )
                )
            bases.append(AirtableBase(base["id"], base["name"], tables))

        return bases

    def get_records(self, base_id: str, table_id: str, page_size: int = 100) -> Iterable[dict[str, Any]]:
        offset: dict[str, str] = {}
        while True:
            response = self._get(f"{base_id}/{table_id}", params={"pageSize": page_size, **offset})
            data = response.json()
            yield from data["records"]
            if "offset" in data:
                offset["offset"] = data["offset"]
                continue
            break
