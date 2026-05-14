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
    from ..models.triangulate_spec_backend_options import TriangulateSpecBackendOptions


T = TypeVar("T", bound="TriangulateSpec")


@_attrs_define
class TriangulateSpec:
    """``POST /v1/reconstructions/{rid}:triangulate`` — re-triangulate
    against the reconstruction's existing feature database
    (capability ``triangulate.retri``).

        Attributes:
            version (Literal[1] | Unset):  Default: 1.
            provider (None | str | Unset): Optional sfm_hub provider id to execute this stage. When unset, the server
                resolves one through routing profiles.
            backend_options (TriangulateSpecBackendOptions | Unset): Backend-specific options. Discover supported keys with
                GET /v1/backend/config-schemas.
    """

    version: Literal[1] | Unset = 1
    provider: None | str | Unset = UNSET
    backend_options: TriangulateSpecBackendOptions | Unset = UNSET

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
        from ..models.triangulate_spec_backend_options import (
            TriangulateSpecBackendOptions,
        )

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
        backend_options: TriangulateSpecBackendOptions | Unset
        if isinstance(_backend_options, Unset):
            backend_options = UNSET
        else:
            backend_options = TriangulateSpecBackendOptions.from_dict(_backend_options)

        triangulate_spec = cls(
            version=version,
            provider=provider,
            backend_options=backend_options,
        )

        return triangulate_spec
