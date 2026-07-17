from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.container_service_build_source import ContainerServiceBuildSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.container_service_build_args import ContainerServiceBuildArgs


T = TypeVar("T", bound="ContainerServiceBuild")


@_attrs_define
class ContainerServiceBuild:
    """
    Attributes:
        source (ContainerServiceBuildSource | Unset):  Default: ContainerServiceBuildSource.GIT.
        context (None | str | Unset):
        dockerfile (str | Unset):  Default: 'Dockerfile'.
        ref (None | str | Unset):
        args (ContainerServiceBuildArgs | Unset):
    """

    source: ContainerServiceBuildSource | Unset = ContainerServiceBuildSource.GIT
    context: None | str | Unset = UNSET
    dockerfile: str | Unset = "Dockerfile"
    ref: None | str | Unset = UNSET
    args: ContainerServiceBuildArgs | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        source: str | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        context: None | str | Unset
        if isinstance(self.context, Unset):
            context = UNSET
        else:
            context = self.context

        dockerfile = self.dockerfile

        ref: None | str | Unset
        if isinstance(self.ref, Unset):
            ref = UNSET
        else:
            ref = self.ref

        args: dict[str, Any] | Unset = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if context is not UNSET:
            field_dict["context"] = context
        if dockerfile is not UNSET:
            field_dict["dockerfile"] = dockerfile
        if ref is not UNSET:
            field_dict["ref"] = ref
        if args is not UNSET:
            field_dict["args"] = args

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_service_build_args import ContainerServiceBuildArgs

        d = dict(src_dict)
        _source = d.pop("source", UNSET)
        source: ContainerServiceBuildSource | Unset
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = ContainerServiceBuildSource(_source)

        def _parse_context(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        context = _parse_context(d.pop("context", UNSET))

        dockerfile = d.pop("dockerfile", UNSET)

        def _parse_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ref = _parse_ref(d.pop("ref", UNSET))

        _args = d.pop("args", UNSET)
        args: ContainerServiceBuildArgs | Unset
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = ContainerServiceBuildArgs.from_dict(_args)

        container_service_build = cls(
            source=source,
            context=context,
            dockerfile=dockerfile,
            ref=ref,
            args=args,
        )

        return container_service_build
