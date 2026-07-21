from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_registry_item_out_links_type_0 import (
        PluginRegistryItemOutLinksType0,
    )


T = TypeVar("T", bound="PluginRegistryItemOut")


@_attrs_define
class PluginRegistryItemOut:
    """
    Attributes:
        plugin_id (str):
        display_name (str):
        description (str):
        package_name (str):
        github_url (str):
        trust_tier (str):
        runtime_modes (list[str]):
        providers (list[str]):
        installed (bool | Unset):  Default: False.
        enabled (bool | Unset):  Default: False.
        field_links (None | PluginRegistryItemOutLinksType0 | Unset):
    """

    plugin_id: str
    display_name: str
    description: str
    package_name: str
    github_url: str
    trust_tier: str
    runtime_modes: list[str]
    providers: list[str]
    installed: bool | Unset = False
    enabled: bool | Unset = False
    field_links: None | PluginRegistryItemOutLinksType0 | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.plugin_registry_item_out_links_type_0 import (
            PluginRegistryItemOutLinksType0,
        )

        plugin_id = self.plugin_id

        display_name = self.display_name

        description = self.description

        package_name = self.package_name

        github_url = self.github_url

        trust_tier = self.trust_tier

        runtime_modes = self.runtime_modes

        providers = self.providers

        installed = self.installed

        enabled = self.enabled

        field_links: dict[str, Any] | None | Unset
        if isinstance(self.field_links, Unset):
            field_links = UNSET
        elif isinstance(self.field_links, PluginRegistryItemOutLinksType0):
            field_links = self.field_links.to_dict()
        else:
            field_links = self.field_links

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "plugin_id": plugin_id,
                "display_name": display_name,
                "description": description,
                "package_name": package_name,
                "github_url": github_url,
                "trust_tier": trust_tier,
                "runtime_modes": runtime_modes,
                "providers": providers,
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
        from ..models.plugin_registry_item_out_links_type_0 import (
            PluginRegistryItemOutLinksType0,
        )

        d = dict(src_dict)
        plugin_id = d.pop("plugin_id")

        display_name = d.pop("display_name")

        description = d.pop("description")

        package_name = d.pop("package_name")

        github_url = d.pop("github_url")

        trust_tier = d.pop("trust_tier")

        runtime_modes = cast(list[str], d.pop("runtime_modes"))

        providers = cast(list[str], d.pop("providers"))

        installed = d.pop("installed", UNSET)

        enabled = d.pop("enabled", UNSET)

        def _parse_field_links(
            data: object,
        ) -> None | PluginRegistryItemOutLinksType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                field_links_type_0 = PluginRegistryItemOutLinksType0.from_dict(data)

                return field_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PluginRegistryItemOutLinksType0 | Unset, data)

        field_links = _parse_field_links(d.pop("_links", UNSET))

        plugin_registry_item_out = cls(
            plugin_id=plugin_id,
            display_name=display_name,
            description=description,
            package_name=package_name,
            github_url=github_url,
            trust_tier=trust_tier,
            runtime_modes=runtime_modes,
            providers=providers,
            installed=installed,
            enabled=enabled,
            field_links=field_links,
        )

        return plugin_registry_item_out
