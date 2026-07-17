from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.radiance_snapshot_out_links_type_0 import (
        RadianceSnapshotOutLinksType0,
    )
    from ..models.radiance_snapshot_out_summary_type_0 import (
        RadianceSnapshotOutSummaryType0,
    )


T = TypeVar("T", bound="RadianceSnapshotOut")


@_attrs_define
class RadianceSnapshotOut:
    """
    Attributes:
        snapshot_id (str):
        radiance_field_id (str):
        seq (int):
        created_at (datetime.datetime):
        field_links (None | RadianceSnapshotOutLinksType0 | Unset):
        summary (None | RadianceSnapshotOutSummaryType0 | Unset):
    """

    snapshot_id: str
    radiance_field_id: str
    seq: int
    created_at: datetime.datetime
    field_links: None | RadianceSnapshotOutLinksType0 | Unset = UNSET
    summary: None | RadianceSnapshotOutSummaryType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.radiance_snapshot_out_links_type_0 import (
            RadianceSnapshotOutLinksType0,
        )
        from ..models.radiance_snapshot_out_summary_type_0 import (
            RadianceSnapshotOutSummaryType0,
        )

        snapshot_id = self.snapshot_id

        radiance_field_id = self.radiance_field_id

        seq = self.seq

        created_at = self.created_at.isoformat()

        field_links: dict[str, Any] | None | Unset
        if isinstance(self.field_links, Unset):
            field_links = UNSET
        elif isinstance(self.field_links, RadianceSnapshotOutLinksType0):
            field_links = self.field_links.to_dict()
        else:
            field_links = self.field_links

        summary: dict[str, Any] | None | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        elif isinstance(self.summary, RadianceSnapshotOutSummaryType0):
            summary = self.summary.to_dict()
        else:
            summary = self.summary

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "snapshot_id": snapshot_id,
                "radiance_field_id": radiance_field_id,
                "seq": seq,
                "created_at": created_at,
            }
        )
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.radiance_snapshot_out_links_type_0 import (
            RadianceSnapshotOutLinksType0,
        )
        from ..models.radiance_snapshot_out_summary_type_0 import (
            RadianceSnapshotOutSummaryType0,
        )

        d = dict(src_dict)
        snapshot_id = d.pop("snapshot_id")

        radiance_field_id = d.pop("radiance_field_id")

        seq = d.pop("seq")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_field_links(
            data: object,
        ) -> None | RadianceSnapshotOutLinksType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                field_links_type_0 = RadianceSnapshotOutLinksType0.from_dict(data)

                return field_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RadianceSnapshotOutLinksType0 | Unset, data)

        field_links = _parse_field_links(d.pop("_links", UNSET))

        def _parse_summary(
            data: object,
        ) -> None | RadianceSnapshotOutSummaryType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0 = RadianceSnapshotOutSummaryType0.from_dict(data)

                return summary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RadianceSnapshotOutSummaryType0 | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        radiance_snapshot_out = cls(
            snapshot_id=snapshot_id,
            radiance_field_id=radiance_field_id,
            seq=seq,
            created_at=created_at,
            field_links=field_links,
            summary=summary,
        )

        radiance_snapshot_out.additional_properties = d
        return radiance_snapshot_out

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
