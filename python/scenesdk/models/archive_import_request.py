from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArchiveImportRequest")


@_attrs_define
class ArchiveImportRequest:
    """``POST /v1/projects/{pid}/datasets:fromArchive`` — register a
    dataset from an already-uploaded image zip.

    Upload the zip through the normal chunked-upload protocol first
    (``POST /v1/uploads`` → ``PATCH`` → ``:finalize`` → ``blob_sha``);
    this route only enqueues the unpack. The worker decodes the archive
    straight from the blob store (in memory for the ephemeral backend),
    extracts the image entries, and registers a derived dataset — one
    call instead of N per-image registrations.

        Attributes:
            blob_sha (str): Content address of the finalized zip upload.
            name (None | str | Unset):
            camera_model (str | Unset):  Default: 'SIMPLE_RADIAL'.
            intrinsics_mode (str | Unset):  Default: 'single_camera'.
            is_spherical (bool | Unset):  Default: False.
            image_prefix (None | str | Unset): Restrict the import to entries under this zip subpath (e.g. 'south-
                building/images/'). When unset the worker auto-detects the common image directory.
    """

    blob_sha: str
    name: None | str | Unset = UNSET
    camera_model: str | Unset = "SIMPLE_RADIAL"
    intrinsics_mode: str | Unset = "single_camera"
    is_spherical: bool | Unset = False
    image_prefix: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        blob_sha = self.blob_sha

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        camera_model = self.camera_model

        intrinsics_mode = self.intrinsics_mode

        is_spherical = self.is_spherical

        image_prefix: None | str | Unset
        if isinstance(self.image_prefix, Unset):
            image_prefix = UNSET
        else:
            image_prefix = self.image_prefix

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "blob_sha": blob_sha,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if camera_model is not UNSET:
            field_dict["camera_model"] = camera_model
        if intrinsics_mode is not UNSET:
            field_dict["intrinsics_mode"] = intrinsics_mode
        if is_spherical is not UNSET:
            field_dict["is_spherical"] = is_spherical
        if image_prefix is not UNSET:
            field_dict["image_prefix"] = image_prefix

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        blob_sha = d.pop("blob_sha")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        camera_model = d.pop("camera_model", UNSET)

        intrinsics_mode = d.pop("intrinsics_mode", UNSET)

        is_spherical = d.pop("is_spherical", UNSET)

        def _parse_image_prefix(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image_prefix = _parse_image_prefix(d.pop("image_prefix", UNSET))

        archive_import_request = cls(
            blob_sha=blob_sha,
            name=name,
            camera_model=camera_model,
            intrinsics_mode=intrinsics_mode,
            is_spherical=is_spherical,
            image_prefix=image_prefix,
        )

        return archive_import_request
