from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArtifactConversionOut")


@_attrs_define
class ArtifactConversionOut:
    """Advertised conversion between artifact formats.

    Attributes:
        from_format (str):
        to_format (str):
        lossless (bool | Unset):  Default: False.
        description (None | str | Unset):
    """

    from_format: str
    to_format: str
    lossless: bool | Unset = False
    description: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from_format = self.from_format

        to_format = self.to_format

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

        lossless = d.pop("lossless", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        artifact_conversion_out = cls(
            from_format=from_format,
            to_format=to_format,
            lossless=lossless,
            description=description,
        )

        return artifact_conversion_out
