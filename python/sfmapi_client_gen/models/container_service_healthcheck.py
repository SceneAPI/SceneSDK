from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerServiceHealthcheck")


@_attrs_define
class ContainerServiceHealthcheck:
    """
    Attributes:
        path (str | Unset):  Default: '/healthz'.
        timeout_seconds (int | Unset):  Default: 5.
    """

    path: str | Unset = "/healthz"
    timeout_seconds: int | Unset = 5

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        timeout_seconds = self.timeout_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path", UNSET)

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        container_service_healthcheck = cls(
            path=path,
            timeout_seconds=timeout_seconds,
        )

        return container_service_healthcheck
