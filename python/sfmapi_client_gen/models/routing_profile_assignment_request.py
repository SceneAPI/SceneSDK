from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RoutingProfileAssignmentRequest")


@_attrs_define
class RoutingProfileAssignmentRequest:
    """
    Attributes:
        profile (str):
    """

    profile: str

    def to_dict(self) -> dict[str, Any]:
        profile = self.profile

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "profile": profile,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        profile = d.pop("profile")

        routing_profile_assignment_request = cls(
            profile=profile,
        )

        return routing_profile_assignment_request
