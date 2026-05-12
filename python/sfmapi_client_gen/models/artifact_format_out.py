from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_format_out_examples_item import ArtifactFormatOutExamplesItem
    from ..models.artifact_format_out_json_schema_type_0 import (
        ArtifactFormatOutJsonSchemaType0,
    )


T = TypeVar("T", bound="ArtifactFormatOut")


@_attrs_define
class ArtifactFormatOut:
    """Documented core artifact interchange format.

    Attributes:
        format_id (str):
        artifact_type (str):
        title (str):
        description (str):
        schema_version (int):
        media_types (list[str]):
        json_schema (ArtifactFormatOutJsonSchemaType0 | None | Unset):
        examples (list[ArtifactFormatOutExamplesItem] | Unset):
        portable (bool | Unset):  Default: True.
    """

    format_id: str
    artifact_type: str
    title: str
    description: str
    schema_version: int
    media_types: list[str]
    json_schema: ArtifactFormatOutJsonSchemaType0 | None | Unset = UNSET
    examples: list[ArtifactFormatOutExamplesItem] | Unset = UNSET
    portable: bool | Unset = True

    def to_dict(self) -> dict[str, Any]:
        from ..models.artifact_format_out_json_schema_type_0 import (
            ArtifactFormatOutJsonSchemaType0,
        )

        format_id = self.format_id

        artifact_type = self.artifact_type

        title = self.title

        description = self.description

        schema_version = self.schema_version

        media_types = self.media_types

        json_schema: dict[str, Any] | None | Unset
        if isinstance(self.json_schema, Unset):
            json_schema = UNSET
        elif isinstance(self.json_schema, ArtifactFormatOutJsonSchemaType0):
            json_schema = self.json_schema.to_dict()
        else:
            json_schema = self.json_schema

        examples: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.examples, Unset):
            examples = []
            for examples_item_data in self.examples:
                examples_item = examples_item_data.to_dict()
                examples.append(examples_item)

        portable = self.portable

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "format_id": format_id,
                "artifact_type": artifact_type,
                "title": title,
                "description": description,
                "schema_version": schema_version,
                "media_types": media_types,
            }
        )
        if json_schema is not UNSET:
            field_dict["json_schema"] = json_schema
        if examples is not UNSET:
            field_dict["examples"] = examples
        if portable is not UNSET:
            field_dict["portable"] = portable

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_format_out_examples_item import (
            ArtifactFormatOutExamplesItem,
        )
        from ..models.artifact_format_out_json_schema_type_0 import (
            ArtifactFormatOutJsonSchemaType0,
        )

        d = dict(src_dict)
        format_id = d.pop("format_id")

        artifact_type = d.pop("artifact_type")

        title = d.pop("title")

        description = d.pop("description")

        schema_version = d.pop("schema_version")

        media_types = cast(list[str], d.pop("media_types"))

        def _parse_json_schema(
            data: object,
        ) -> ArtifactFormatOutJsonSchemaType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                json_schema_type_0 = ArtifactFormatOutJsonSchemaType0.from_dict(data)

                return json_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ArtifactFormatOutJsonSchemaType0 | None | Unset, data)

        json_schema = _parse_json_schema(d.pop("json_schema", UNSET))

        _examples = d.pop("examples", UNSET)
        examples: list[ArtifactFormatOutExamplesItem] | Unset = UNSET
        if _examples is not UNSET:
            examples = []
            for examples_item_data in _examples:
                examples_item = ArtifactFormatOutExamplesItem.from_dict(
                    examples_item_data
                )

                examples.append(examples_item)

        portable = d.pop("portable", UNSET)

        artifact_format_out = cls(
            format_id=format_id,
            artifact_type=artifact_type,
            title=title,
            description=description,
            schema_version=schema_version,
            media_types=media_types,
            json_schema=json_schema,
            examples=examples,
            portable=portable,
        )

        return artifact_format_out
