from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArtifactValidationIssueOut")


@_attrs_define
class ArtifactValidationIssueOut:
    """One artifact validation problem or warning.

    Attributes:
        level (str):
        message (str):
        field (None | str | Unset):
    """

    level: str
    message: str
    field: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        level = self.level

        message = self.message

        field: None | str | Unset
        if isinstance(self.field, Unset):
            field = UNSET
        else:
            field = self.field

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "level": level,
                "message": message,
            }
        )
        if field is not UNSET:
            field_dict["field"] = field

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        level = d.pop("level")

        message = d.pop("message")

        def _parse_field(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        field = _parse_field(d.pop("field", UNSET))

        artifact_validation_issue_out = cls(
            level=level,
            message=message,
            field=field,
        )

        return artifact_validation_issue_out
