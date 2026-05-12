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

from ..models.cubemap_projection_spec_face_order_item import (
    CubemapProjectionSpecFaceOrderItem,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.projection_output_options import ProjectionOutputOptions
    from ..models.projection_sampling import ProjectionSampling


T = TypeVar("T", bound="CubemapProjectionSpec")


@_attrs_define
class CubemapProjectionSpec:
    """Equirectangular panorama to six cubemap faces.

    Attributes:
        convention (Literal['sfmapi-opencv'] | Unset):  Default: 'sfmapi-opencv'.
        face_size (int | Unset):  Default: 1024.
        face_order (list[CubemapProjectionSpecFaceOrderItem] | Unset):
        sampling (ProjectionSampling | Unset): Portable sampling controls for image projection jobs.
        output (ProjectionOutputOptions | Unset): Portable output controls shared by projection jobs.
    """

    convention: Literal["sfmapi-opencv"] | Unset = "sfmapi-opencv"
    face_size: int | Unset = 1024
    face_order: list[CubemapProjectionSpecFaceOrderItem] | Unset = UNSET
    sampling: ProjectionSampling | Unset = UNSET
    output: ProjectionOutputOptions | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        convention = self.convention

        face_size = self.face_size

        face_order: list[str] | Unset = UNSET
        if not isinstance(self.face_order, Unset):
            face_order = []
            for face_order_item_data in self.face_order:
                face_order_item = face_order_item_data.value
                face_order.append(face_order_item)

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
        if face_size is not UNSET:
            field_dict["face_size"] = face_size
        if face_order is not UNSET:
            field_dict["face_order"] = face_order
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

        face_size = d.pop("face_size", UNSET)

        _face_order = d.pop("face_order", UNSET)
        face_order: list[CubemapProjectionSpecFaceOrderItem] | Unset = UNSET
        if _face_order is not UNSET:
            face_order = []
            for face_order_item_data in _face_order:
                face_order_item = CubemapProjectionSpecFaceOrderItem(
                    face_order_item_data
                )

                face_order.append(face_order_item)

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

        cubemap_projection_spec = cls(
            convention=convention,
            face_size=face_size,
            face_order=face_order,
            sampling=sampling,
            output=output,
        )

        cubemap_projection_spec.additional_properties = d
        return cubemap_projection_spec

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
