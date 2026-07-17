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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.perspective_view_spec import PerspectiveViewSpec
    from ..models.projection_output_options import ProjectionOutputOptions
    from ..models.projection_sampling import ProjectionSampling


T = TypeVar("T", bound="PerspectiveProjectionSpec")


@_attrs_define
class PerspectiveProjectionSpec:
    """Equirectangular panorama to one or more perspective images.

    Attributes:
        convention (Literal['sfmapi-opencv'] | Unset):  Default: 'sfmapi-opencv'.
        views (list[PerspectiveViewSpec] | Unset):
        sampling (ProjectionSampling | Unset): Portable sampling controls for image projection jobs.
        output (ProjectionOutputOptions | Unset): Portable output controls shared by projection jobs.
    """

    convention: Literal["sfmapi-opencv"] | Unset = "sfmapi-opencv"
    views: list[PerspectiveViewSpec] | Unset = UNSET
    sampling: ProjectionSampling | Unset = UNSET
    output: ProjectionOutputOptions | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        convention = self.convention

        views: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.views, Unset):
            views = []
            for views_item_data in self.views:
                views_item = views_item_data.to_dict()
                views.append(views_item)

        sampling: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sampling, Unset):
            sampling = self.sampling.to_dict()

        output: dict[str, Any] | Unset = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if convention is not UNSET:
            field_dict["convention"] = convention
        if views is not UNSET:
            field_dict["views"] = views
        if sampling is not UNSET:
            field_dict["sampling"] = sampling
        if output is not UNSET:
            field_dict["output"] = output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.perspective_view_spec import PerspectiveViewSpec
        from ..models.projection_output_options import ProjectionOutputOptions
        from ..models.projection_sampling import ProjectionSampling

        d = dict(src_dict)
        convention = cast(Literal["sfmapi-opencv"] | Unset, d.pop("convention", UNSET))
        if convention != "sfmapi-opencv" and not isinstance(convention, Unset):
            raise ValueError(
                f"convention must match const 'sfmapi-opencv', got '{convention}'"
            )

        _views = d.pop("views", UNSET)
        views: list[PerspectiveViewSpec] | Unset = UNSET
        if _views is not UNSET:
            views = []
            for views_item_data in _views:
                views_item = PerspectiveViewSpec.from_dict(views_item_data)

                views.append(views_item)

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

        perspective_projection_spec = cls(
            convention=convention,
            views=views,
            sampling=sampling,
            output=output,
        )

        return perspective_projection_spec
