from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerServiceMounts")


@_attrs_define
class ContainerServiceMounts:
    """
    Attributes:
        input_path (str | Unset):  Default: '/sfmapi/input'.
        output_path (str | Unset):  Default: '/sfmapi/output'.
        work_path (str | Unset):  Default: '/sfmapi/work'.
        log_path (str | Unset):  Default: '/sfmapi/logs'.
    """

    input_path: str | Unset = "/sfmapi/input"
    output_path: str | Unset = "/sfmapi/output"
    work_path: str | Unset = "/sfmapi/work"
    log_path: str | Unset = "/sfmapi/logs"

    def to_dict(self) -> dict[str, Any]:
        input_path = self.input_path

        output_path = self.output_path

        work_path = self.work_path

        log_path = self.log_path

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if input_path is not UNSET:
            field_dict["input_path"] = input_path
        if output_path is not UNSET:
            field_dict["output_path"] = output_path
        if work_path is not UNSET:
            field_dict["work_path"] = work_path
        if log_path is not UNSET:
            field_dict["log_path"] = log_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_path = d.pop("input_path", UNSET)

        output_path = d.pop("output_path", UNSET)

        work_path = d.pop("work_path", UNSET)

        log_path = d.pop("log_path", UNSET)

        container_service_mounts = cls(
            input_path=input_path,
            output_path=output_path,
            work_path=work_path,
            log_path=log_path,
        )

        return container_service_mounts
