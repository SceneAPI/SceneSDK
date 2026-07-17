from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_pipeline_step_manifest import PluginPipelineStepManifest


T = TypeVar("T", bound="PluginPipelineManifest")


@_attrs_define
class PluginPipelineManifest:
    """
    Attributes:
        pipeline_id (str):
        title (str):
        steps (list[PluginPipelineStepManifest]):
        initial_inputs (list[str] | Unset):
        description (str | Unset):  Default: ''.
    """

    pipeline_id: str
    title: str
    steps: list[PluginPipelineStepManifest]
    initial_inputs: list[str] | Unset = UNSET
    description: str | Unset = ""

    def to_dict(self) -> dict[str, Any]:
        pipeline_id = self.pipeline_id

        title = self.title

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        initial_inputs: list[str] | Unset = UNSET
        if not isinstance(self.initial_inputs, Unset):
            initial_inputs = self.initial_inputs

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "pipeline_id": pipeline_id,
                "title": title,
                "steps": steps,
            }
        )
        if initial_inputs is not UNSET:
            field_dict["initial_inputs"] = initial_inputs
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_pipeline_step_manifest import PluginPipelineStepManifest

        d = dict(src_dict)
        pipeline_id = d.pop("pipeline_id")

        title = d.pop("title")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = PluginPipelineStepManifest.from_dict(steps_item_data)

            steps.append(steps_item)

        initial_inputs = cast(list[str], d.pop("initial_inputs", UNSET))

        description = d.pop("description", UNSET)

        plugin_pipeline_manifest = cls(
            pipeline_id=pipeline_id,
            title=title,
            steps=steps,
            initial_inputs=initial_inputs,
            description=description,
        )

        return plugin_pipeline_manifest
