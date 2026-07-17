from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_detail_out_links_type_0 import PluginDetailOutLinksType0
    from ..models.plugin_manifest import PluginManifest


T = TypeVar("T", bound="PluginDetailOut")


@_attrs_define
class PluginDetailOut:
    """
    Attributes:
        manifest (PluginManifest):
        installed (bool | Unset):  Default: False.
        enabled (bool | Unset):  Default: False.
        field_links (None | PluginDetailOutLinksType0 | Unset):
    """

    manifest: PluginManifest
    installed: bool | Unset = False
    enabled: bool | Unset = False
    field_links: None | PluginDetailOutLinksType0 | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.plugin_detail_out_links_type_0 import PluginDetailOutLinksType0

        manifest = self.manifest.to_dict()

        installed = self.installed

        enabled = self.enabled

        field_links: dict[str, Any] | None | Unset
        if isinstance(self.field_links, Unset):
            field_links = UNSET
        elif isinstance(self.field_links, PluginDetailOutLinksType0):
            field_links = self.field_links.to_dict()
        else:
            field_links = self.field_links

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "manifest": manifest,
            }
        )
        if installed is not UNSET:
            field_dict["installed"] = installed
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if field_links is not UNSET:
            field_dict["_links"] = field_links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_detail_out_links_type_0 import PluginDetailOutLinksType0
        from ..models.plugin_manifest import PluginManifest

        d = dict(src_dict)
        manifest = PluginManifest.from_dict(d.pop("manifest"))

        installed = d.pop("installed", UNSET)

        enabled = d.pop("enabled", UNSET)

        def _parse_field_links(
            data: object,
        ) -> None | PluginDetailOutLinksType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                field_links_type_0 = PluginDetailOutLinksType0.from_dict(data)

                return field_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PluginDetailOutLinksType0 | Unset, data)

        field_links = _parse_field_links(d.pop("_links", UNSET))

        plugin_detail_out = cls(
            manifest=manifest,
            installed=installed,
            enabled=enabled,
            field_links=field_links,
        )

        return plugin_detail_out
