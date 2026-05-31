from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.plugin_install_request_method import PluginInstallRequestMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="PluginInstallRequest")


@_attrs_define
class PluginInstallRequest:
    """
    Attributes:
        method (PluginInstallRequestMethod | Unset):  Default: PluginInstallRequestMethod.UV.
        github_url (None | str | Unset):
        ref (None | str | Unset):
        package_name (None | str | Unset):
        dry_run (bool | Unset):  Default: True.
        allow_unsafe_execution (bool | Unset):  Default: False.
        request_id (None | str | Unset):
        provision_runtime (bool | Unset):  Default: True.
        force (bool | Unset):  Default: False.
    """

    method: PluginInstallRequestMethod | Unset = PluginInstallRequestMethod.UV
    github_url: None | str | Unset = UNSET
    ref: None | str | Unset = UNSET
    package_name: None | str | Unset = UNSET
    dry_run: bool | Unset = True
    allow_unsafe_execution: bool | Unset = False
    request_id: None | str | Unset = UNSET
    provision_runtime: bool | Unset = True
    force: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        method: str | Unset = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        github_url: None | str | Unset
        if isinstance(self.github_url, Unset):
            github_url = UNSET
        else:
            github_url = self.github_url

        ref: None | str | Unset
        if isinstance(self.ref, Unset):
            ref = UNSET
        else:
            ref = self.ref

        package_name: None | str | Unset
        if isinstance(self.package_name, Unset):
            package_name = UNSET
        else:
            package_name = self.package_name

        dry_run = self.dry_run

        allow_unsafe_execution = self.allow_unsafe_execution

        request_id: None | str | Unset
        if isinstance(self.request_id, Unset):
            request_id = UNSET
        else:
            request_id = self.request_id

        provision_runtime = self.provision_runtime

        force = self.force

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if method is not UNSET:
            field_dict["method"] = method
        if github_url is not UNSET:
            field_dict["github_url"] = github_url
        if ref is not UNSET:
            field_dict["ref"] = ref
        if package_name is not UNSET:
            field_dict["package_name"] = package_name
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if allow_unsafe_execution is not UNSET:
            field_dict["allow_unsafe_execution"] = allow_unsafe_execution
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if provision_runtime is not UNSET:
            field_dict["provision_runtime"] = provision_runtime
        if force is not UNSET:
            field_dict["force"] = force

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _method = d.pop("method", UNSET)
        method: PluginInstallRequestMethod | Unset
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = PluginInstallRequestMethod(_method)

        def _parse_github_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        github_url = _parse_github_url(d.pop("github_url", UNSET))

        def _parse_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ref = _parse_ref(d.pop("ref", UNSET))

        def _parse_package_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        package_name = _parse_package_name(d.pop("package_name", UNSET))

        dry_run = d.pop("dry_run", UNSET)

        allow_unsafe_execution = d.pop("allow_unsafe_execution", UNSET)

        def _parse_request_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        provision_runtime = d.pop("provision_runtime", UNSET)

        force = d.pop("force", UNSET)

        plugin_install_request = cls(
            method=method,
            github_url=github_url,
            ref=ref,
            package_name=package_name,
            dry_run=dry_run,
            allow_unsafe_execution=allow_unsafe_execution,
            request_id=request_id,
            provision_runtime=provision_runtime,
            force=force,
        )

        return plugin_install_request
