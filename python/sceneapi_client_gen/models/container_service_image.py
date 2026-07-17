from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.container_service_build import ContainerServiceBuild


T = TypeVar("T", bound="ContainerServiceImage")


@_attrs_define
class ContainerServiceImage:
    """
    Attributes:
        image (None | str | Unset):
        digest (None | str | Unset):
        registry (None | str | Unset):
        build (ContainerServiceBuild | None | Unset):
    """

    image: None | str | Unset = UNSET
    digest: None | str | Unset = UNSET
    registry: None | str | Unset = UNSET
    build: ContainerServiceBuild | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.container_service_build import ContainerServiceBuild

        image: None | str | Unset
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        digest: None | str | Unset
        if isinstance(self.digest, Unset):
            digest = UNSET
        else:
            digest = self.digest

        registry: None | str | Unset
        if isinstance(self.registry, Unset):
            registry = UNSET
        else:
            registry = self.registry

        build: dict[str, Any] | None | Unset
        if isinstance(self.build, Unset):
            build = UNSET
        elif isinstance(self.build, ContainerServiceBuild):
            build = self.build.to_dict()
        else:
            build = self.build

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if image is not UNSET:
            field_dict["image"] = image
        if digest is not UNSET:
            field_dict["digest"] = digest
        if registry is not UNSET:
            field_dict["registry"] = registry
        if build is not UNSET:
            field_dict["build"] = build

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_service_build import ContainerServiceBuild

        d = dict(src_dict)

        def _parse_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_digest(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        digest = _parse_digest(d.pop("digest", UNSET))

        def _parse_registry(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        registry = _parse_registry(d.pop("registry", UNSET))

        def _parse_build(data: object) -> ContainerServiceBuild | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                build_type_0 = ContainerServiceBuild.from_dict(data)

                return build_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ContainerServiceBuild | None | Unset, data)

        build = _parse_build(d.pop("build", UNSET))

        container_service_image = cls(
            image=image,
            digest=digest,
            registry=registry,
            build=build,
        )

        return container_service_image
