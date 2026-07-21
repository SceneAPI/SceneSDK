from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UploadEntrySpec")


@_attrs_define
class UploadEntrySpec:
    """One image entry in an :class:`UploadSourceSpec`. Each entry binds
    a human-readable filename to a previously-finalized upload's
    canonical content-addressed sha (returned by ``POST
    /v1/uploads/{id}:finalize``).

        Attributes:
            name (str):
            blob_sha (str):
    """

    name: str
    blob_sha: str

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        blob_sha = self.blob_sha

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "blob_sha": blob_sha,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        blob_sha = d.pop("blob_sha")

        upload_entry_spec = cls(
            name=name,
            blob_sha=blob_sha,
        )

        return upload_entry_spec
