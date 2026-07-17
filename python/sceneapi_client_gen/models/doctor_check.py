from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.doctor_check_status import DoctorCheckStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.doctor_check_metadata import DoctorCheckMetadata


T = TypeVar("T", bound="DoctorCheck")


@_attrs_define
class DoctorCheck:
    """
    Attributes:
        name (str):
        status (DoctorCheckStatus):
        detail (str):
        metadata (DoctorCheckMetadata | Unset):
    """

    name: str
    status: DoctorCheckStatus
    detail: str
    metadata: DoctorCheckMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status = self.status.value

        detail = self.detail

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "status": status,
                "detail": detail,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.doctor_check_metadata import DoctorCheckMetadata

        d = dict(src_dict)
        name = d.pop("name")

        status = DoctorCheckStatus(d.pop("status"))

        detail = d.pop("detail")

        _metadata = d.pop("metadata", UNSET)
        metadata: DoctorCheckMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = DoctorCheckMetadata.from_dict(_metadata)

        doctor_check = cls(
            name=name,
            status=status,
            detail=detail,
            metadata=metadata,
        )

        return doctor_check
