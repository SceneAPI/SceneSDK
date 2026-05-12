from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compatibility_tool_versions import CompatibilityToolVersions


T = TypeVar("T", bound="Compatibility")


@_attrs_define
class Compatibility:
    """
    Attributes:
        sfmapi (str | Unset):  Default: '>=0.0.1'.
        python (None | str | Unset):  Default: '>=3.12,<3.13'.
        os (list[str] | Unset):
        cuda (None | str | Unset):
        tool_versions (CompatibilityToolVersions | Unset):
    """

    sfmapi: str | Unset = ">=0.0.1"
    python: None | str | Unset = ">=3.12,<3.13"
    os: list[str] | Unset = UNSET
    cuda: None | str | Unset = UNSET
    tool_versions: CompatibilityToolVersions | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sfmapi = self.sfmapi

        python: None | str | Unset
        if isinstance(self.python, Unset):
            python = UNSET
        else:
            python = self.python

        os: list[str] | Unset = UNSET
        if not isinstance(self.os, Unset):
            os = self.os

        cuda: None | str | Unset
        if isinstance(self.cuda, Unset):
            cuda = UNSET
        else:
            cuda = self.cuda

        tool_versions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tool_versions, Unset):
            tool_versions = self.tool_versions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sfmapi is not UNSET:
            field_dict["sfmapi"] = sfmapi
        if python is not UNSET:
            field_dict["python"] = python
        if os is not UNSET:
            field_dict["os"] = os
        if cuda is not UNSET:
            field_dict["cuda"] = cuda
        if tool_versions is not UNSET:
            field_dict["tool_versions"] = tool_versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compatibility_tool_versions import CompatibilityToolVersions

        d = dict(src_dict)
        sfmapi = d.pop("sfmapi", UNSET)

        def _parse_python(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        python = _parse_python(d.pop("python", UNSET))

        os = cast(list[str], d.pop("os", UNSET))

        def _parse_cuda(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cuda = _parse_cuda(d.pop("cuda", UNSET))

        _tool_versions = d.pop("tool_versions", UNSET)
        tool_versions: CompatibilityToolVersions | Unset
        if isinstance(_tool_versions, Unset):
            tool_versions = UNSET
        else:
            tool_versions = CompatibilityToolVersions.from_dict(_tool_versions)

        compatibility = cls(
            sfmapi=sfmapi,
            python=python,
            os=os,
            cuda=cuda,
            tool_versions=tool_versions,
        )

        compatibility.additional_properties = d
        return compatibility

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
