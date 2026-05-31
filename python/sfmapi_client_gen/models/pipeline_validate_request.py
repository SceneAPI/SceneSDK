from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="PipelineValidateRequest")


@_attrs_define
class PipelineValidateRequest:
    """
    Attributes:
        steps (list[str]):
    """

    steps: list[str]

    def to_dict(self) -> dict[str, Any]:
        steps = self.steps

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "steps": steps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        steps = cast(list[str], d.pop("steps"))

        pipeline_validate_request = cls(
            steps=steps,
        )

        return pipeline_validate_request
