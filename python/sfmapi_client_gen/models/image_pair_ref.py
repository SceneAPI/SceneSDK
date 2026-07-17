from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ImagePairRef")


@_attrs_define
class ImagePairRef:
    """One explicit pair of dataset image names.

    Attributes:
        image_name1 (str):
        image_name2 (str):
    """

    image_name1: str
    image_name2: str

    def to_dict(self) -> dict[str, Any]:
        image_name1 = self.image_name1

        image_name2 = self.image_name2

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "image_name1": image_name1,
                "image_name2": image_name2,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image_name1 = d.pop("image_name1")

        image_name2 = d.pop("image_name2")

        image_pair_ref = cls(
            image_name1=image_name1,
            image_name2=image_name2,
        )

        return image_pair_ref
