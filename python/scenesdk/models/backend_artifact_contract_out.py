from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_conversion_out import ArtifactConversionOut
    from ..models.backend_artifact_contract_out_links_type_0 import (
        BackendArtifactContractOutLinksType0,
    )
    from ..models.backend_artifact_contract_out_metadata import (
        BackendArtifactContractOutMetadata,
    )


T = TypeVar("T", bound="BackendArtifactContractOut")


@_attrs_define
class BackendArtifactContractOut:
    """Discoverable artifact input/output contract for a portable stage.

    Attributes:
        contract_id (str):
        backend (str):
        stage (str):
        display_name (str):
        capability (None | str | Unset):
        provider (None | str | Unset):
        description (None | str | Unset):
        accepts (list[str] | Unset):
        emits (list[str] | Unset):
        accepts_formats (list[str] | Unset):
        emits_formats (list[str] | Unset):
        preferred (None | str | Unset):
        preferred_format (None | str | Unset):
        conversions (list[ArtifactConversionOut] | Unset):
        metadata (BackendArtifactContractOutMetadata | Unset):
        field_links (BackendArtifactContractOutLinksType0 | None | Unset):
    """

    contract_id: str
    backend: str
    stage: str
    display_name: str
    capability: None | str | Unset = UNSET
    provider: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    accepts: list[str] | Unset = UNSET
    emits: list[str] | Unset = UNSET
    accepts_formats: list[str] | Unset = UNSET
    emits_formats: list[str] | Unset = UNSET
    preferred: None | str | Unset = UNSET
    preferred_format: None | str | Unset = UNSET
    conversions: list[ArtifactConversionOut] | Unset = UNSET
    metadata: BackendArtifactContractOutMetadata | Unset = UNSET
    field_links: BackendArtifactContractOutLinksType0 | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.backend_artifact_contract_out_links_type_0 import (
            BackendArtifactContractOutLinksType0,
        )

        contract_id = self.contract_id

        backend = self.backend

        stage = self.stage

        display_name = self.display_name

        capability: None | str | Unset
        if isinstance(self.capability, Unset):
            capability = UNSET
        else:
            capability = self.capability

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        accepts: list[str] | Unset = UNSET
        if not isinstance(self.accepts, Unset):
            accepts = self.accepts

        emits: list[str] | Unset = UNSET
        if not isinstance(self.emits, Unset):
            emits = self.emits

        accepts_formats: list[str] | Unset = UNSET
        if not isinstance(self.accepts_formats, Unset):
            accepts_formats = self.accepts_formats

        emits_formats: list[str] | Unset = UNSET
        if not isinstance(self.emits_formats, Unset):
            emits_formats = self.emits_formats

        preferred: None | str | Unset
        if isinstance(self.preferred, Unset):
            preferred = UNSET
        else:
            preferred = self.preferred

        preferred_format: None | str | Unset
        if isinstance(self.preferred_format, Unset):
            preferred_format = UNSET
        else:
            preferred_format = self.preferred_format

        conversions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.conversions, Unset):
            conversions = []
            for conversions_item_data in self.conversions:
                conversions_item = conversions_item_data.to_dict()
                conversions.append(conversions_item)

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_links: dict[str, Any] | None | Unset
        if isinstance(self.field_links, Unset):
            field_links = UNSET
        elif isinstance(self.field_links, BackendArtifactContractOutLinksType0):
            field_links = self.field_links.to_dict()
        else:
            field_links = self.field_links

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "contract_id": contract_id,
                "backend": backend,
                "stage": stage,
                "display_name": display_name,
            }
        )
        if capability is not UNSET:
            field_dict["capability"] = capability
        if provider is not UNSET:
            field_dict["provider"] = provider
        if description is not UNSET:
            field_dict["description"] = description
        if accepts is not UNSET:
            field_dict["accepts"] = accepts
        if emits is not UNSET:
            field_dict["emits"] = emits
        if accepts_formats is not UNSET:
            field_dict["accepts_formats"] = accepts_formats
        if emits_formats is not UNSET:
            field_dict["emits_formats"] = emits_formats
        if preferred is not UNSET:
            field_dict["preferred"] = preferred
        if preferred_format is not UNSET:
            field_dict["preferred_format"] = preferred_format
        if conversions is not UNSET:
            field_dict["conversions"] = conversions
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if field_links is not UNSET:
            field_dict["_links"] = field_links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_conversion_out import ArtifactConversionOut
        from ..models.backend_artifact_contract_out_links_type_0 import (
            BackendArtifactContractOutLinksType0,
        )
        from ..models.backend_artifact_contract_out_metadata import (
            BackendArtifactContractOutMetadata,
        )

        d = dict(src_dict)
        contract_id = d.pop("contract_id")

        backend = d.pop("backend")

        stage = d.pop("stage")

        display_name = d.pop("display_name")

        def _parse_capability(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        capability = _parse_capability(d.pop("capability", UNSET))

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        accepts = cast(list[str], d.pop("accepts", UNSET))

        emits = cast(list[str], d.pop("emits", UNSET))

        accepts_formats = cast(list[str], d.pop("accepts_formats", UNSET))

        emits_formats = cast(list[str], d.pop("emits_formats", UNSET))

        def _parse_preferred(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        preferred = _parse_preferred(d.pop("preferred", UNSET))

        def _parse_preferred_format(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        preferred_format = _parse_preferred_format(d.pop("preferred_format", UNSET))

        _conversions = d.pop("conversions", UNSET)
        conversions: list[ArtifactConversionOut] | Unset = UNSET
        if _conversions is not UNSET:
            conversions = []
            for conversions_item_data in _conversions:
                conversions_item = ArtifactConversionOut.from_dict(
                    conversions_item_data
                )

                conversions.append(conversions_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: BackendArtifactContractOutMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = BackendArtifactContractOutMetadata.from_dict(_metadata)

        def _parse_field_links(
            data: object,
        ) -> BackendArtifactContractOutLinksType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                field_links_type_0 = BackendArtifactContractOutLinksType0.from_dict(
                    data
                )

                return field_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BackendArtifactContractOutLinksType0 | None | Unset, data)

        field_links = _parse_field_links(d.pop("_links", UNSET))

        backend_artifact_contract_out = cls(
            contract_id=contract_id,
            backend=backend,
            stage=stage,
            display_name=display_name,
            capability=capability,
            provider=provider,
            description=description,
            accepts=accepts,
            emits=emits,
            accepts_formats=accepts_formats,
            emits_formats=emits_formats,
            preferred=preferred,
            preferred_format=preferred_format,
            conversions=conversions,
            metadata=metadata,
            field_links=field_links,
        )

        return backend_artifact_contract_out
