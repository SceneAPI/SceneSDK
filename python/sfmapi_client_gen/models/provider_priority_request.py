from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProviderPriorityRequest")


@_attrs_define
class ProviderPriorityRequest:
    """
    Attributes:
        providers (list[str] | Unset):
    """

    providers: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        providers: list[str] | Unset = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if providers is not UNSET:
            field_dict["providers"] = providers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        providers = cast(list[str], d.pop("providers", UNSET))

        provider_priority_request = cls(
            providers=providers,
        )

        return provider_priority_request
