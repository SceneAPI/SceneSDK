from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_attribute_manifest import PluginAttributeManifest
    from ..models.plugin_processor_manifest_consumer import (
        PluginProcessorManifestConsumer,
    )
    from ..models.plugin_processor_manifest_supplier import (
        PluginProcessorManifestSupplier,
    )


T = TypeVar("T", bound="PluginProcessorManifest")


@_attrs_define
class PluginProcessorManifest:
    """
    Attributes:
        processor_id (str):
        title (str):
        consumer (PluginProcessorManifestConsumer):
        supplier (PluginProcessorManifestSupplier):
        capabilities (list[str]):
        attributes (list[PluginAttributeManifest] | Unset):
        description (str | Unset):  Default: ''.
    """

    processor_id: str
    title: str
    consumer: PluginProcessorManifestConsumer
    supplier: PluginProcessorManifestSupplier
    capabilities: list[str]
    attributes: list[PluginAttributeManifest] | Unset = UNSET
    description: str | Unset = ""

    def to_dict(self) -> dict[str, Any]:
        processor_id = self.processor_id

        title = self.title

        consumer = self.consumer.to_dict()

        supplier = self.supplier.to_dict()

        capabilities = self.capabilities

        attributes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = []
            for attributes_item_data in self.attributes:
                attributes_item = attributes_item_data.to_dict()
                attributes.append(attributes_item)

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "processor_id": processor_id,
                "title": title,
                "consumer": consumer,
                "supplier": supplier,
                "capabilities": capabilities,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_attribute_manifest import PluginAttributeManifest
        from ..models.plugin_processor_manifest_consumer import (
            PluginProcessorManifestConsumer,
        )
        from ..models.plugin_processor_manifest_supplier import (
            PluginProcessorManifestSupplier,
        )

        d = dict(src_dict)
        processor_id = d.pop("processor_id")

        title = d.pop("title")

        consumer = PluginProcessorManifestConsumer.from_dict(d.pop("consumer"))

        supplier = PluginProcessorManifestSupplier.from_dict(d.pop("supplier"))

        capabilities = cast(list[str], d.pop("capabilities"))

        _attributes = d.pop("attributes", UNSET)
        attributes: list[PluginAttributeManifest] | Unset = UNSET
        if _attributes is not UNSET:
            attributes = []
            for attributes_item_data in _attributes:
                attributes_item = PluginAttributeManifest.from_dict(
                    attributes_item_data
                )

                attributes.append(attributes_item)

        description = d.pop("description", UNSET)

        plugin_processor_manifest = cls(
            processor_id=processor_id,
            title=title,
            consumer=consumer,
            supplier=supplier,
            capabilities=capabilities,
            attributes=attributes,
            description=description,
        )

        return plugin_processor_manifest
