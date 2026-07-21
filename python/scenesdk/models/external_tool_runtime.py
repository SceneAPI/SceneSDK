from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalToolRuntime")


@_attrs_define
class ExternalToolRuntime:
    """
    Attributes:
        executable_names (list[str] | Unset):
        env_vars (list[str] | Unset):
        version_args (list[str] | Unset):
    """

    executable_names: list[str] | Unset = UNSET
    env_vars: list[str] | Unset = UNSET
    version_args: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        executable_names: list[str] | Unset = UNSET
        if not isinstance(self.executable_names, Unset):
            executable_names = self.executable_names

        env_vars: list[str] | Unset = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = self.env_vars

        version_args: list[str] | Unset = UNSET
        if not isinstance(self.version_args, Unset):
            version_args = self.version_args

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if executable_names is not UNSET:
            field_dict["executable_names"] = executable_names
        if env_vars is not UNSET:
            field_dict["env_vars"] = env_vars
        if version_args is not UNSET:
            field_dict["version_args"] = version_args

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        executable_names = cast(list[str], d.pop("executable_names", UNSET))

        env_vars = cast(list[str], d.pop("env_vars", UNSET))

        version_args = cast(list[str], d.pop("version_args", UNSET))

        external_tool_runtime = cls(
            executable_names=executable_names,
            env_vars=env_vars,
            version_args=version_args,
        )

        return external_tool_runtime
