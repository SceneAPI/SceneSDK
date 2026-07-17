from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OneShotImageInfo")


@_attrs_define
class OneShotImageInfo:
    """Header-derived image metadata echoed back for caller sanity checks.

    ``width`` and ``height`` are ``None`` when the server cannot read the
    dimensions cheaply from image headers. sfmapi does not decode pixels in
    the API layer.

        Attributes:
            width (int | None):
            height (int | None):
            byte_size (int):
    """

    width: int | None
    height: int | None
    byte_size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        width: int | None
        width = self.width

        height: int | None
        height = self.height

        byte_size = self.byte_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "width": width,
                "height": height,
                "byte_size": byte_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_width(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        width = _parse_width(d.pop("width"))

        def _parse_height(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        height = _parse_height(d.pop("height"))

        byte_size = d.pop("byte_size")

        one_shot_image_info = cls(
            width=width,
            height=height,
            byte_size=byte_size,
        )

        one_shot_image_info.additional_properties = d
        return one_shot_image_info

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
