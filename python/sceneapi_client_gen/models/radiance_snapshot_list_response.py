from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.radiance_snapshot_list_response_links_type_0 import (
        RadianceSnapshotListResponseLinksType0,
    )


T = TypeVar("T", bound="RadianceSnapshotListResponse")


@_attrs_define
class RadianceSnapshotListResponse:
    """
    Attributes:
        seqs (list[int] | Unset):
        field_links (None | RadianceSnapshotListResponseLinksType0 | Unset):
    """

    seqs: list[int] | Unset = UNSET
    field_links: None | RadianceSnapshotListResponseLinksType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.radiance_snapshot_list_response_links_type_0 import (
            RadianceSnapshotListResponseLinksType0,
        )

        seqs: list[int] | Unset = UNSET
        if not isinstance(self.seqs, Unset):
            seqs = self.seqs

        field_links: dict[str, Any] | None | Unset
        if isinstance(self.field_links, Unset):
            field_links = UNSET
        elif isinstance(self.field_links, RadianceSnapshotListResponseLinksType0):
            field_links = self.field_links.to_dict()
        else:
            field_links = self.field_links

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if seqs is not UNSET:
            field_dict["seqs"] = seqs
        if field_links is not UNSET:
            field_dict["_links"] = field_links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.radiance_snapshot_list_response_links_type_0 import (
            RadianceSnapshotListResponseLinksType0,
        )

        d = dict(src_dict)
        seqs = cast(list[int], d.pop("seqs", UNSET))

        def _parse_field_links(
            data: object,
        ) -> None | RadianceSnapshotListResponseLinksType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                field_links_type_0 = RadianceSnapshotListResponseLinksType0.from_dict(
                    data
                )

                return field_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RadianceSnapshotListResponseLinksType0 | Unset, data)

        field_links = _parse_field_links(d.pop("_links", UNSET))

        radiance_snapshot_list_response = cls(
            seqs=seqs,
            field_links=field_links,
        )

        radiance_snapshot_list_response.additional_properties = d
        return radiance_snapshot_list_response

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
