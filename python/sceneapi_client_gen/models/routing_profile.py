from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.routing_profile_routes import RoutingProfileRoutes


T = TypeVar("T", bound="RoutingProfile")


@_attrs_define
class RoutingProfile:
    """
    Attributes:
        name (str):
        routes (RoutingProfileRoutes | Unset):
    """

    name: str
    routes: RoutingProfileRoutes | Unset = UNSET

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
        from ..models.routing_profile_routes import RoutingProfileRoutes

        d = dict(src_dict)
        name = d.pop("name")

        _routes = d.pop("routes", UNSET)
        routes: RoutingProfileRoutes | Unset
        if isinstance(_routes, Unset):
            routes = UNSET
        else:
            routes = RoutingProfileRoutes.from_dict(_routes)

        routing_profile = cls(
            name=name,
            routes=routes,
        )

        return routing_profile
