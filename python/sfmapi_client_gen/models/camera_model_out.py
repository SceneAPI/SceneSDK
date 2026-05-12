from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.camera_model_out_distortion import CameraModelOutDistortion
from ..models.camera_model_out_projection import CameraModelOutProjection
from ..types import UNSET, Unset

T = TypeVar("T", bound="CameraModelOut")


@_attrs_define
class CameraModelOut:
    """Portable description of a camera model's parameter layout.

    Attributes:
        model (str):
        projection (CameraModelOutProjection):
        distortion (CameraModelOutDistortion):
        params (list[str] | Unset):
        aliases (list[str] | Unset):
        spherical (bool | Unset):  Default: False.
        notes (None | str | Unset):
    """

    model: str
    projection: CameraModelOutProjection
    distortion: CameraModelOutDistortion
    params: list[str] | Unset = UNSET
    aliases: list[str] | Unset = UNSET
    spherical: bool | Unset = False
    notes: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        model = self.model

        projection = self.projection.value

        distortion = self.distortion.value

        params: list[str] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params

        aliases: list[str] | Unset = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        spherical = self.spherical

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model": model,
                "projection": projection,
                "distortion": distortion,
            }
        )
        if params is not UNSET:
            field_dict["params"] = params
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if spherical is not UNSET:
            field_dict["spherical"] = spherical
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model = d.pop("model")

        projection = CameraModelOutProjection(d.pop("projection"))

        distortion = CameraModelOutDistortion(d.pop("distortion"))

        params = cast(list[str], d.pop("params", UNSET))

        aliases = cast(list[str], d.pop("aliases", UNSET))

        spherical = d.pop("spherical", UNSET)

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        camera_model_out = cls(
            model=model,
            projection=projection,
            distortion=distortion,
            params=params,
            aliases=aliases,
            spherical=spherical,
            notes=notes,
        )

        return camera_model_out
