from typing import Any

from singer_sdk import typing as th

# Define custom types for Airtable-specific fields
AirtableThumbnail = th.ObjectType(
    th.Property("url", th.StringType), 
    th.Property("height", th.NumberType), 
    th.Property("width", th.NumberType)
)

AirtableThumbnailSet = th.ObjectType(
    th.Property("full", AirtableThumbnail),
    th.Property("large", AirtableThumbnail),
    th.Property("small", AirtableThumbnail),
)

AirtableAttachment = th.ObjectType(
    th.Property("id", th.StringType),
    th.Property("type", th.StringType),
    th.Property("filename", th.StringType),
    th.Property("height", th.NumberType),
    th.Property("size", th.NumberType),
    th.Property("url", th.StringType),
    th.Property("width", th.NumberType),
    th.Property("thumbnails", AirtableThumbnailSet),
)

AirtableCollaborator = th.ObjectType(
    th.Property("id", th.StringType),
    th.Property("email", th.StringType),
    th.Property("name", th.StringType),
    th.Property("permissionLevel", th.StringType),
    th.Property("profilePicUrl", th.StringType),
)

# Mapping of Airtable field types to Singer field types
AIRTABLE_TO_SINGER_MAPPING: dict[str, Any] = {
    "singleLineText": th.StringType,
    "email": th.StringType,
    "url": th.StringType,
    "multilineText": th.StringType,
    "number": th.NumberType,
    "percent": th.NumberType,  # Percent values can be treated as numbers
    "currency": th.NumberType,  # Currency values can be treated as numbers
    "singleSelect": th.StringType,
    "multipleSelects": th.ArrayType(th.StringType),
    "singleCollaborator": th.StringType,  # Simplified to StringType for the ID or name
    "multipleCollaborators": th.ArrayType(AirtableCollaborator),
    "multipleRecordLinks": th.ArrayType(th.StringType),
    "date": th.DateType,
    "dateTime": th.DateTimeType,
    "phoneNumber": th.StringType,
    "multipleAttachments": th.ArrayType(AirtableAttachment),
    "checkbox": th.BooleanType,
    "formula": th.StringType,  # Formulas can be of various types; simplified to StringType
    "createdTime": th.DateTimeType,
    "rollup": th.StringType,  # Rollups can be various types; simplified to StringType
    "count": th.IntegerType,  # Counts are numeric
    "lookup": th.StringType,  # Lookups can be various types; simplified to StringType
    "multipleLookupValues": th.ArrayType(th.StringType),
    "autoNumber": th.IntegerType,  # AutoNumbers are numeric
    "barcode": th.StringType,
    "rating": th.IntegerType,  # Ratings are typically numeric
    "richText": th.StringType,
    "duration": th.NumberType,  # Duration can be treated as a number (seconds)
    "lastModifiedTime": th.DateTimeType,
    "button": th.StringType,
    "createdBy": th.StringType,  # CreatedBy can be a user ID or name
    "lastModifiedBy": th.StringType,  # LastModifiedBy can be a user ID or name
    "externalSyncSource": th.StringType,
    "aiText": th.StringType,
}