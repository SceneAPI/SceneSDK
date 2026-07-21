from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerServiceProvenance")


@_attrs_define
class ContainerServiceProvenance:
    """
    Attributes:
        image_digest_required (bool | Unset):  Default: True.
        sbom_url (None | str | Unset):
        attestation_url (None | str | Unset):
        source_revision (None | str | Unset):
    """

    image_digest_required: bool | Unset = True
    sbom_url: None | str | Unset = UNSET
    attestation_url: None | str | Unset = UNSET
    source_revision: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        image_digest_required = self.image_digest_required

        sbom_url: None | str | Unset
        if isinstance(self.sbom_url, Unset):
            sbom_url = UNSET
        else:
            sbom_url = self.sbom_url

        attestation_url: None | str | Unset
        if isinstance(self.attestation_url, Unset):
            attestation_url = UNSET
        else:
            attestation_url = self.attestation_url

        source_revision: None | str | Unset
        if isinstance(self.source_revision, Unset):
            source_revision = UNSET
        else:
            source_revision = self.source_revision

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if image_digest_required is not UNSET:
            field_dict["image_digest_required"] = image_digest_required
        if sbom_url is not UNSET:
            field_dict["sbom_url"] = sbom_url
        if attestation_url is not UNSET:
            field_dict["attestation_url"] = attestation_url
        if source_revision is not UNSET:
            field_dict["source_revision"] = source_revision

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image_digest_required = d.pop("image_digest_required", UNSET)

        def _parse_sbom_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sbom_url = _parse_sbom_url(d.pop("sbom_url", UNSET))

        def _parse_attestation_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        attestation_url = _parse_attestation_url(d.pop("attestation_url", UNSET))

        def _parse_source_revision(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_revision = _parse_source_revision(d.pop("source_revision", UNSET))

        container_service_provenance = cls(
            image_digest_required=image_digest_required,
            sbom_url=sbom_url,
            attestation_url=attestation_url,
            source_revision=source_revision,
        )

        return container_service_provenance
