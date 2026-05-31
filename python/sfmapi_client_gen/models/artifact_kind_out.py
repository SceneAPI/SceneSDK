from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ArtifactKindOut")


@_attrs_define
class ArtifactKindOut:
    """Documented core artifact kind.

    Attributes:
        kind (str):
        datatype (str):
        title (str):
        description (str):
        durable (bool):
        artifact_format (str): Default canonical format id for this kind.
        schema_version (int):
    """

    kind: str
    datatype: str
    title: str
    description: str
    durable: bool
    artifact_format: str
    schema_version: int

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        datatype = self.datatype

        title = self.title

        description = self.description

        durable = self.durable

        artifact_format = self.artifact_format

        schema_version = self.schema_version

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "datatype": datatype,
                "title": title,
                "description": description,
                "durable": durable,
                "artifact_format": artifact_format,
                "schema_version": schema_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = d.pop("kind")

        datatype = d.pop("datatype")

        title = d.pop("title")

        description = d.pop("description")

        durable = d.pop("durable")

        artifact_format = d.pop("artifact_format")

        schema_version = d.pop("schema_version")

        artifact_kind_out = cls(
            kind=kind,
            datatype=datatype,
            title=title,
            description=description,
            durable=durable,
            artifact_format=artifact_format,
            schema_version=schema_version,
        )

        return artifact_kind_out
