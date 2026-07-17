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

from ..models.export_spec_format import ExportSpecFormat
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.export_spec_backend_options import ExportSpecBackendOptions


T = TypeVar("T", bound="ExportSpec")


@_attrs_define
class ExportSpec:
    """``POST /v1/reconstructions/{rid}:export`` — export the sparse model
    to a portable interchange format (capability ``export.{format}``).

        Attributes:
            version (Literal[1] | Unset):  Default: 1.
            provider (None | str | Unset): Optional sfm_hub provider id to execute this stage. When unset, the server
                resolves one through routing profiles.
            backend_options (ExportSpecBackendOptions | Unset): Backend-specific options. Discover supported keys with GET
                /v1/backend/config-schemas.
            format_ (ExportSpecFormat | Unset):  Default: ExportSpecFormat.PLY.
    """

    version: Literal[1] | Unset = 1
    provider: None | str | Unset = UNSET
    backend_options: ExportSpecBackendOptions | Unset = UNSET
    format_: ExportSpecFormat | Unset = ExportSpecFormat.PLY

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

        format_: str | Unset = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if provider is not UNSET:
            field_dict["provider"] = provider
        if backend_options is not UNSET:
            field_dict["backend_options"] = backend_options
        if format_ is not UNSET:
            field_dict["format"] = format_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.export_spec_backend_options import ExportSpecBackendOptions

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
        backend_options: ExportSpecBackendOptions | Unset
        if isinstance(_backend_options, Unset):
            backend_options = UNSET
        else:
            backend_options = ExportSpecBackendOptions.from_dict(_backend_options)

        _format_ = d.pop("format", UNSET)
        format_: ExportSpecFormat | Unset
        if isinstance(_format_, Unset):
            format_ = UNSET
        else:
            format_ = ExportSpecFormat(_format_)

        export_spec = cls(
            version=version,
            provider=provider,
            backend_options=backend_options,
            format_=format_,
        )

        return export_spec
