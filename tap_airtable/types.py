from typing import Any

from singer_sdk import typing as th

AirtableThumbnail = th.ObjectType(
    th.Property("url", th.StringType), th.Property("height", th.NumberType), th.Property("width", th.NumberType)
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

AIRTABLE_TO_SINGER_MAPPING: dict[str, Any] = {
    "singleLineText": th.StringType,
    "email": th.StringType,
    "url": th.StringType,
    "multilineText": th.StringType,
    "number": th.NumberType,
    "percent": th.StringType,
    "currency": th.StringType,
    "singleSelect": th.StringType,
    "multipleSelects": th.ArrayType(th.StringType),
    "singleCollaborator": th.StringType,
    "multipleCollaborators": th.ArrayType(AirtableCollaborator),
    "multipleRecordLinks": th.ArrayType(th.StringType),
    "date": th.DateType,
    "dateTime": th.DateTimeType,
    "phoneNumber": th.StringType,
    "multipleAttachments": th.ArrayType(AirtableAttachment),
    "checkbox": th.BooleanType,
    "formula": th.StringType,
    "createdTime": th.DateTimeType,
    "rollup": th.StringType,
    "count": th.StringType,
    "lookup": th.StringType,
    "multipleLookupValues": th.ArrayType(th.StringType),
    "autoNumber": th.StringType,
    "barcode": th.StringType,
    "rating": th.StringType,
    "richText": th.StringType,
    "duration": th.StringType,
    "lastModifiedTime": th.DateTimeType,
    "button": th.StringType,
    "createdBy": th.StringType,
    "lastModifiedBy": th.StringType,
    "externalSyncSource": th.StringType,
    "aiText": th.StringType,
}
