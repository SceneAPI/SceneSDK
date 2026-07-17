from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.projection_output_options_format import ProjectionOutputOptionsFormat
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectionOutputOptions")


@_attrs_define
class ProjectionOutputOptions:
    """Portable output controls shared by projection jobs.

    Attributes:
        format_ (ProjectionOutputOptionsFormat | Unset):  Default: ProjectionOutputOptionsFormat.SOURCE.
        jpeg_quality (int | Unset):  Default: 92.
        write_manifest (bool | Unset):  Default: True.
        create_dataset (bool | Unset):  Default: True.
        dataset_name (None | str | Unset):
    """

    format_: ProjectionOutputOptionsFormat | Unset = (
        ProjectionOutputOptionsFormat.SOURCE
    )
    jpeg_quality: int | Unset = 92
    write_manifest: bool | Unset = True
    create_dataset: bool | Unset = True
    dataset_name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        format_: str | Unset = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value

        jpeg_quality = self.jpeg_quality

        write_manifest = self.write_manifest

        create_dataset = self.create_dataset

        dataset_name: None | str | Unset
        if isinstance(self.dataset_name, Unset):
            dataset_name = UNSET
        else:
            dataset_name = self.dataset_name

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if format_ is not UNSET:
            field_dict["format"] = format_
        if jpeg_quality is not UNSET:
            field_dict["jpeg_quality"] = jpeg_quality
        if write_manifest is not UNSET:
            field_dict["write_manifest"] = write_manifest
        if create_dataset is not UNSET:
            field_dict["create_dataset"] = create_dataset
        if dataset_name is not UNSET:
            field_dict["dataset_name"] = dataset_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _format_ = d.pop("format", UNSET)
        format_: ProjectionOutputOptionsFormat | Unset
        if isinstance(_format_, Unset):
            format_ = UNSET
        else:
            format_ = ProjectionOutputOptionsFormat(_format_)

        jpeg_quality = d.pop("jpeg_quality", UNSET)

        write_manifest = d.pop("write_manifest", UNSET)

        create_dataset = d.pop("create_dataset", UNSET)

        def _parse_dataset_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_name = _parse_dataset_name(d.pop("dataset_name", UNSET))

        projection_output_options = cls(
            format_=format_,
            jpeg_quality=jpeg_quality,
            write_manifest=write_manifest,
            create_dataset=create_dataset,
            dataset_name=dataset_name,
        )

        return projection_output_options
