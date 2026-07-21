from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_validation_issue_out import ArtifactValidationIssueOut


T = TypeVar("T", bound="ArtifactValidationOut")


@_attrs_define
class ArtifactValidationOut:
    """Best-effort validation result for an artifact descriptor and bytes.

    Attributes:
        artifact_id (str):
        valid (bool):
        artifact_format (None | str | Unset):
        datatype (None | str | Unset):
        checked_content (bool | Unset):  Default: False.
        issues (list[ArtifactValidationIssueOut] | Unset):
    """

    artifact_id: str
    valid: bool
    artifact_format: None | str | Unset = UNSET
    datatype: None | str | Unset = UNSET
    checked_content: bool | Unset = False
    issues: list[ArtifactValidationIssueOut] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        artifact_id = self.artifact_id

        valid = self.valid

        artifact_format: None | str | Unset
        if isinstance(self.artifact_format, Unset):
            artifact_format = UNSET
        else:
            artifact_format = self.artifact_format

        datatype: None | str | Unset
        if isinstance(self.datatype, Unset):
            datatype = UNSET
        else:
            datatype = self.datatype

        checked_content = self.checked_content

        issues: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.issues, Unset):
            issues = []
            for issues_item_data in self.issues:
                issues_item = issues_item_data.to_dict()
                issues.append(issues_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "artifact_id": artifact_id,
                "valid": valid,
            }
        )
        if artifact_format is not UNSET:
            field_dict["artifact_format"] = artifact_format
        if datatype is not UNSET:
            field_dict["datatype"] = datatype
        if checked_content is not UNSET:
            field_dict["checked_content"] = checked_content
        if issues is not UNSET:
            field_dict["issues"] = issues

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_validation_issue_out import ArtifactValidationIssueOut

        d = dict(src_dict)
        artifact_id = d.pop("artifact_id")

        valid = d.pop("valid")

        def _parse_artifact_format(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        artifact_format = _parse_artifact_format(d.pop("artifact_format", UNSET))

        def _parse_datatype(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        datatype = _parse_datatype(d.pop("datatype", UNSET))

        checked_content = d.pop("checked_content", UNSET)

        _issues = d.pop("issues", UNSET)
        issues: list[ArtifactValidationIssueOut] | Unset = UNSET
        if _issues is not UNSET:
            issues = []
            for issues_item_data in _issues:
                issues_item = ArtifactValidationIssueOut.from_dict(issues_item_data)

                issues.append(issues_item)

        artifact_validation_out = cls(
            artifact_id=artifact_id,
            valid=valid,
            artifact_format=artifact_format,
            datatype=datatype,
            checked_content=checked_content,
            issues=issues,
        )

        return artifact_validation_out
