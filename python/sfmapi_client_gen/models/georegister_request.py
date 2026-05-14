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

from ..models.georegister_request_mode import GeoregisterRequestMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.georegister_request_backend_options import (
        GeoregisterRequestBackendOptions,
    )
    from ..models.sim_3 import Sim3


T = TypeVar("T", bound="GeoregisterRequest")


@_attrs_define
class GeoregisterRequest:
    """``POST /v1/reconstructions/{rid}:georegister`` request body.

    ``mode=sim3`` (default) applies the supplied :class:`Sim3` transform
    via the backend's ``apply_sim3`` (capability ``georegister.sim3``).
    ``mode=gps`` solves the transform from georeferenced inputs via
    ``align_reconstruction`` (capability ``georegister.gps``); the
    georeferenced inputs are read from the reconstruction + the
    ``backend_options`` bag.

        Attributes:
            version (Literal[1] | Unset):  Default: 1.
            provider (None | str | Unset): Optional sfm_hub provider id to execute this stage. When unset, the server
                resolves one through routing profiles.
            backend_options (GeoregisterRequestBackendOptions | Unset): Backend-specific options. Discover supported keys
                with GET /v1/backend/config-schemas.
            mode (GeoregisterRequestMode | Unset):  Default: GeoregisterRequestMode.SIM3.
            sim3 (None | Sim3 | Unset): Required when mode='sim3'; rejected when mode='gps'.
    """

    version: Literal[1] | Unset = 1
    provider: None | str | Unset = UNSET
    backend_options: GeoregisterRequestBackendOptions | Unset = UNSET
    mode: GeoregisterRequestMode | Unset = GeoregisterRequestMode.SIM3
    sim3: None | Sim3 | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.sim_3 import Sim3

        version = self.version

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        backend_options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.backend_options, Unset):
            backend_options = self.backend_options.to_dict()

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        sim3: dict[str, Any] | None | Unset
        if isinstance(self.sim3, Unset):
            sim3 = UNSET
        elif isinstance(self.sim3, Sim3):
            sim3 = self.sim3.to_dict()
        else:
            sim3 = self.sim3

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if provider is not UNSET:
            field_dict["provider"] = provider
        if backend_options is not UNSET:
            field_dict["backend_options"] = backend_options
        if mode is not UNSET:
            field_dict["mode"] = mode
        if sim3 is not UNSET:
            field_dict["sim3"] = sim3

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.georegister_request_backend_options import (
            GeoregisterRequestBackendOptions,
        )
        from ..models.sim_3 import Sim3

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
        backend_options: GeoregisterRequestBackendOptions | Unset
        if isinstance(_backend_options, Unset):
            backend_options = UNSET
        else:
            backend_options = GeoregisterRequestBackendOptions.from_dict(
                _backend_options
            )

        _mode = d.pop("mode", UNSET)
        mode: GeoregisterRequestMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = GeoregisterRequestMode(_mode)

        def _parse_sim3(data: object) -> None | Sim3 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sim3_type_0 = Sim3.from_dict(data)

                return sim3_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Sim3 | Unset, data)

        sim3 = _parse_sim3(d.pop("sim3", UNSET))

        georegister_request = cls(
            version=version,
            provider=provider,
            backend_options=backend_options,
            mode=mode,
            sim3=sim3,
        )

        return georegister_request
