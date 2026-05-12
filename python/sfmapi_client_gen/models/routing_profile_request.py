from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.routing_profile_request_routes import RoutingProfileRequestRoutes


T = TypeVar("T", bound="RoutingProfileRequest")


@_attrs_define
class RoutingProfileRequest:
    """
    Attributes:
        name (str):
        routes (RoutingProfileRequestRoutes | Unset):
    """

    name: str
    routes: RoutingProfileRequestRoutes | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        routes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.routes, Unset):
            routes = self.routes.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )
        if routes is not UNSET:
            field_dict["routes"] = routes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.routing_profile_request_routes import RoutingProfileRequestRoutes

        d = dict(src_dict)
        name = d.pop("name")

        _routes = d.pop("routes", UNSET)
        routes: RoutingProfileRequestRoutes | Unset
        if isinstance(_routes, Unset):
            routes = UNSET
        else:
            routes = RoutingProfileRequestRoutes.from_dict(_routes)

        routing_profile_request = cls(
            name=name,
            routes=routes,
        )

        return routing_profile_request
