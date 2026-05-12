from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_conversion_step_out import ArtifactConversionStepOut


T = TypeVar("T", bound="ArtifactConversionPlanOut")


@_attrs_define
class ArtifactConversionPlanOut:
    """Conversion compatibility result for an artifact.

    Attributes:
        artifact_id (str):
        target_format (str):
        conversion_required (bool):
        executable (bool):
        source_format (None | str | Unset):
        reason (None | str | Unset):
        steps (list[ArtifactConversionStepOut] | Unset):
    """

    artifact_id: str
    target_format: str
    conversion_required: bool
    executable: bool
    source_format: None | str | Unset = UNSET
    reason: None | str | Unset = UNSET
    steps: list[ArtifactConversionStepOut] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        artifact_id = self.artifact_id

        target_format = self.target_format

        conversion_required = self.conversion_required

        executable = self.executable

        source_format: None | str | Unset
        if isinstance(self.source_format, Unset):
            source_format = UNSET
        else:
            source_format = self.source_format

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        steps: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item = steps_item_data.to_dict()
                steps.append(steps_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "artifact_id": artifact_id,
                "target_format": target_format,
                "conversion_required": conversion_required,
                "executable": executable,
            }
        )
        if source_format is not UNSET:
            field_dict["source_format"] = source_format
        if reason is not UNSET:
            field_dict["reason"] = reason
        if steps is not UNSET:
            field_dict["steps"] = steps

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_conversion_step_out import ArtifactConversionStepOut

        d = dict(src_dict)
        artifact_id = d.pop("artifact_id")

        target_format = d.pop("target_format")

        conversion_required = d.pop("conversion_required")

        executable = d.pop("executable")

        def _parse_source_format(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_format = _parse_source_format(d.pop("source_format", UNSET))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        _steps = d.pop("steps", UNSET)
        steps: list[ArtifactConversionStepOut] | Unset = UNSET
        if _steps is not UNSET:
            steps = []
            for steps_item_data in _steps:
                steps_item = ArtifactConversionStepOut.from_dict(steps_item_data)

                steps.append(steps_item)

        artifact_conversion_plan_out = cls(
            artifact_id=artifact_id,
            target_format=target_format,
            conversion_required=conversion_required,
            executable=executable,
            source_format=source_format,
            reason=reason,
            steps=steps,
        )

        return artifact_conversion_plan_out
