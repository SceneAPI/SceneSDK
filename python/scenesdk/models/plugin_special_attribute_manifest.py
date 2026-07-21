from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.plugin_special_attribute_manifest_type import (
    PluginSpecialAttributeManifestType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PluginSpecialAttributeManifest")


@_attrs_define
class PluginSpecialAttributeManifest:
    """
    Attributes:
        name (str):
        type_ (PluginSpecialAttributeManifestType):
        required (bool | Unset):  Default: False.
        default (Any | None | Unset):
        enum (list[str] | Unset):
        min_ (float | int | None | Unset):
        max_ (float | int | None | Unset):
        description (str | Unset):  Default: ''.
    """

    name: str
    type_: PluginSpecialAttributeManifestType
    required: bool | Unset = False
    default: Any | None | Unset = UNSET
    enum: list[str] | Unset = UNSET
    min_: float | int | None | Unset = UNSET
    max_: float | int | None | Unset = UNSET
    description: str | Unset = ""

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_.value

        required = self.required

        default: Any | None | Unset
        if isinstance(self.default, Unset):
            default = UNSET
        else:
            default = self.default

        enum: list[str] | Unset = UNSET
        if not isinstance(self.enum, Unset):
            enum = self.enum

        min_: float | int | None | Unset
        if isinstance(self.min_, Unset):
            min_ = UNSET
        else:
            min_ = self.min_

        max_: float | int | None | Unset
        if isinstance(self.max_, Unset):
            max_ = UNSET
        else:
            max_ = self.max_

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "type": type_,
            }
        )
        if required is not UNSET:
            field_dict["required"] = required
        if default is not UNSET:
            field_dict["default"] = default
        if enum is not UNSET:
            field_dict["enum"] = enum
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = PluginSpecialAttributeManifestType(d.pop("type"))

        required = d.pop("required", UNSET)

        def _parse_default(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        default = _parse_default(d.pop("default", UNSET))

        enum = cast(list[str], d.pop("enum", UNSET))

        def _parse_min_(data: object) -> float | int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | int | None | Unset, data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_max_(data: object) -> float | int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | int | None | Unset, data)

        max_ = _parse_max_(d.pop("max", UNSET))

        description = d.pop("description", UNSET)

        plugin_special_attribute_manifest = cls(
            name=name,
            type_=type_,
            required=required,
            default=default,
            enum=enum,
            min_=min_,
            max_=max_,
            description=description,
        )

        return plugin_special_attribute_manifest
