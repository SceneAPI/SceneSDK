from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DockerRuntime")


@_attrs_define
class DockerRuntime:
    """
    Attributes:
        image (None | str | Unset):
        build_context (None | str | Unset):
    """

    image: None | str | Unset = UNSET
    build_context: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        image: None | str | Unset
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        build_context: None | str | Unset
        if isinstance(self.build_context, Unset):
            build_context = UNSET
        else:
            build_context = self.build_context

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if image is not UNSET:
            field_dict["image"] = image
        if build_context is not UNSET:
            field_dict["build_context"] = build_context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_build_context(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        build_context = _parse_build_context(d.pop("build_context", UNSET))

        docker_runtime = cls(
            image=image,
            build_context=build_context,
        )

        return docker_runtime
