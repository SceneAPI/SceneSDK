from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.projection_sampling_interpolation import ProjectionSamplingInterpolation
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectionSampling")


@_attrs_define
class ProjectionSampling:
    """Portable sampling controls for image projection jobs.

    Attributes:
        interpolation (ProjectionSamplingInterpolation | Unset):  Default: ProjectionSamplingInterpolation.LINEAR.
        antialias (bool | Unset):  Default: True.
        seam_padding_px (int | Unset):  Default: 0.
        overlap_px (int | Unset):  Default: 0.
    """

    interpolation: ProjectionSamplingInterpolation | Unset = (
        ProjectionSamplingInterpolation.LINEAR
    )
    antialias: bool | Unset = True
    seam_padding_px: int | Unset = 0
    overlap_px: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        interpolation: str | Unset = UNSET
        if not isinstance(self.interpolation, Unset):
            interpolation = self.interpolation.value

        antialias = self.antialias

        seam_padding_px = self.seam_padding_px

        overlap_px = self.overlap_px

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if interpolation is not UNSET:
            field_dict["interpolation"] = interpolation
        if antialias is not UNSET:
            field_dict["antialias"] = antialias
        if seam_padding_px is not UNSET:
            field_dict["seam_padding_px"] = seam_padding_px
        if overlap_px is not UNSET:
            field_dict["overlap_px"] = overlap_px

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _interpolation = d.pop("interpolation", UNSET)
        interpolation: ProjectionSamplingInterpolation | Unset
        if isinstance(_interpolation, Unset):
            interpolation = UNSET
        else:
            interpolation = ProjectionSamplingInterpolation(_interpolation)

        antialias = d.pop("antialias", UNSET)

        seam_padding_px = d.pop("seam_padding_px", UNSET)

        overlap_px = d.pop("overlap_px", UNSET)

        projection_sampling = cls(
            interpolation=interpolation,
            antialias=antialias,
            seam_padding_px=seam_padding_px,
            overlap_px=overlap_px,
        )

        projection_sampling.additional_properties = d
        return projection_sampling

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
