from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.docker_runtime import DockerRuntime
    from ..models.external_tool_runtime import ExternalToolRuntime
    from ..models.uv_runtime import UvRuntime


T = TypeVar("T", bound="RuntimeModes")


@_attrs_define
class RuntimeModes:
    """
    Attributes:
        uv (None | Unset | UvRuntime):
        docker (DockerRuntime | None | Unset):
        external_tool (ExternalToolRuntime | None | Unset):
    """

    uv: None | Unset | UvRuntime = UNSET
    docker: DockerRuntime | None | Unset = UNSET
    external_tool: ExternalToolRuntime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.docker_runtime import DockerRuntime
        from ..models.external_tool_runtime import ExternalToolRuntime
        from ..models.uv_runtime import UvRuntime

        uv: dict[str, Any] | None | Unset
        if isinstance(self.uv, Unset):
            uv = UNSET
        elif isinstance(self.uv, UvRuntime):
            uv = self.uv.to_dict()
        else:
            uv = self.uv

        docker: dict[str, Any] | None | Unset
        if isinstance(self.docker, Unset):
            docker = UNSET
        elif isinstance(self.docker, DockerRuntime):
            docker = self.docker.to_dict()
        else:
            docker = self.docker

        external_tool: dict[str, Any] | None | Unset
        if isinstance(self.external_tool, Unset):
            external_tool = UNSET
        elif isinstance(self.external_tool, ExternalToolRuntime):
            external_tool = self.external_tool.to_dict()
        else:
            external_tool = self.external_tool

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if uv is not UNSET:
            field_dict["uv"] = uv
        if docker is not UNSET:
            field_dict["docker"] = docker
        if external_tool is not UNSET:
            field_dict["external_tool"] = external_tool

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.docker_runtime import DockerRuntime
        from ..models.external_tool_runtime import ExternalToolRuntime
        from ..models.uv_runtime import UvRuntime

        d = dict(src_dict)

        def _parse_uv(data: object) -> None | Unset | UvRuntime:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                uv_type_0 = UvRuntime.from_dict(data)

                return uv_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UvRuntime, data)

        uv = _parse_uv(d.pop("uv", UNSET))

        def _parse_docker(data: object) -> DockerRuntime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                docker_type_0 = DockerRuntime.from_dict(data)

                return docker_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DockerRuntime | None | Unset, data)

        docker = _parse_docker(d.pop("docker", UNSET))

        def _parse_external_tool(data: object) -> ExternalToolRuntime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                external_tool_type_0 = ExternalToolRuntime.from_dict(data)

                return external_tool_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExternalToolRuntime | None | Unset, data)

        external_tool = _parse_external_tool(d.pop("external_tool", UNSET))

        runtime_modes = cls(
            uv=uv,
            docker=docker,
            external_tool=external_tool,
        )

        return runtime_modes
