from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="KaptureImportRequest")


@_attrs_define
class KaptureImportRequest:
    """``POST /v1/projects/{pid}/datasets:import_kapture``.

    Attributes:
        archive_path (str):
    """

    archive_path: str

    def to_dict(self) -> dict[str, Any]:
        archive_path = self.archive_path

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "archive_path": archive_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        archive_path = d.pop("archive_path")

        kapture_import_request = cls(
            archive_path=archive_path,
        )

        return kapture_import_request
