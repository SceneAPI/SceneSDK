from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.pipeline_step import PipelineStep


T = TypeVar("T", bound="PipelineRunRequest")


@_attrs_define
class PipelineRunRequest:
    """
    Attributes:
        dataset_id (str):
        steps (list[PipelineStep]):
    """

    dataset_id: str
    steps: list[PipelineStep]

    def to_dict(self) -> dict[str, Any]:
        dataset_id = self.dataset_id

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "dataset_id": dataset_id,
                "steps": steps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pipeline_step import PipelineStep

        d = dict(src_dict)
        dataset_id = d.pop("dataset_id")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = PipelineStep.from_dict(steps_item_data)

            steps.append(steps_item)

        pipeline_run_request = cls(
            dataset_id=dataset_id,
            steps=steps,
        )

        return pipeline_run_request
