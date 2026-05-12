from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.projection_output_options import ProjectionOutputOptions
    from ..models.projection_sampling import ProjectionSampling


T = TypeVar("T", bound="EquirectangularProjectionSpec")


@_attrs_define
class EquirectangularProjectionSpec:
    """Cubemap faces back to an equirectangular panorama.

    Attributes:
        convention (Literal['sfmapi-opencv'] | Unset):  Default: 'sfmapi-opencv'.
        width (int | None | Unset):
        height (int | None | Unset):
        sampling (ProjectionSampling | Unset): Portable sampling controls for image projection jobs.
        output (ProjectionOutputOptions | Unset): Portable output controls shared by projection jobs.
    """

    convention: Literal["sfmapi-opencv"] | Unset = "sfmapi-opencv"
    width: int | None | Unset = UNSET
    height: int | None | Unset = UNSET
    sampling: ProjectionSampling | Unset = UNSET
    output: ProjectionOutputOptions | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        convention = self.convention

        width: int | None | Unset
        if isinstance(self.width, Unset):
            width = UNSET
        else:
            width = self.width

        height: int | None | Unset
        if isinstance(self.height, Unset):
            height = UNSET
        else:
            height = self.height

        sampling: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sampling, Unset):
            sampling = self.sampling.to_dict()

        output: dict[str, Any] | Unset = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if convention is not UNSET:
            field_dict["convention"] = convention
        if width is not UNSET:
            field_dict["width"] = width
        if height is not UNSET:
            field_dict["height"] = height
        if sampling is not UNSET:
            field_dict["sampling"] = sampling
        if output is not UNSET:
            field_dict["output"] = output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.projection_output_options import ProjectionOutputOptions
        from ..models.projection_sampling import ProjectionSampling

        d = dict(src_dict)
        convention = cast(Literal["sfmapi-opencv"] | Unset, d.pop("convention", UNSET))
        if convention != "sfmapi-opencv" and not isinstance(convention, Unset):
            raise ValueError(
                f"convention must match const 'sfmapi-opencv', got '{convention}'"
            )

        def _parse_width(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        width = _parse_width(d.pop("width", UNSET))

        def _parse_height(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        height = _parse_height(d.pop("height", UNSET))

        _sampling = d.pop("sampling", UNSET)
        sampling: ProjectionSampling | Unset
        if isinstance(_sampling, Unset):
            sampling = UNSET
        else:
            sampling = ProjectionSampling.from_dict(_sampling)

        _output = d.pop("output", UNSET)
        output: ProjectionOutputOptions | Unset
        if isinstance(_output, Unset):
            output = UNSET
        else:
            output = ProjectionOutputOptions.from_dict(_output)

        equirectangular_projection_spec = cls(
            convention=convention,
            width=width,
            height=height,
            sampling=sampling,
            output=output,
        )

        equirectangular_projection_spec.additional_properties = d
        return equirectangular_projection_spec

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
