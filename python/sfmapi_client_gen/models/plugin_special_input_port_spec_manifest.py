from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PluginSpecialInputPortSpecManifest")


@_attrs_define
class PluginSpecialInputPortSpecManifest:
    """
    Attributes:
        datatype (str):
        required (bool | Unset):  Default: False.
        multiple (bool | Unset):  Default: False.
        description (str | Unset):  Default: ''.
    """

    datatype: str
    required: bool | Unset = False
    multiple: bool | Unset = False
    description: str | Unset = ""

    def to_dict(self) -> dict[str, Any]:
        datatype = self.datatype

        required = self.required

        multiple = self.multiple

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "datatype": datatype,
            }
        )
        if required is not UNSET:
            field_dict["required"] = required
        if multiple is not UNSET:
            field_dict["multiple"] = multiple
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        datatype = d.pop("datatype")

        required = d.pop("required", UNSET)

        multiple = d.pop("multiple", UNSET)

        description = d.pop("description", UNSET)

        plugin_special_input_port_spec_manifest = cls(
            datatype=datatype,
            required=required,
            multiple=multiple,
            description=description,
        )

        return plugin_special_input_port_spec_manifest
