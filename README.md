# tap-airtable

`tap-airtable` is a Singer tap for Airtable usable with Meltano.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

### Standalone

You can install `tap-airtable` using `pipx` to install it globally on your system:

```bash
pipx install tap-airtable
```

### With Meltano

If you're using this tap with Meltano, you can install it as an extractor.
The tap is not yet available in the Meltano Hub, so you will need to install it from the source.

```bash
meltano add extractor tap-airtable --from-ref https://raw.githubusercontent.com/tomasvotava/tap-airtable/master/tap-airtable.yml
```

## Configuration

### Accepted Config Options

| Property | Required | Description |
|:---|:----|:---|
| `token` | Yes | Airtable API token |
| `base_ids` | No | List of base IDs to extract data from (if not given, all bases are extracted) |
| `table_mapping` | No | Mapping of Airtable table ids to target table names (if not given table names from Airtable are used) |

If `table_mapping` is not provided, the tap will use the table names from Airtable as target table names.
This may not be ideal if the table names are not human-readable or if they contain special characters.

### Standalone Configuration

```json
{
    "token": "<your airtable token>",
    "base_ids": ["<base_id_1>", "<base_id_2>"],
    "table_mapping": {
        "<table_id_1>": "target_table_name_1",
        "<table_id_2>": "target_table_name_2"
    }
}
```

Run the tap with:

```bash
tap-airtable --config config.json
```

### Meltano Configuration

Run `meltano config tap-airtable set --interactive` to set the configuration interactively.
