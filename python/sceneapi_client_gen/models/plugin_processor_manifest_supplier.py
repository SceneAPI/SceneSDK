from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.plugin_port_spec_manifest import PluginPortSpecManifest


T = TypeVar("T", bound="PluginProcessorManifestSupplier")


@_attrs_define
class PluginProcessorManifestSupplier:
    """ """

    additional_properties: dict[str, PluginPortSpecManifest] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_port_spec_manifest import PluginPortSpecManifest

        d = dict(src_dict)
        plugin_processor_manifest_supplier = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = PluginPortSpecManifest.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        plugin_processor_manifest_supplier.additional_properties = additional_properties
        return plugin_processor_manifest_supplier

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> PluginPortSpecManifest:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: PluginPortSpecManifest) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
