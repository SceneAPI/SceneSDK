from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_pipeline_step_manifest_attributes import (
        PluginPipelineStepManifestAttributes,
    )
    from ..models.plugin_pipeline_step_manifest_wires import (
        PluginPipelineStepManifestWires,
    )


T = TypeVar("T", bound="PluginPipelineStepManifest")


@_attrs_define
class PluginPipelineStepManifest:
    """
    Attributes:
        ref (str):
        processor (str):
        attributes (PluginPipelineStepManifestAttributes | Unset):
        wires (PluginPipelineStepManifestWires | Unset):
    """

    ref: str
    processor: str
    attributes: PluginPipelineStepManifestAttributes | Unset = UNSET
    wires: PluginPipelineStepManifestWires | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        ref = self.ref

        processor = self.processor

        attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        wires: dict[str, Any] | Unset = UNSET
        if not isinstance(self.wires, Unset):
            wires = self.wires.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "ref": ref,
                "processor": processor,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if wires is not UNSET:
            field_dict["wires"] = wires

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_pipeline_step_manifest_attributes import (
            PluginPipelineStepManifestAttributes,
        )
        from ..models.plugin_pipeline_step_manifest_wires import (
            PluginPipelineStepManifestWires,
        )

        d = dict(src_dict)
        ref = d.pop("ref")

        processor = d.pop("processor")

        _attributes = d.pop("attributes", UNSET)
        attributes: PluginPipelineStepManifestAttributes | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = PluginPipelineStepManifestAttributes.from_dict(_attributes)

        _wires = d.pop("wires", UNSET)
        wires: PluginPipelineStepManifestWires | Unset
        if isinstance(_wires, Unset):
            wires = UNSET
        else:
            wires = PluginPipelineStepManifestWires.from_dict(_wires)

        plugin_pipeline_step_manifest = cls(
            ref=ref,
            processor=processor,
            attributes=attributes,
            wires=wires,
        )

        return plugin_pipeline_step_manifest
