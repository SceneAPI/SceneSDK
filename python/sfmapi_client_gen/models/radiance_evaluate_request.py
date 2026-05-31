from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.radiance_eval_config import RadianceEvalConfig
    from ..models.radiance_evaluate_request_backend_options import (
        RadianceEvaluateRequestBackendOptions,
    )


T = TypeVar("T", bound="RadianceEvaluateRequest")


@_attrs_define
class RadianceEvaluateRequest:
    """Request body for ``POST /v1/radiance_fields/{id}:evaluate``.

    Attributes:
        snapshot_seq (int | None | Unset):
        dataset_id (None | str | Unset):
        provider (None | str | Unset):
        method (None | str | Unset):
        eval_ (RadianceEvalConfig | Unset): Portable evaluation settings for splat providers.

            Provider-specific eval knobs stay in ``backend_options``; this shape
            captures the stable cross-provider contract exposed through the SDK.
        backend_options (RadianceEvaluateRequestBackendOptions | Unset):
        request_id (None | str | Unset):
    """

    snapshot_seq: int | None | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    provider: None | str | Unset = UNSET
    method: None | str | Unset = UNSET
    eval_: RadianceEvalConfig | Unset = UNSET
    backend_options: RadianceEvaluateRequestBackendOptions | Unset = UNSET
    request_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        snapshot_seq: int | None | Unset
        if isinstance(self.snapshot_seq, Unset):
            snapshot_seq = UNSET
        else:
            snapshot_seq = self.snapshot_seq

        dataset_id: None | str | Unset
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        method: None | str | Unset
        if isinstance(self.method, Unset):
            method = UNSET
        else:
            method = self.method

        eval_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.eval_, Unset):
            eval_ = self.eval_.to_dict()

        backend_options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.backend_options, Unset):
            backend_options = self.backend_options.to_dict()

        request_id: None | str | Unset
        if isinstance(self.request_id, Unset):
            request_id = UNSET
        else:
            request_id = self.request_id

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if snapshot_seq is not UNSET:
            field_dict["snapshot_seq"] = snapshot_seq
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if provider is not UNSET:
            field_dict["provider"] = provider
        if method is not UNSET:
            field_dict["method"] = method
        if eval_ is not UNSET:
            field_dict["eval"] = eval_
        if backend_options is not UNSET:
            field_dict["backend_options"] = backend_options
        if request_id is not UNSET:
            field_dict["request_id"] = request_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.radiance_eval_config import RadianceEvalConfig
        from ..models.radiance_evaluate_request_backend_options import (
            RadianceEvaluateRequestBackendOptions,
        )

        d = dict(src_dict)

        def _parse_snapshot_seq(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        snapshot_seq = _parse_snapshot_seq(d.pop("snapshot_seq", UNSET))

        def _parse_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        def _parse_method(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        method = _parse_method(d.pop("method", UNSET))

        _eval_ = d.pop("eval", UNSET)
        eval_: RadianceEvalConfig | Unset
        if isinstance(_eval_, Unset):
            eval_ = UNSET
        else:
            eval_ = RadianceEvalConfig.from_dict(_eval_)

        _backend_options = d.pop("backend_options", UNSET)
        backend_options: RadianceEvaluateRequestBackendOptions | Unset
        if isinstance(_backend_options, Unset):
            backend_options = UNSET
        else:
            backend_options = RadianceEvaluateRequestBackendOptions.from_dict(
                _backend_options
            )

        def _parse_request_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        radiance_evaluate_request = cls(
            snapshot_seq=snapshot_seq,
            dataset_id=dataset_id,
            provider=provider,
            method=method,
            eval_=eval_,
            backend_options=backend_options,
            request_id=request_id,
        )

        return radiance_evaluate_request
