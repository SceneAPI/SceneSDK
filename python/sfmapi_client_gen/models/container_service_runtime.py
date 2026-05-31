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
    from ..models.container_service_cache import ContainerServiceCache
    from ..models.container_service_endpoint import ContainerServiceEndpoint
    from ..models.container_service_execution import ContainerServiceExecution
    from ..models.container_service_healthcheck import ContainerServiceHealthcheck
    from ..models.container_service_image import ContainerServiceImage
    from ..models.container_service_object_store import ContainerServiceObjectStore
    from ..models.container_service_provenance import ContainerServiceProvenance


T = TypeVar("T", bound="ContainerServiceRuntime")


@_attrs_define
class ContainerServiceRuntime:
    """
    Attributes:
        protocol (Literal['sfmapi-plugin-http-v1']):
        protocol_version (str):
        service (ContainerServiceEndpoint):
        image (ContainerServiceImage | None | Unset):
        object_store (ContainerServiceObjectStore | None | Unset):
        cache (ContainerServiceCache | Unset):
        provenance (ContainerServiceProvenance | Unset):
        healthcheck (ContainerServiceHealthcheck | Unset):
        execution (ContainerServiceExecution | Unset):
    """

    protocol: Literal["sfmapi-plugin-http-v1"]
    protocol_version: str
    service: ContainerServiceEndpoint
    image: ContainerServiceImage | None | Unset = UNSET
    object_store: ContainerServiceObjectStore | None | Unset = UNSET
    cache: ContainerServiceCache | Unset = UNSET
    provenance: ContainerServiceProvenance | Unset = UNSET
    healthcheck: ContainerServiceHealthcheck | Unset = UNSET
    execution: ContainerServiceExecution | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.container_service_image import ContainerServiceImage
        from ..models.container_service_object_store import ContainerServiceObjectStore

        protocol = self.protocol

        protocol_version = self.protocol_version

        service = self.service.to_dict()

        image: dict[str, Any] | None | Unset
        if isinstance(self.image, Unset):
            image = UNSET
        elif isinstance(self.image, ContainerServiceImage):
            image = self.image.to_dict()
        else:
            image = self.image

        object_store: dict[str, Any] | None | Unset
        if isinstance(self.object_store, Unset):
            object_store = UNSET
        elif isinstance(self.object_store, ContainerServiceObjectStore):
            object_store = self.object_store.to_dict()
        else:
            object_store = self.object_store

        cache: dict[str, Any] | Unset = UNSET
        if not isinstance(self.cache, Unset):
            cache = self.cache.to_dict()

        provenance: dict[str, Any] | Unset = UNSET
        if not isinstance(self.provenance, Unset):
            provenance = self.provenance.to_dict()

        healthcheck: dict[str, Any] | Unset = UNSET
        if not isinstance(self.healthcheck, Unset):
            healthcheck = self.healthcheck.to_dict()

        execution: dict[str, Any] | Unset = UNSET
        if not isinstance(self.execution, Unset):
            execution = self.execution.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "protocol": protocol,
                "protocol_version": protocol_version,
                "service": service,
            }
        )
        if image is not UNSET:
            field_dict["image"] = image
        if object_store is not UNSET:
            field_dict["object_store"] = object_store
        if cache is not UNSET:
            field_dict["cache"] = cache
        if provenance is not UNSET:
            field_dict["provenance"] = provenance
        if healthcheck is not UNSET:
            field_dict["healthcheck"] = healthcheck
        if execution is not UNSET:
            field_dict["execution"] = execution

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_service_cache import ContainerServiceCache
        from ..models.container_service_endpoint import ContainerServiceEndpoint
        from ..models.container_service_execution import ContainerServiceExecution
        from ..models.container_service_healthcheck import ContainerServiceHealthcheck
        from ..models.container_service_image import ContainerServiceImage
        from ..models.container_service_object_store import ContainerServiceObjectStore
        from ..models.container_service_provenance import ContainerServiceProvenance

        d = dict(src_dict)
        protocol = cast(Literal["sfmapi-plugin-http-v1"], d.pop("protocol"))
        if protocol != "sfmapi-plugin-http-v1":
            raise ValueError(
                f"protocol must match const 'sfmapi-plugin-http-v1', got '{protocol}'"
            )

        protocol_version = d.pop("protocol_version")

        service = ContainerServiceEndpoint.from_dict(d.pop("service"))

        def _parse_image(data: object) -> ContainerServiceImage | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                image_type_0 = ContainerServiceImage.from_dict(data)

                return image_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ContainerServiceImage | None | Unset, data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_object_store(
            data: object,
        ) -> ContainerServiceObjectStore | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                object_store_type_0 = ContainerServiceObjectStore.from_dict(data)

                return object_store_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ContainerServiceObjectStore | None | Unset, data)

        object_store = _parse_object_store(d.pop("object_store", UNSET))

        _cache = d.pop("cache", UNSET)
        cache: ContainerServiceCache | Unset
        if isinstance(_cache, Unset):
            cache = UNSET
        else:
            cache = ContainerServiceCache.from_dict(_cache)

        _provenance = d.pop("provenance", UNSET)
        provenance: ContainerServiceProvenance | Unset
        if isinstance(_provenance, Unset):
            provenance = UNSET
        else:
            provenance = ContainerServiceProvenance.from_dict(_provenance)

        _healthcheck = d.pop("healthcheck", UNSET)
        healthcheck: ContainerServiceHealthcheck | Unset
        if isinstance(_healthcheck, Unset):
            healthcheck = UNSET
        else:
            healthcheck = ContainerServiceHealthcheck.from_dict(_healthcheck)

        _execution = d.pop("execution", UNSET)
        execution: ContainerServiceExecution | Unset
        if isinstance(_execution, Unset):
            execution = UNSET
        else:
            execution = ContainerServiceExecution.from_dict(_execution)

        container_service_runtime = cls(
            protocol=protocol,
            protocol_version=protocol_version,
            service=service,
            image=image,
            object_store=object_store,
            cache=cache,
            provenance=provenance,
            healthcheck=healthcheck,
            execution=execution,
        )

        return container_service_runtime
