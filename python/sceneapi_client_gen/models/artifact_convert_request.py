from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_convert_request_options import ArtifactConvertRequestOptions


T = TypeVar("T", bound="ArtifactConvertRequest")


@_attrs_define
class ArtifactConvertRequest:
    """Submit a conversion job for one artifact.

    Attributes:
        provider (None | str | Unset): Optional provider id to use when planning backend-native conversions.
        to_format (None | str | Unset): Exact target format id. Mutually compatible with accepted_formats.
        accepted_formats (list[str] | Unset): Acceptable target format ids in preference order. Required to be non-empty
            when to_format is omitted.
        require_lossless (bool | Unset):  Default: False.
        name (None | str | Unset):
        to_kind (None | str | Unset):
        options (ArtifactConvertRequestOptions | Unset):
    """

    provider: None | str | Unset = UNSET
    to_format: None | str | Unset = UNSET
    accepted_formats: list[str] | Unset = UNSET
    require_lossless: bool | Unset = False
    name: None | str | Unset = UNSET
    to_kind: None | str | Unset = UNSET
    options: ArtifactConvertRequestOptions | Unset = UNSET

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

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        to_kind: None | str | Unset
        if isinstance(self.to_kind, Unset):
            to_kind = UNSET
        else:
            to_kind = self.to_kind

        options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

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
        if name is not UNSET:
            field_dict["name"] = name
        if to_kind is not UNSET:
            field_dict["to_kind"] = to_kind
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_convert_request_options import (
            ArtifactConvertRequestOptions,
        )

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

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_to_kind(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        to_kind = _parse_to_kind(d.pop("to_kind", UNSET))

        _options = d.pop("options", UNSET)
        options: ArtifactConvertRequestOptions | Unset
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = ArtifactConvertRequestOptions.from_dict(_options)

        artifact_convert_request = cls(
            provider=provider,
            to_format=to_format,
            accepted_formats=accepted_formats,
            require_lossless=require_lossless,
            name=name,
            to_kind=to_kind,
            options=options,
        )

        return artifact_convert_request
