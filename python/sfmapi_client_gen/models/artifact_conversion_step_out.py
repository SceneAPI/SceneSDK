from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArtifactConversionStepOut")


@_attrs_define
class ArtifactConversionStepOut:
    """One conversion step selected from backend contracts.

    Attributes:
        from_format (str):
        to_format (str):
        contract_id (None | str | Unset):
        backend (None | str | Unset):
        provider (None | str | Unset):
        lossless (bool | Unset):  Default: False.
        description (None | str | Unset):
    """

    from_format: str
    to_format: str
    contract_id: None | str | Unset = UNSET
    backend: None | str | Unset = UNSET
    provider: None | str | Unset = UNSET
    lossless: bool | Unset = False
    description: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from_format = self.from_format

        to_format = self.to_format

        contract_id: None | str | Unset
        if isinstance(self.contract_id, Unset):
            contract_id = UNSET
        else:
            contract_id = self.contract_id

        backend: None | str | Unset
        if isinstance(self.backend, Unset):
            backend = UNSET
        else:
            backend = self.backend

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        lossless = self.lossless

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "from_format": from_format,
                "to_format": to_format,
            }
        )
        if contract_id is not UNSET:
            field_dict["contract_id"] = contract_id
        if backend is not UNSET:
            field_dict["backend"] = backend
        if provider is not UNSET:
            field_dict["provider"] = provider
        if lossless is not UNSET:
            field_dict["lossless"] = lossless
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_format = d.pop("from_format")

        to_format = d.pop("to_format")

        def _parse_contract_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        contract_id = _parse_contract_id(d.pop("contract_id", UNSET))

        def _parse_backend(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        backend = _parse_backend(d.pop("backend", UNSET))

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        lossless = d.pop("lossless", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        artifact_conversion_step_out = cls(
            from_format=from_format,
            to_format=to_format,
            contract_id=contract_id,
            backend=backend,
            provider=provider,
            lossless=lossless,
            description=description,
        )

        return artifact_conversion_step_out
