from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerServiceObjectStore")


@_attrs_define
class ContainerServiceObjectStore:
    """
    Attributes:
        url_env (None | str | Unset):
        input_prefix (None | str | Unset):
        output_prefix (None | str | Unset):
    """

    url_env: None | str | Unset = UNSET
    input_prefix: None | str | Unset = UNSET
    output_prefix: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        url_env: None | str | Unset
        if isinstance(self.url_env, Unset):
            url_env = UNSET
        else:
            url_env = self.url_env

        input_prefix: None | str | Unset
        if isinstance(self.input_prefix, Unset):
            input_prefix = UNSET
        else:
            input_prefix = self.input_prefix

        output_prefix: None | str | Unset
        if isinstance(self.output_prefix, Unset):
            output_prefix = UNSET
        else:
            output_prefix = self.output_prefix

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if url_env is not UNSET:
            field_dict["url_env"] = url_env
        if input_prefix is not UNSET:
            field_dict["input_prefix"] = input_prefix
        if output_prefix is not UNSET:
            field_dict["output_prefix"] = output_prefix

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_url_env(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url_env = _parse_url_env(d.pop("url_env", UNSET))

        def _parse_input_prefix(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        input_prefix = _parse_input_prefix(d.pop("input_prefix", UNSET))

        def _parse_output_prefix(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_prefix = _parse_output_prefix(d.pop("output_prefix", UNSET))

        container_service_object_store = cls(
            url_env=url_env,
            input_prefix=input_prefix,
            output_prefix=output_prefix,
        )

        return container_service_object_store
