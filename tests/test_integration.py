from tap_airtable.client import AirtableClient
from tap_airtable.tap import TapAirtable


def test_discover_streams_integration(integration_test_tap: TapAirtable) -> None:
    streams = integration_test_tap.discover_streams()

    assert streams[0].name == "teams"
    assert streams[1].name == "renamed_food"
    assert streams[2].name == "faker_users"
    assert streams[3].name == "faker_cars"

    assert {stream.base_id for stream in streams} == {"appwtyvkFPMTyR40b"}


def test_client_get_records(integration_test_client: AirtableClient) -> None:
    records = list(integration_test_client.get_records("appwtyvkFPMTyR40b", "tbl3SsrPtyxu3SiX6"))
    assert len(records) == 3
    assert set(records[0]["fields"].keys()) == {"Name", "Priority", "Flagged"}
