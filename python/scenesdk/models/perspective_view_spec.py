from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PerspectiveViewSpec")


@_attrs_define
class PerspectiveViewSpec:
    """One pinhole view sampled from an equirectangular panorama.

    Attributes:
        name (None | str | Unset):
        yaw_deg (float | Unset):  Default: 0.0.
        pitch_deg (float | Unset):  Default: 0.0.
        roll_deg (float | Unset):  Default: 0.0.
        hfov_deg (float | Unset):  Default: 90.0.
        width (int | Unset):  Default: 1024.
        height (int | Unset):  Default: 1024.
    """

    name: None | str | Unset = UNSET
    yaw_deg: float | Unset = 0.0
    pitch_deg: float | Unset = 0.0
    roll_deg: float | Unset = 0.0
    hfov_deg: float | Unset = 90.0
    width: int | Unset = 1024
    height: int | Unset = 1024

    def to_dict(self) -> dict[str, Any]:
        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        yaw_deg = self.yaw_deg

        pitch_deg = self.pitch_deg

        roll_deg = self.roll_deg

        hfov_deg = self.hfov_deg

        width = self.width

        height = self.height

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if yaw_deg is not UNSET:
            field_dict["yaw_deg"] = yaw_deg
        if pitch_deg is not UNSET:
            field_dict["pitch_deg"] = pitch_deg
        if roll_deg is not UNSET:
            field_dict["roll_deg"] = roll_deg
        if hfov_deg is not UNSET:
            field_dict["hfov_deg"] = hfov_deg
        if width is not UNSET:
            field_dict["width"] = width
        if height is not UNSET:
            field_dict["height"] = height

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        yaw_deg = d.pop("yaw_deg", UNSET)

        pitch_deg = d.pop("pitch_deg", UNSET)

        roll_deg = d.pop("roll_deg", UNSET)

        hfov_deg = d.pop("hfov_deg", UNSET)

        width = d.pop("width", UNSET)

        height = d.pop("height", UNSET)

        perspective_view_spec = cls(
            name=name,
            yaw_deg=yaw_deg,
            pitch_deg=pitch_deg,
            roll_deg=roll_deg,
            hfov_deg=hfov_deg,
            width=width,
            height=height,
        )

        return perspective_view_spec
