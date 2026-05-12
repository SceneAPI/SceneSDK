from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.conformance_status import ConformanceStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Conformance")


@_attrs_define
class Conformance:
    """
    Attributes:
        status (ConformanceStatus | Unset):  Default: ConformanceStatus.NOT_RUN.
        suite (None | str | Unset):
        report_url (None | str | Unset):
        checked_at (None | str | Unset):
    """

    status: ConformanceStatus | Unset = ConformanceStatus.NOT_RUN
    suite: None | str | Unset = UNSET
    report_url: None | str | Unset = UNSET
    checked_at: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        suite: None | str | Unset
        if isinstance(self.suite, Unset):
            suite = UNSET
        else:
            suite = self.suite

        report_url: None | str | Unset
        if isinstance(self.report_url, Unset):
            report_url = UNSET
        else:
            report_url = self.report_url

        checked_at: None | str | Unset
        if isinstance(self.checked_at, Unset):
            checked_at = UNSET
        else:
            checked_at = self.checked_at

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if suite is not UNSET:
            field_dict["suite"] = suite
        if report_url is not UNSET:
            field_dict["report_url"] = report_url
        if checked_at is not UNSET:
            field_dict["checked_at"] = checked_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _status = d.pop("status", UNSET)
        status: ConformanceStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ConformanceStatus(_status)

        def _parse_suite(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        suite = _parse_suite(d.pop("suite", UNSET))

        def _parse_report_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        report_url = _parse_report_url(d.pop("report_url", UNSET))

        def _parse_checked_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        checked_at = _parse_checked_at(d.pop("checked_at", UNSET))

        conformance = cls(
            status=status,
            suite=suite,
            report_url=report_url,
            checked_at=checked_at,
        )

        return conformance
