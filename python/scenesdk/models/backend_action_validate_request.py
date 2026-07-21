from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.backend_action_validate_request_inputs import (
        BackendActionValidateRequestInputs,
    )


T = TypeVar("T", bound="BackendActionValidateRequest")


@_attrs_define
class BackendActionValidateRequest:
    """Validate action input without submitting work.

    Attributes:
        project_id (None | str | Unset):
        provider (None | str | Unset):
        inputs (BackendActionValidateRequestInputs | Unset):
    """

    project_id: None | str | Unset = UNSET
    provider: None | str | Unset = UNSET
    inputs: BackendActionValidateRequestInputs | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
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

        field_dict.update({})
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if provider is not UNSET:
            field_dict["provider"] = provider
        if inputs is not UNSET:
            field_dict["inputs"] = inputs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.backend_action_validate_request_inputs import (
            BackendActionValidateRequestInputs,
        )

        d = dict(src_dict)

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        _inputs = d.pop("inputs", UNSET)
        inputs: BackendActionValidateRequestInputs | Unset
        if isinstance(_inputs, Unset):
            inputs = UNSET
        else:
            inputs = BackendActionValidateRequestInputs.from_dict(_inputs)

        backend_action_validate_request = cls(
            project_id=project_id,
            provider=provider,
            inputs=inputs,
        )

        return backend_action_validate_request
