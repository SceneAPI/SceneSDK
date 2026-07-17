from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PluginDependencyManifest")


@_attrs_define
class PluginDependencyManifest:
    """
    Attributes:
        plugin_id (str): Canonical plugin id reserved for future dependency-aware typed-dataflow resolution. Current
            validation remains limited to core and same-plugin references.
        version (None | str | Unset): Optional plugin package/source version constraint reserved for future dependency-
            aware typed-dataflow resolution.
    """

    plugin_id: str
    version: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        plugin_id = self.plugin_id

        version: None | str | Unset
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "plugin_id": plugin_id,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plugin_id = d.pop("plugin_id")

        def _parse_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        version = _parse_version(d.pop("version", UNSET))

        plugin_dependency_manifest = cls(
            plugin_id=plugin_id,
            version=version,
        )

        return plugin_dependency_manifest
