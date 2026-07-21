from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.radiance_field_out_status import RadianceFieldOutStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.radiance_field_out_links_type_0 import RadianceFieldOutLinksType0
    from ..models.radiance_field_out_spec import RadianceFieldOutSpec
    from ..models.radiance_field_out_summary_type_0 import RadianceFieldOutSummaryType0


T = TypeVar("T", bound="RadianceFieldOut")


@_attrs_define
class RadianceFieldOut:
    """
    Attributes:
        radiance_field_id (str):
        project_id (str):
        name (str):
        provider (str):
        method (str):
        status (RadianceFieldOutStatus):
        spec (RadianceFieldOutSpec):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        field_links (None | RadianceFieldOutLinksType0 | Unset):
        dataset_id (None | str | Unset):
        recon_id (None | str | Unset):
        summary (None | RadianceFieldOutSummaryType0 | Unset):
    """

    radiance_field_id: str
    project_id: str
    name: str
    provider: str
    method: str
    status: RadianceFieldOutStatus
    spec: RadianceFieldOutSpec
    created_at: datetime.datetime
    updated_at: datetime.datetime
    field_links: None | RadianceFieldOutLinksType0 | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    recon_id: None | str | Unset = UNSET
    summary: None | RadianceFieldOutSummaryType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.radiance_field_out_links_type_0 import RadianceFieldOutLinksType0
        from ..models.radiance_field_out_summary_type_0 import (
            RadianceFieldOutSummaryType0,
        )

        radiance_field_id = self.radiance_field_id

        project_id = self.project_id

        name = self.name

        provider = self.provider

        method = self.method

        status = self.status.value

        spec = self.spec.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_links: dict[str, Any] | None | Unset
        if isinstance(self.field_links, Unset):
            field_links = UNSET
        elif isinstance(self.field_links, RadianceFieldOutLinksType0):
            field_links = self.field_links.to_dict()
        else:
            field_links = self.field_links

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

        summary: dict[str, Any] | None | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        elif isinstance(self.summary, RadianceFieldOutSummaryType0):
            summary = self.summary.to_dict()
        else:
            summary = self.summary

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "radiance_field_id": radiance_field_id,
                "project_id": project_id,
                "name": name,
                "provider": provider,
                "method": method,
                "status": status,
                "spec": spec,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if recon_id is not UNSET:
            field_dict["recon_id"] = recon_id
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.radiance_field_out_links_type_0 import RadianceFieldOutLinksType0
        from ..models.radiance_field_out_spec import RadianceFieldOutSpec
        from ..models.radiance_field_out_summary_type_0 import (
            RadianceFieldOutSummaryType0,
        )

        d = dict(src_dict)
        radiance_field_id = d.pop("radiance_field_id")

        project_id = d.pop("project_id")

        name = d.pop("name")

        provider = d.pop("provider")

        method = d.pop("method")

        status = RadianceFieldOutStatus(d.pop("status"))

        spec = RadianceFieldOutSpec.from_dict(d.pop("spec"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        def _parse_field_links(
            data: object,
        ) -> None | RadianceFieldOutLinksType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                field_links_type_0 = RadianceFieldOutLinksType0.from_dict(data)

                return field_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RadianceFieldOutLinksType0 | Unset, data)

        field_links = _parse_field_links(d.pop("_links", UNSET))

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

        def _parse_summary(data: object) -> None | RadianceFieldOutSummaryType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0 = RadianceFieldOutSummaryType0.from_dict(data)

                return summary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RadianceFieldOutSummaryType0 | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        radiance_field_out = cls(
            radiance_field_id=radiance_field_id,
            project_id=project_id,
            name=name,
            provider=provider,
            method=method,
            status=status,
            spec=spec,
            created_at=created_at,
            updated_at=updated_at,
            field_links=field_links,
            dataset_id=dataset_id,
            recon_id=recon_id,
            summary=summary,
        )

        radiance_field_out.additional_properties = d
        return radiance_field_out

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
