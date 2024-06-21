import os

import dotenv
import pytest

from tap_airtable.client import AirtableClient
from tap_airtable.entities import AirtableBase, AirtableField, AirtableTable
from tap_airtable.tap import TapAirtable

test_base_foo = AirtableBase(
    "foo",
    "foo",
    tables=[
        AirtableTable(
            id="table_1",
            name="table_1",
            fields=[
                AirtableField("singleLineText", "field1", "field1"),
                AirtableField("email", "email", "email"),
            ],
        ),
        AirtableTable(
            id="table_2",
            name="table_2",
            fields=[
                AirtableField("dateTime", "created_at", "created_at"),
                AirtableField("number", "number", "number"),
                AirtableField("singleLineText", "name", "name"),
            ],
        ),
    ],
)

test_base_bar = AirtableBase(
    "bar",
    "bar",
    tables=[
        AirtableTable(
            id="bar_table",
            name="bar_table",
            fields=[
                AirtableField("singleLineText", "field1", "field1"),
                AirtableField("singleLineText", "field2", "field2"),
                AirtableField("singleLineText", "field3", "field3"),
                AirtableField("singleLineText", "field4", "field4"),
            ],
        )
    ],
)


@pytest.fixture()
def _patch_client(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("tap_airtable.client.AirtableClient.get_bases", lambda _, __: [test_base_foo, test_base_bar])


@pytest.fixture(name="integration_test_token", scope="session")
def integration_test_token_fixture() -> str:
    try:
        dotenv.load_dotenv()
        token = os.environ["AIRTABLE_INTEGRATION_TEST_TOKEN"]
    except KeyError:
        pytest.skip("Integration tests cannot run without AIRTABLE_INTEGRATION_TEST_TOKEN variable.")
    return token


@pytest.fixture()
def integration_test_tap(integration_test_token: str) -> TapAirtable:
    return TapAirtable(
        config={
            "token": integration_test_token,
            "base_ids": ["appwtyvkFPMTyR40b"],
            "table_mapping": {"tblWqSoZj2A4uxTSR": "renamed_food"},
        }
    )


@pytest.fixture()
def integration_test_client(integration_test_token: str) -> AirtableClient:
    return AirtableClient(integration_test_token)
