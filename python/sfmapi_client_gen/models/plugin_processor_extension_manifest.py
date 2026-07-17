from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_processor_extension_manifest_special_inputs import (
        PluginProcessorExtensionManifestSpecialInputs,
    )
    from ..models.plugin_special_attribute_manifest import (
        PluginSpecialAttributeManifest,
    )


T = TypeVar("T", bound="PluginProcessorExtensionManifest")


@_attrs_define
class PluginProcessorExtensionManifest:
    """
    Attributes:
        processor_id (str):
        special_inputs (PluginProcessorExtensionManifestSpecialInputs | Unset): Plugin-qualified extension input roles.
            JSON Schema validates the qualified-name shape; runtime PluginManifest validation also requires the prefix to
            match plugin_id.
        special_attributes (list[PluginSpecialAttributeManifest] | Unset): Plugin-qualified extension attributes. JSON
            Schema validates the qualified-name shape; runtime PluginManifest validation also requires the prefix to match
            plugin_id.
    """

    processor_id: str
    special_inputs: PluginProcessorExtensionManifestSpecialInputs | Unset = UNSET
    special_attributes: list[PluginSpecialAttributeManifest] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        processor_id = self.processor_id

        special_inputs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.special_inputs, Unset):
            special_inputs = self.special_inputs.to_dict()

        special_attributes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.special_attributes, Unset):
            special_attributes = []
            for special_attributes_item_data in self.special_attributes:
                special_attributes_item = special_attributes_item_data.to_dict()
                special_attributes.append(special_attributes_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "processor_id": processor_id,
            }
        )
        if special_inputs is not UNSET:
            field_dict["special_inputs"] = special_inputs
        if special_attributes is not UNSET:
            field_dict["special_attributes"] = special_attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_processor_extension_manifest_special_inputs import (
            PluginProcessorExtensionManifestSpecialInputs,
        )
        from ..models.plugin_special_attribute_manifest import (
            PluginSpecialAttributeManifest,
        )

        d = dict(src_dict)
        processor_id = d.pop("processor_id")

        _special_inputs = d.pop("special_inputs", UNSET)
        special_inputs: PluginProcessorExtensionManifestSpecialInputs | Unset
        if isinstance(_special_inputs, Unset):
            special_inputs = UNSET
        else:
            special_inputs = PluginProcessorExtensionManifestSpecialInputs.from_dict(
                _special_inputs
            )

        _special_attributes = d.pop("special_attributes", UNSET)
        special_attributes: list[PluginSpecialAttributeManifest] | Unset = UNSET
        if _special_attributes is not UNSET:
            special_attributes = []
            for special_attributes_item_data in _special_attributes:
                special_attributes_item = PluginSpecialAttributeManifest.from_dict(
                    special_attributes_item_data
                )

                special_attributes.append(special_attributes_item)

        plugin_processor_extension_manifest = cls(
            processor_id=processor_id,
            special_inputs=special_inputs,
            special_attributes=special_attributes,
        )

        return plugin_processor_extension_manifest
