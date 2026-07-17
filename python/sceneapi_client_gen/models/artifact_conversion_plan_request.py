from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArtifactConversionPlanRequest")


@_attrs_define
class ArtifactConversionPlanRequest:
    """Ask sfmapi to choose or validate an artifact format conversion.

    Attributes:
        provider (None | str | Unset): Optional provider id to use when planning backend-native conversions.
        to_format (None | str | Unset): Exact target format id. Mutually compatible with accepted_formats.
        accepted_formats (list[str] | Unset): Acceptable target format ids in preference order. Required to be non-empty
            when to_format is omitted.
        require_lossless (bool | Unset):  Default: False.
    """

    provider: None | str | Unset = UNSET
    to_format: None | str | Unset = UNSET
    accepted_formats: list[str] | Unset = UNSET
    require_lossless: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        to_format: None | str | Unset
        if isinstance(self.to_format, Unset):
            to_format = UNSET
        else:
            to_format = self.to_format

        accepted_formats: list[str] | Unset = UNSET
        if not isinstance(self.accepted_formats, Unset):
            accepted_formats = self.accepted_formats

        if accepted_formats is not UNSET and len(accepted_formats) == 0:
            raise ValueError(
                "Artifact conversion requests require to_format or "
                "non-empty accepted_formats"
            )
        if (to_format is UNSET or to_format is None) and accepted_formats is UNSET:
            raise ValueError(
                "Artifact conversion requests require to_format or "
                "non-empty accepted_formats"
            )

        require_lossless = self.require_lossless

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if provider is not UNSET:
            field_dict["provider"] = provider
        if to_format is not UNSET:
            field_dict["to_format"] = to_format
        if accepted_formats is not UNSET:
            field_dict["accepted_formats"] = accepted_formats
        if require_lossless is not UNSET:
            field_dict["require_lossless"] = require_lossless

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        def _parse_to_format(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        to_format = _parse_to_format(d.pop("to_format", UNSET))

        accepted_formats = cast(list[str], d.pop("accepted_formats", UNSET))

        require_lossless = d.pop("require_lossless", UNSET)

        artifact_conversion_plan_request = cls(
            provider=provider,
            to_format=to_format,
            accepted_formats=accepted_formats,
            require_lossless=require_lossless,
        )

        return artifact_conversion_plan_request
