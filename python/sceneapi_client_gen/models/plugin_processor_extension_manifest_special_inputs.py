from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PluginProcessorExtensionManifestSpecialInputs")


@_attrs_define
class PluginProcessorExtensionManifestSpecialInputs:
    """Plugin-qualified extension input roles. JSON Schema validates the qualified-name shape; runtime PluginManifest
    validation also requires the prefix to match plugin_id.

    """

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        plugin_processor_extension_manifest_special_inputs = cls()

        return plugin_processor_extension_manifest_special_inputs
