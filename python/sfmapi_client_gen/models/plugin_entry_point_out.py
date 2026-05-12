from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_manifest import PluginManifest


T = TypeVar("T", bound="PluginEntryPointOut")


@_attrs_define
class PluginEntryPointOut:
    """
    Attributes:
        plugin_id (str):
        entry_point (str):
        distribution (None | str | Unset):
        version (None | str | Unset):
        manifest (None | PluginManifest | Unset):
        load_error (None | str | Unset):
    """

    plugin_id: str
    entry_point: str
    distribution: None | str | Unset = UNSET
    version: None | str | Unset = UNSET
    manifest: None | PluginManifest | Unset = UNSET
    load_error: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.plugin_manifest import PluginManifest

        plugin_id = self.plugin_id

        entry_point = self.entry_point

        distribution: None | str | Unset
        if isinstance(self.distribution, Unset):
            distribution = UNSET
        else:
            distribution = self.distribution

        version: None | str | Unset
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        manifest: dict[str, Any] | None | Unset
        if isinstance(self.manifest, Unset):
            manifest = UNSET
        elif isinstance(self.manifest, PluginManifest):
            manifest = self.manifest.to_dict()
        else:
            manifest = self.manifest

        load_error: None | str | Unset
        if isinstance(self.load_error, Unset):
            load_error = UNSET
        else:
            load_error = self.load_error

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "plugin_id": plugin_id,
                "entry_point": entry_point,
            }
        )
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if version is not UNSET:
            field_dict["version"] = version
        if manifest is not UNSET:
            field_dict["manifest"] = manifest
        if load_error is not UNSET:
            field_dict["load_error"] = load_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_manifest import PluginManifest

        d = dict(src_dict)
        plugin_id = d.pop("plugin_id")

        entry_point = d.pop("entry_point")

        def _parse_distribution(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        distribution = _parse_distribution(d.pop("distribution", UNSET))

        def _parse_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        version = _parse_version(d.pop("version", UNSET))

        def _parse_manifest(data: object) -> None | PluginManifest | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                manifest_type_0 = PluginManifest.from_dict(data)

                return manifest_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PluginManifest | Unset, data)

        manifest = _parse_manifest(d.pop("manifest", UNSET))

        def _parse_load_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        load_error = _parse_load_error(d.pop("load_error", UNSET))

        plugin_entry_point_out = cls(
            plugin_id=plugin_id,
            entry_point=entry_point,
            distribution=distribution,
            version=version,
            manifest=manifest,
            load_error=load_error,
        )

        return plugin_entry_point_out
