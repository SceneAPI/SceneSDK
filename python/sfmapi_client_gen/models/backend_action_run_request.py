from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.backend_action_run_request_inputs import BackendActionRunRequestInputs


T = TypeVar("T", bound="BackendActionRunRequest")


@_attrs_define
class BackendActionRunRequest:
    """Submit a backend-native action as an sfmapi job.

    Attributes:
        project_id (str):
        provider (None | str | Unset):
        inputs (BackendActionRunRequestInputs | Unset):
    """

    project_id: str
    provider: None | str | Unset = UNSET
    inputs: BackendActionRunRequestInputs | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        inputs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.inputs, Unset):
            inputs = self.inputs.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "project_id": project_id,
            }
        )
        if provider is not UNSET:
            field_dict["provider"] = provider
        if inputs is not UNSET:
            field_dict["inputs"] = inputs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.backend_action_run_request_inputs import (
            BackendActionRunRequestInputs,
        )

        d = dict(src_dict)
        project_id = d.pop("project_id")

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        _inputs = d.pop("inputs", UNSET)
        inputs: BackendActionRunRequestInputs | Unset
        if isinstance(_inputs, Unset):
            inputs = UNSET
        else:
            inputs = BackendActionRunRequestInputs.from_dict(_inputs)

        backend_action_run_request = cls(
            project_id=project_id,
            provider=provider,
            inputs=inputs,
        )

        return backend_action_run_request
