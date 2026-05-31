from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerServiceRetry")


@_attrs_define
class ContainerServiceRetry:
    """
    Attributes:
        max_attempts (int | Unset):  Default: 1.
        backoff_seconds (int | Unset):  Default: 0.
    """

    max_attempts: int | Unset = 1
    backoff_seconds: int | Unset = 0

    def to_dict(self) -> dict[str, Any]:
        max_attempts = self.max_attempts

        backoff_seconds = self.backoff_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if max_attempts is not UNSET:
            field_dict["max_attempts"] = max_attempts
        if backoff_seconds is not UNSET:
            field_dict["backoff_seconds"] = backoff_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_attempts = d.pop("max_attempts", UNSET)

        backoff_seconds = d.pop("backoff_seconds", UNSET)

        container_service_retry = cls(
            max_attempts=max_attempts,
            backoff_seconds=backoff_seconds,
        )

        return container_service_retry
