from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.doctor_check_status import DoctorCheckStatus

T = TypeVar("T", bound="DoctorCheck")


@_attrs_define
class DoctorCheck:
    """
    Attributes:
        name (str):
        status (DoctorCheckStatus):
        detail (str):
    """

    name: str
    status: DoctorCheckStatus
    detail: str

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status = self.status.value

        detail = self.detail

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "status": status,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        status = DoctorCheckStatus(d.pop("status"))

        detail = d.pop("detail")

        doctor_check = cls(
            name=name,
            status=status,
            detail=detail,
        )

        return doctor_check
