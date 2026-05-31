from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.radiance_eval_config import RadianceEvalConfig
    from ..models.radiance_train_request_backend_options import (
        RadianceTrainRequestBackendOptions,
    )


T = TypeVar("T", bound="RadianceTrainRequest")


@_attrs_define
class RadianceTrainRequest:
    """Request body for ``POST /v1/projects/{project_id}/radiance_fields:train``.

    The alpha core implementation supports a deterministic ``stub`` provider
    for parity tests. Real training providers belong in plugins and should
    preserve provider-specific knobs inside ``backend_options``.

        Attributes:
            name (None | str | Unset):
            dataset_id (None | str | Unset):
            recon_id (None | str | Unset):
            provider (str | Unset):  Default: 'stub'.
            method (str | Unset):  Default: 'stub'.
            max_steps (int | Unset):  Default: 1.
            eval_ (None | RadianceEvalConfig | Unset):
            backend_options (RadianceTrainRequestBackendOptions | Unset):
            request_id (None | str | Unset): Client retry token. Reserved for idempotent radiance submissions.
    """

    name: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    recon_id: None | str | Unset = UNSET
    provider: str | Unset = "stub"
    method: str | Unset = "stub"
    max_steps: int | Unset = 1
    eval_: None | RadianceEvalConfig | Unset = UNSET
    backend_options: RadianceTrainRequestBackendOptions | Unset = UNSET
    request_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.radiance_eval_config import RadianceEvalConfig

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        dataset_id: None | str | Unset
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        recon_id: None | str | Unset
        if isinstance(self.recon_id, Unset):
            recon_id = UNSET
        else:
            recon_id = self.recon_id

        provider = self.provider

        method = self.method

        max_steps = self.max_steps

        eval_: dict[str, Any] | None | Unset
        if isinstance(self.eval_, Unset):
            eval_ = UNSET
        elif isinstance(self.eval_, RadianceEvalConfig):
            eval_ = self.eval_.to_dict()
        else:
            eval_ = self.eval_

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
        if name is not UNSET:
            field_dict["name"] = name
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if recon_id is not UNSET:
            field_dict["recon_id"] = recon_id
        if provider is not UNSET:
            field_dict["provider"] = provider
        if method is not UNSET:
            field_dict["method"] = method
        if max_steps is not UNSET:
            field_dict["max_steps"] = max_steps
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
        from ..models.radiance_train_request_backend_options import (
            RadianceTrainRequestBackendOptions,
        )

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_recon_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recon_id = _parse_recon_id(d.pop("recon_id", UNSET))

        provider = d.pop("provider", UNSET)

        method = d.pop("method", UNSET)

        max_steps = d.pop("max_steps", UNSET)

        def _parse_eval_(data: object) -> None | RadianceEvalConfig | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                eval_type_0 = RadianceEvalConfig.from_dict(data)

                return eval_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RadianceEvalConfig | Unset, data)

        eval_ = _parse_eval_(d.pop("eval", UNSET))

        _backend_options = d.pop("backend_options", UNSET)
        backend_options: RadianceTrainRequestBackendOptions | Unset
        if isinstance(_backend_options, Unset):
            backend_options = UNSET
        else:
            backend_options = RadianceTrainRequestBackendOptions.from_dict(
                _backend_options
            )

        def _parse_request_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        radiance_train_request = cls(
            name=name,
            dataset_id=dataset_id,
            recon_id=recon_id,
            provider=provider,
            method=method,
            max_steps=max_steps,
            eval_=eval_,
            backend_options=backend_options,
            request_id=request_id,
        )

        return radiance_train_request
