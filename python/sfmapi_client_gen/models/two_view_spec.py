from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.two_view_spec_backend_options import TwoViewSpecBackendOptions


T = TypeVar("T", bound="TwoViewSpec")


@_attrs_define
class TwoViewSpec:
    """``POST /v1/datasets/{did}:estimateTwoView`` — estimate two-view
    geometry (E/F/H + relative pose) for image pairs in the dataset's
    feature database (capability ``geometry.two_view``).

        Attributes:
            version (Literal[1] | Unset):  Default: 1.
            provider (None | str | Unset): Optional sfm_hub provider id to execute this stage. When unset, the server
                resolves one through routing profiles.
            backend_options (TwoViewSpecBackendOptions | Unset): Backend-specific options. Discover supported keys with GET
                /v1/backend/config-schemas.
    """

    version: Literal[1] | Unset = 1
    provider: None | str | Unset = UNSET
    backend_options: TwoViewSpecBackendOptions | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        backend_options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.backend_options, Unset):
            backend_options = self.backend_options.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if provider is not UNSET:
            field_dict["provider"] = provider
        if backend_options is not UNSET:
            field_dict["backend_options"] = backend_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.two_view_spec_backend_options import TwoViewSpecBackendOptions

        d = dict(src_dict)
        version = cast(Literal[1] | Unset, d.pop("version", UNSET))
        if version != 1 and not isinstance(version, Unset):
            raise ValueError(f"version must match const 1, got '{version}'")

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        _backend_options = d.pop("backend_options", UNSET)
        backend_options: TwoViewSpecBackendOptions | Unset
        if isinstance(_backend_options, Unset):
            backend_options = UNSET
        else:
            backend_options = TwoViewSpecBackendOptions.from_dict(_backend_options)

        two_view_spec = cls(
            version=version,
            provider=provider,
            backend_options=backend_options,
        )

        return two_view_spec
