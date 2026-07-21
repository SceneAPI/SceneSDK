from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.routing_out_profiles import RoutingOutProfiles
    from ..models.routing_out_project_profiles import RoutingOutProjectProfiles
    from ..models.routing_out_workspace_profiles import RoutingOutWorkspaceProfiles


T = TypeVar("T", bound="RoutingOut")


@_attrs_define
class RoutingOut:
    """
    Attributes:
        default_profile (None | str | Unset):
        provider_priority (list[str] | Unset):
        profiles (RoutingOutProfiles | Unset):
        project_profiles (RoutingOutProjectProfiles | Unset):
        workspace_profiles (RoutingOutWorkspaceProfiles | Unset):
    """

    default_profile: None | str | Unset = UNSET
    provider_priority: list[str] | Unset = UNSET
    profiles: RoutingOutProfiles | Unset = UNSET
    project_profiles: RoutingOutProjectProfiles | Unset = UNSET
    workspace_profiles: RoutingOutWorkspaceProfiles | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        default_profile: None | str | Unset
        if isinstance(self.default_profile, Unset):
            default_profile = UNSET
        else:
            default_profile = self.default_profile

        provider_priority: list[str] | Unset = UNSET
        if not isinstance(self.provider_priority, Unset):
            provider_priority = self.provider_priority

        profiles: dict[str, Any] | Unset = UNSET
        if not isinstance(self.profiles, Unset):
            profiles = self.profiles.to_dict()

        project_profiles: dict[str, Any] | Unset = UNSET
        if not isinstance(self.project_profiles, Unset):
            project_profiles = self.project_profiles.to_dict()

        workspace_profiles: dict[str, Any] | Unset = UNSET
        if not isinstance(self.workspace_profiles, Unset):
            workspace_profiles = self.workspace_profiles.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if default_profile is not UNSET:
            field_dict["default_profile"] = default_profile
        if provider_priority is not UNSET:
            field_dict["provider_priority"] = provider_priority
        if profiles is not UNSET:
            field_dict["profiles"] = profiles
        if project_profiles is not UNSET:
            field_dict["project_profiles"] = project_profiles
        if workspace_profiles is not UNSET:
            field_dict["workspace_profiles"] = workspace_profiles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.routing_out_profiles import RoutingOutProfiles
        from ..models.routing_out_project_profiles import RoutingOutProjectProfiles
        from ..models.routing_out_workspace_profiles import RoutingOutWorkspaceProfiles

        d = dict(src_dict)

        def _parse_default_profile(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_profile = _parse_default_profile(d.pop("default_profile", UNSET))

        provider_priority = cast(list[str], d.pop("provider_priority", UNSET))

        _profiles = d.pop("profiles", UNSET)
        profiles: RoutingOutProfiles | Unset
        if isinstance(_profiles, Unset):
            profiles = UNSET
        else:
            profiles = RoutingOutProfiles.from_dict(_profiles)

        _project_profiles = d.pop("project_profiles", UNSET)
        project_profiles: RoutingOutProjectProfiles | Unset
        if isinstance(_project_profiles, Unset):
            project_profiles = UNSET
        else:
            project_profiles = RoutingOutProjectProfiles.from_dict(_project_profiles)

        _workspace_profiles = d.pop("workspace_profiles", UNSET)
        workspace_profiles: RoutingOutWorkspaceProfiles | Unset
        if isinstance(_workspace_profiles, Unset):
            workspace_profiles = UNSET
        else:
            workspace_profiles = RoutingOutWorkspaceProfiles.from_dict(
                _workspace_profiles
            )

        routing_out = cls(
            default_profile=default_profile,
            provider_priority=provider_priority,
            profiles=profiles,
            project_profiles=project_profiles,
            workspace_profiles=workspace_profiles,
        )

        return routing_out
