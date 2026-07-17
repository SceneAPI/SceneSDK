from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pipeline_step import PipelineStep
    from ..models.processor_pipeline_step import ProcessorPipelineStep


T = TypeVar("T", bound="PipelineRunRequest")


@_attrs_define
class PipelineRunRequest:
    """
    Attributes:
        dataset_id (str):
        steps (list[PipelineStep | ProcessorPipelineStep | str]):
        initial_inputs (list[str] | Unset): Legacy compatibility list of initial DataType ids available as synthetic
            inputs.* ports. New Processor pipelines should prefer reference-keyed initial inputs when that durable shape is
            enabled.
    """

    dataset_id: str
    steps: list[PipelineStep | ProcessorPipelineStep | str]
    initial_inputs: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.pipeline_step import PipelineStep
        from ..models.processor_pipeline_step import ProcessorPipelineStep

        dataset_id = self.dataset_id

        steps = []
        for steps_item_data in self.steps:
            steps_item: dict[str, Any] | str
            if isinstance(steps_item_data, ProcessorPipelineStep):
                steps_item = steps_item_data.to_dict()
            elif isinstance(steps_item_data, PipelineStep):
                steps_item = steps_item_data.to_dict()
            else:
                steps_item = steps_item_data
            steps.append(steps_item)

        initial_inputs: list[str] | Unset = UNSET
        if not isinstance(self.initial_inputs, Unset):
            initial_inputs = self.initial_inputs

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "dataset_id": dataset_id,
                "steps": steps,
            }
        )
        if initial_inputs is not UNSET:
            field_dict["initial_inputs"] = initial_inputs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pipeline_step import PipelineStep
        from ..models.processor_pipeline_step import ProcessorPipelineStep

        d = dict(src_dict)
        dataset_id = d.pop("dataset_id")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:

            def _parse_steps_item(
                data: object,
            ) -> PipelineStep | ProcessorPipelineStep | str:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    steps_item_type_1 = ProcessorPipelineStep.from_dict(data)

                    return steps_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    steps_item_type_2 = PipelineStep.from_dict(data)

                    return steps_item_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(PipelineStep | ProcessorPipelineStep | str, data)

            steps_item = _parse_steps_item(steps_item_data)

            steps.append(steps_item)

        initial_inputs = cast(list[str], d.pop("initial_inputs", UNSET))

        pipeline_run_request = cls(
            dataset_id=dataset_id,
            steps=steps,
            initial_inputs=initial_inputs,
        )

        return pipeline_run_request
