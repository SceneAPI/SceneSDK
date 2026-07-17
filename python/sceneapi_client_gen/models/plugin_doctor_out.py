from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.plugin_doctor_out_status import PluginDoctorOutStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.doctor_check import DoctorCheck


T = TypeVar("T", bound="PluginDoctorOut")


@_attrs_define
class PluginDoctorOut:
    """
    Attributes:
        plugin_id (str):
        status (PluginDoctorOutStatus):
        checks (list[DoctorCheck] | Unset):
    """

    plugin_id: str
    status: PluginDoctorOutStatus
    checks: list[DoctorCheck] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        plugin_id = self.plugin_id

        status = self.status.value

        checks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.checks, Unset):
            checks = []
            for checks_item_data in self.checks:
                checks_item = checks_item_data.to_dict()
                checks.append(checks_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "plugin_id": plugin_id,
                "status": status,
            }
        )
        if checks is not UNSET:
            field_dict["checks"] = checks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.doctor_check import DoctorCheck

        d = dict(src_dict)
        plugin_id = d.pop("plugin_id")

        status = PluginDoctorOutStatus(d.pop("status"))

        _checks = d.pop("checks", UNSET)
        checks: list[DoctorCheck] | Unset = UNSET
        if _checks is not UNSET:
            checks = []
            for checks_item_data in _checks:
                checks_item = DoctorCheck.from_dict(checks_item_data)

                checks.append(checks_item)

        plugin_doctor_out = cls(
            plugin_id=plugin_id,
            status=status,
            checks=checks,
        )

        return plugin_doctor_out
