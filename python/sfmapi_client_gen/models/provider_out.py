from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.provider_out_links_type_0 import ProviderOutLinksType0


T = TypeVar("T", bound="ProviderOut")


@_attrs_define
class ProviderOut:
    """
    Attributes:
        provider_id (str):
        plugin_id (str):
        display_name (str):
        description (None | str | Unset):
        capabilities (list[str] | Unset):
        backend_actions (list[str] | Unset):
        runtime_modes (list[str] | Unset):
        installed (bool | Unset):  Default: True.
        enabled (bool | Unset):  Default: True.
        field_links (None | ProviderOutLinksType0 | Unset):
    """

    provider_id: str
    plugin_id: str
    display_name: str
    description: None | str | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    backend_actions: list[str] | Unset = UNSET
    runtime_modes: list[str] | Unset = UNSET
    installed: bool | Unset = True
    enabled: bool | Unset = True
    field_links: None | ProviderOutLinksType0 | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.provider_out_links_type_0 import ProviderOutLinksType0

        provider_id = self.provider_id

        plugin_id = self.plugin_id

        display_name = self.display_name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        backend_actions: list[str] | Unset = UNSET
        if not isinstance(self.backend_actions, Unset):
            backend_actions = self.backend_actions

        runtime_modes: list[str] | Unset = UNSET
        if not isinstance(self.runtime_modes, Unset):
            runtime_modes = self.runtime_modes

        installed = self.installed

        enabled = self.enabled

        field_links: dict[str, Any] | None | Unset
        if isinstance(self.field_links, Unset):
            field_links = UNSET
        elif isinstance(self.field_links, ProviderOutLinksType0):
            field_links = self.field_links.to_dict()
        else:
            field_links = self.field_links

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider_id": provider_id,
                "plugin_id": plugin_id,
                "display_name": display_name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if backend_actions is not UNSET:
            field_dict["backend_actions"] = backend_actions
        if runtime_modes is not UNSET:
            field_dict["runtime_modes"] = runtime_modes
        if installed is not UNSET:
            field_dict["installed"] = installed
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if field_links is not UNSET:
            field_dict["_links"] = field_links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_out_links_type_0 import ProviderOutLinksType0

        d = dict(src_dict)
        provider_id = d.pop("provider_id")

        plugin_id = d.pop("plugin_id")

        display_name = d.pop("display_name")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        backend_actions = cast(list[str], d.pop("backend_actions", UNSET))

        runtime_modes = cast(list[str], d.pop("runtime_modes", UNSET))

        installed = d.pop("installed", UNSET)

        enabled = d.pop("enabled", UNSET)

        def _parse_field_links(data: object) -> None | ProviderOutLinksType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                field_links_type_0 = ProviderOutLinksType0.from_dict(data)

                return field_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProviderOutLinksType0 | Unset, data)

        field_links = _parse_field_links(d.pop("_links", UNSET))

        provider_out = cls(
            provider_id=provider_id,
            plugin_id=plugin_id,
            display_name=display_name,
            description=description,
            capabilities=capabilities,
            backend_actions=backend_actions,
            runtime_modes=runtime_modes,
            installed=installed,
            enabled=enabled,
            field_links=field_links,
        )

        return provider_out
