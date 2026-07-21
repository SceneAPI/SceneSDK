from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.processor_pipeline_step_attributes import (
        ProcessorPipelineStepAttributes,
    )
    from ..models.processor_pipeline_step_params import ProcessorPipelineStepParams
    from ..models.processor_pipeline_step_wires import ProcessorPipelineStepWires


T = TypeVar("T", bound="ProcessorPipelineStep")


@_attrs_define
class ProcessorPipelineStep:
    """One native Processor instance in a typed pipeline.

    Attributes:
        processor (str):
        ref (None | str | Unset):
        provider (None | str | Unset):
        attributes (ProcessorPipelineStepAttributes | Unset):
        params (ProcessorPipelineStepParams | Unset): Legacy alias for attributes; attributes win on overlap.
        wires (ProcessorPipelineStepWires | Unset):
    """

    processor: str
    ref: None | str | Unset = UNSET
    provider: None | str | Unset = UNSET
    attributes: ProcessorPipelineStepAttributes | Unset = UNSET
    params: ProcessorPipelineStepParams | Unset = UNSET
    wires: ProcessorPipelineStepWires | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        processor = self.processor

        ref: None | str | Unset
        if isinstance(self.ref, Unset):
            ref = UNSET
        else:
            ref = self.ref

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict() if hasattr(self.attributes, "to_dict") else dict(self.attributes)

        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict() if hasattr(self.params, "to_dict") else dict(self.params)

        wires: dict[str, Any] | Unset = UNSET
        if not isinstance(self.wires, Unset):
            wires = self.wires.to_dict() if hasattr(self.wires, "to_dict") else dict(self.wires)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "processor": processor,
            }
        )
        if ref is not UNSET:
            field_dict["ref"] = ref
        if provider is not UNSET:
            field_dict["provider"] = provider
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if params is not UNSET:
            field_dict["params"] = params
        if wires is not UNSET:
            field_dict["wires"] = wires

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.processor_pipeline_step_attributes import (
            ProcessorPipelineStepAttributes,
        )
        from ..models.processor_pipeline_step_params import ProcessorPipelineStepParams
        from ..models.processor_pipeline_step_wires import ProcessorPipelineStepWires

        d = dict(src_dict)
        processor = d.pop("processor")

        def _parse_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ref = _parse_ref(d.pop("ref", UNSET))

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        _attributes = d.pop("attributes", UNSET)
        attributes: ProcessorPipelineStepAttributes | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = ProcessorPipelineStepAttributes.from_dict(_attributes)

        _params = d.pop("params", UNSET)
        params: ProcessorPipelineStepParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = ProcessorPipelineStepParams.from_dict(_params)

        _wires = d.pop("wires", UNSET)
        wires: ProcessorPipelineStepWires | Unset
        if isinstance(_wires, Unset):
            wires = UNSET
        else:
            wires = ProcessorPipelineStepWires.from_dict(_wires)

        processor_pipeline_step = cls(
            processor=processor,
            ref=ref,
            provider=provider,
            attributes=attributes,
            params=params,
            wires=wires,
        )

        return processor_pipeline_step
