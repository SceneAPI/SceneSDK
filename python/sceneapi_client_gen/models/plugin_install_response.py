from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.plugin_install_response_method import PluginInstallResponseMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_provisioning_out import PluginProvisioningOut


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
        provision_runtime (bool | Unset):  Default: False.
        provisioned (bool | Unset):  Default: False.
        provisioning_status (str | Unset):  Default: 'not_requested'.
        provisioning_error (None | str | Unset):
        request_id (None | str | Unset):
        provisioning (None | PluginProvisioningOut | Unset):
    """

    plugin_id: str
    method: PluginInstallResponseMethod
    dry_run: bool
    installed: bool
    command: list[str] | Unset = UNSET
    direct_reference: None | str | Unset = UNSET
    warnings: list[str] | Unset = UNSET
    resolved_commit: None | str | Unset = UNSET
    provision_runtime: bool | Unset = False
    provisioned: bool | Unset = False
    provisioning_status: str | Unset = "not_requested"
    provisioning_error: None | str | Unset = UNSET
    request_id: None | str | Unset = UNSET
    provisioning: None | PluginProvisioningOut | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.plugin_provisioning_out import PluginProvisioningOut

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

        provision_runtime = self.provision_runtime

        provisioned = self.provisioned

        provisioning_status = self.provisioning_status

        provisioning_error: None | str | Unset
        if isinstance(self.provisioning_error, Unset):
            provisioning_error = UNSET
        else:
            provisioning_error = self.provisioning_error

        request_id: None | str | Unset
        if isinstance(self.request_id, Unset):
            request_id = UNSET
        else:
            request_id = self.request_id

        provisioning: dict[str, Any] | None | Unset
        if isinstance(self.provisioning, Unset):
            provisioning = UNSET
        elif isinstance(self.provisioning, PluginProvisioningOut):
            provisioning = self.provisioning.to_dict()
        else:
            provisioning = self.provisioning

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
        if provision_runtime is not UNSET:
            field_dict["provision_runtime"] = provision_runtime
        if provisioned is not UNSET:
            field_dict["provisioned"] = provisioned
        if provisioning_status is not UNSET:
            field_dict["provisioning_status"] = provisioning_status
        if provisioning_error is not UNSET:
            field_dict["provisioning_error"] = provisioning_error
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if provisioning is not UNSET:
            field_dict["provisioning"] = provisioning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_provisioning_out import PluginProvisioningOut

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

        provision_runtime = d.pop("provision_runtime", UNSET)

        provisioned = d.pop("provisioned", UNSET)

        provisioning_status = d.pop("provisioning_status", UNSET)

        def _parse_provisioning_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provisioning_error = _parse_provisioning_error(
            d.pop("provisioning_error", UNSET)
        )

        def _parse_request_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        def _parse_provisioning(data: object) -> None | PluginProvisioningOut | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                provisioning_type_0 = PluginProvisioningOut.from_dict(data)

                return provisioning_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PluginProvisioningOut | Unset, data)

        provisioning = _parse_provisioning(d.pop("provisioning", UNSET))

        plugin_install_response = cls(
            plugin_id=plugin_id,
            method=method,
            dry_run=dry_run,
            installed=installed,
            command=command,
            direct_reference=direct_reference,
            warnings=warnings,
            resolved_commit=resolved_commit,
            provision_runtime=provision_runtime,
            provisioned=provisioned,
            provisioning_status=provisioning_status,
            provisioning_error=provisioning_error,
            request_id=request_id,
            provisioning=provisioning,
        )

        return plugin_install_response
