from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Rotation")


@_attrs_define
class Rotation:
    """Hamilton quaternion stored ``(w, x, y, z)``.

    Attributes:
        w (float):
        x (float):
        y (float):
        z (float):
    """

    w: float
    x: float
    y: float
    z: float

    def to_dict(self) -> dict[str, Any]:
        w = self.w

        x = self.x

        y = self.y

        z = self.z

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "w": w,
                "x": x,
                "y": y,
                "z": z,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        w = d.pop("w")

        x = d.pop("x")

        y = d.pop("y")

        z = d.pop("z")

        rotation = cls(
            w=w,
            x=x,
            y=y,
            z=z,
        )

        return rotation
