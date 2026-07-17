from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.plugin_data_type_manifest_kind import PluginDataTypeManifestKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="PluginDataTypeManifest")


@_attrs_define
class PluginDataTypeManifest:
    """
    Attributes:
        type_id (str):
        title (str):
        kind (PluginDataTypeManifestKind | Unset):  Default: PluginDataTypeManifestKind.ARTIFACT.
        description (str | Unset):  Default: ''.
    """

    type_id: str
    title: str
    kind: PluginDataTypeManifestKind | Unset = PluginDataTypeManifestKind.ARTIFACT
    description: str | Unset = ""

    def to_dict(self) -> dict[str, Any]:
        type_id = self.type_id

        title = self.title

        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type_id": type_id,
                "title": title,
            }
        )
        if kind is not UNSET:
            field_dict["kind"] = kind
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_id = d.pop("type_id")

        title = d.pop("title")

        _kind = d.pop("kind", UNSET)
        kind: PluginDataTypeManifestKind | Unset
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = PluginDataTypeManifestKind(_kind)

        description = d.pop("description", UNSET)

        plugin_data_type_manifest = cls(
            type_id=type_id,
            title=title,
            kind=kind,
            description=description,
        )

        return plugin_data_type_manifest
