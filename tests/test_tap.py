import pytest

from tap_airtable.tap import TapAirtable


@pytest.mark.usefixtures("_patch_client")
def test_discover_streams() -> None:
    tap = TapAirtable(config={"token": "token"})
    streams = tap.discover_streams()
    assert len(streams) == 3
    assert streams[0].name == "table_1"
    assert streams[0].base_id == "foo"
    assert streams[0].original_airtable_table.name == "table_1"

    assert streams[1].name == "table_2"
    assert streams[1].base_id == "foo"
    assert streams[1].original_airtable_table.name == "table_2"

    assert streams[2].name == "bar_table"
    assert streams[2].base_id == "bar"
    assert streams[2].original_airtable_table.name == "bar_table"


@pytest.mark.usefixtures("_patch_client")
def test_discover_streams_mapping() -> None:
    tap = TapAirtable(
        config={
            "token": "token",
            "table_mapping": {"table_1": "Table 1", "table_2": "Table 2", "bar_table": "products"},
        }
    )

    streams = tap.discover_streams()

    assert streams[0].original_airtable_table.name == "Table 1"
    assert streams[0].name == "table_1"  # is slugified

    assert streams[1].original_airtable_table.name == "Table 2"
    assert streams[1].name == "table_2"  # slugified

    assert streams[2].original_airtable_table.name == "products"
    assert streams[2].name == "products"
