from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pipeline_step_params import PipelineStepParams


T = TypeVar("T", bound="PipelineStep")


@_attrs_define
class PipelineStep:
    """Compatibility schema name for the legacy operation-list step.

    Attributes:
        op (str):
        provider (None | str | Unset):
        params (PipelineStepParams | Unset):
    """

    op: str
    provider: None | str | Unset = UNSET
    params: PipelineStepParams | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        op = self.op

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict() if hasattr(self.params, "to_dict") else dict(self.params)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "op": op,
            }
        )
        if provider is not UNSET:
            field_dict["provider"] = provider
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pipeline_step_params import PipelineStepParams

        d = dict(src_dict)
        op = d.pop("op")

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        _params = d.pop("params", UNSET)
        params: PipelineStepParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = PipelineStepParams.from_dict(_params)

        pipeline_step = cls(
            op=op,
            provider=provider,
            params=params,
        )

        return pipeline_step
