from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.projection_job_request_operation import ProjectionJobRequestOperation
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cubemap_projection_spec import CubemapProjectionSpec
    from ..models.equirectangular_projection_spec import EquirectangularProjectionSpec
    from ..models.perspective_projection_spec import PerspectiveProjectionSpec


T = TypeVar("T", bound="ProjectionJobRequest")


@_attrs_define
class ProjectionJobRequest:
    """Dataset-level projection job request.

    Only the spec matching ``operation`` is used. Missing matching specs
    are filled with their portable defaults.

        Attributes:
            operation (ProjectionJobRequestOperation | Unset):  Default:
                ProjectionJobRequestOperation.EQUIRECTANGULAR_TO_CUBEMAP.
            cubemap (CubemapProjectionSpec | None | Unset):
            equirectangular (EquirectangularProjectionSpec | None | Unset):
            perspective (None | PerspectiveProjectionSpec | Unset):
    """

    operation: ProjectionJobRequestOperation | Unset = (
        ProjectionJobRequestOperation.EQUIRECTANGULAR_TO_CUBEMAP
    )
    cubemap: CubemapProjectionSpec | None | Unset = UNSET
    equirectangular: EquirectangularProjectionSpec | None | Unset = UNSET
    perspective: None | PerspectiveProjectionSpec | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cubemap_projection_spec import CubemapProjectionSpec
        from ..models.equirectangular_projection_spec import (
            EquirectangularProjectionSpec,
        )
        from ..models.perspective_projection_spec import PerspectiveProjectionSpec

        operation: str | Unset = UNSET
        if not isinstance(self.operation, Unset):
            operation = self.operation.value

        cubemap: dict[str, Any] | None | Unset
        if isinstance(self.cubemap, Unset):
            cubemap = UNSET
        elif isinstance(self.cubemap, CubemapProjectionSpec):
            cubemap = self.cubemap.to_dict()
        else:
            cubemap = self.cubemap

        equirectangular: dict[str, Any] | None | Unset
        if isinstance(self.equirectangular, Unset):
            equirectangular = UNSET
        elif isinstance(self.equirectangular, EquirectangularProjectionSpec):
            equirectangular = self.equirectangular.to_dict()
        else:
            equirectangular = self.equirectangular

        perspective: dict[str, Any] | None | Unset
        if isinstance(self.perspective, Unset):
            perspective = UNSET
        elif isinstance(self.perspective, PerspectiveProjectionSpec):
            perspective = self.perspective.to_dict()
        else:
            perspective = self.perspective

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if operation is not UNSET:
            field_dict["operation"] = operation
        if cubemap is not UNSET:
            field_dict["cubemap"] = cubemap
        if equirectangular is not UNSET:
            field_dict["equirectangular"] = equirectangular
        if perspective is not UNSET:
            field_dict["perspective"] = perspective

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cubemap_projection_spec import CubemapProjectionSpec
        from ..models.equirectangular_projection_spec import (
            EquirectangularProjectionSpec,
        )
        from ..models.perspective_projection_spec import PerspectiveProjectionSpec

        d = dict(src_dict)
        _operation = d.pop("operation", UNSET)
        operation: ProjectionJobRequestOperation | Unset
        if isinstance(_operation, Unset):
            operation = UNSET
        else:
            operation = ProjectionJobRequestOperation(_operation)

        def _parse_cubemap(data: object) -> CubemapProjectionSpec | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cubemap_type_0 = CubemapProjectionSpec.from_dict(data)

                return cubemap_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CubemapProjectionSpec | None | Unset, data)

        cubemap = _parse_cubemap(d.pop("cubemap", UNSET))

        def _parse_equirectangular(
            data: object,
        ) -> EquirectangularProjectionSpec | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                equirectangular_type_0 = EquirectangularProjectionSpec.from_dict(data)

                return equirectangular_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EquirectangularProjectionSpec | None | Unset, data)

        equirectangular = _parse_equirectangular(d.pop("equirectangular", UNSET))

        def _parse_perspective(
            data: object,
        ) -> None | PerspectiveProjectionSpec | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                perspective_type_0 = PerspectiveProjectionSpec.from_dict(data)

                return perspective_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PerspectiveProjectionSpec | Unset, data)

        perspective = _parse_perspective(d.pop("perspective", UNSET))

        projection_job_request = cls(
            operation=operation,
            cubemap=cubemap,
            equirectangular=equirectangular,
            perspective=perspective,
        )

        projection_job_request.additional_properties = d
        return projection_job_request

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
