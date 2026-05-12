from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProviderManifest")


@_attrs_define
class ProviderManifest:
    """
    Attributes:
        provider_id (str):
        display_name (str):
        description (None | str | Unset):
        capabilities (list[str] | Unset):
        backend_actions (list[str] | Unset):
        priority_hint (int | Unset):  Default: 100.
    """

    provider_id: str
    display_name: str
    description: None | str | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    backend_actions: list[str] | Unset = UNSET
    priority_hint: int | Unset = 100

    def to_dict(self) -> dict[str, Any]:
        provider_id = self.provider_id

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

        priority_hint = self.priority_hint

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider_id": provider_id,
                "display_name": display_name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if backend_actions is not UNSET:
            field_dict["backend_actions"] = backend_actions
        if priority_hint is not UNSET:
            field_dict["priority_hint"] = priority_hint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider_id = d.pop("provider_id")

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

        priority_hint = d.pop("priority_hint", UNSET)

        provider_manifest = cls(
            provider_id=provider_id,
            display_name=display_name,
            description=description,
            capabilities=capabilities,
            backend_actions=backend_actions,
            priority_hint=priority_hint,
        )

        return provider_manifest
