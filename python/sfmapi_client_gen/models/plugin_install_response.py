from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.plugin_install_response_method import PluginInstallResponseMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="PluginInstallResponse")


@_attrs_define
class PluginInstallResponse:
    """
    Attributes:
        plugin_id (str):
        method (PluginInstallResponseMethod):
        dry_run (bool):
        installed (bool):
        command (list[str] | Unset):
        direct_reference (None | str | Unset):
        warnings (list[str] | Unset):
        resolved_commit (None | str | Unset):
    """

    plugin_id: str
    method: PluginInstallResponseMethod
    dry_run: bool
    installed: bool
    command: list[str] | Unset = UNSET
    direct_reference: None | str | Unset = UNSET
    warnings: list[str] | Unset = UNSET
    resolved_commit: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        plugin_id = self.plugin_id

        method = self.method.value

        dry_run = self.dry_run

        installed = self.installed

        command: list[str] | Unset = UNSET
        if not isinstance(self.command, Unset):
            command = self.command

        direct_reference: None | str | Unset
        if isinstance(self.direct_reference, Unset):
            direct_reference = UNSET
        else:
            direct_reference = self.direct_reference

        warnings: list[str] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        resolved_commit: None | str | Unset
        if isinstance(self.resolved_commit, Unset):
            resolved_commit = UNSET
        else:
            resolved_commit = self.resolved_commit

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "plugin_id": plugin_id,
                "method": method,
                "dry_run": dry_run,
                "installed": installed,
            }
        )
        if command is not UNSET:
            field_dict["command"] = command
        if direct_reference is not UNSET:
            field_dict["direct_reference"] = direct_reference
        if warnings is not UNSET:
            field_dict["warnings"] = warnings
        if resolved_commit is not UNSET:
            field_dict["resolved_commit"] = resolved_commit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plugin_id = d.pop("plugin_id")

        method = PluginInstallResponseMethod(d.pop("method"))

        dry_run = d.pop("dry_run")

        installed = d.pop("installed")

        command = cast(list[str], d.pop("command", UNSET))

        def _parse_direct_reference(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        direct_reference = _parse_direct_reference(d.pop("direct_reference", UNSET))

        warnings = cast(list[str], d.pop("warnings", UNSET))

        def _parse_resolved_commit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        resolved_commit = _parse_resolved_commit(d.pop("resolved_commit", UNSET))

        plugin_install_response = cls(
            plugin_id=plugin_id,
            method=method,
            dry_run=dry_run,
            installed=installed,
            command=command,
            direct_reference=direct_reference,
            warnings=warnings,
            resolved_commit=resolved_commit,
        )

        return plugin_install_response
