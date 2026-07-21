from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerServiceEndpoint")


@_attrs_define
class ContainerServiceEndpoint:
    """
    Attributes:
        default_url (None | str | Unset):
        url_env (None | str | Unset):
    """

    default_url: None | str | Unset = UNSET
    url_env: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        default_url: None | str | Unset
        if isinstance(self.default_url, Unset):
            default_url = UNSET
        else:
            default_url = self.default_url

        url_env: None | str | Unset
        if isinstance(self.url_env, Unset):
            url_env = UNSET
        else:
            url_env = self.url_env

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if default_url is not UNSET:
            field_dict["default_url"] = default_url
        if url_env is not UNSET:
            field_dict["url_env"] = url_env

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_default_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_url = _parse_default_url(d.pop("default_url", UNSET))

        def _parse_url_env(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url_env = _parse_url_env(d.pop("url_env", UNSET))

        container_service_endpoint = cls(
            default_url=default_url,
            url_env=url_env,
        )

        return container_service_endpoint
