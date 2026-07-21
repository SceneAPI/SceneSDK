from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.container_service_cache_policy import ContainerServiceCachePolicy
from ..models.container_service_cache_scope import ContainerServiceCacheScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerServiceCache")


@_attrs_define
class ContainerServiceCache:
    """
    Attributes:
        policy (ContainerServiceCachePolicy | Unset):  Default: ContainerServiceCachePolicy.NONE.
        scope (ContainerServiceCacheScope | Unset):  Default: ContainerServiceCacheScope.REQUEST.
        path (None | str | Unset):
    """

    policy: ContainerServiceCachePolicy | Unset = ContainerServiceCachePolicy.NONE
    scope: ContainerServiceCacheScope | Unset = ContainerServiceCacheScope.REQUEST
    path: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        policy: str | Unset = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.value

        scope: str | Unset = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.value

        path: None | str | Unset
        if isinstance(self.path, Unset):
            path = UNSET
        else:
            path = self.path

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if policy is not UNSET:
            field_dict["policy"] = policy
        if scope is not UNSET:
            field_dict["scope"] = scope
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _policy = d.pop("policy", UNSET)
        policy: ContainerServiceCachePolicy | Unset
        if isinstance(_policy, Unset):
            policy = UNSET
        else:
            policy = ContainerServiceCachePolicy(_policy)

        _scope = d.pop("scope", UNSET)
        scope: ContainerServiceCacheScope | Unset
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = ContainerServiceCacheScope(_scope)

        def _parse_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        path = _parse_path(d.pop("path", UNSET))

        container_service_cache = cls(
            policy=policy,
            scope=scope,
            path=path,
        )

        return container_service_cache
