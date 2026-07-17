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
    from ..models.upload_entry_spec import UploadEntrySpec


T = TypeVar("T", bound="UploadSourceSpec")


@_attrs_define
class UploadSourceSpec:
    """Image source backed by previously-uploaded blobs (sfmapi owns
    the bytes via the content-addressed blob store).

        Attributes:
            kind (Literal['upload'] | Unset):  Default: 'upload'.
            entries (list[UploadEntrySpec] | Unset):
    """

    kind: Literal["upload"] | Unset = "upload"
    entries: list[UploadEntrySpec] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        entries: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.entries, Unset):
            entries = []
            for entries_item_data in self.entries:
                entries_item = entries_item_data.to_dict()
                entries.append(entries_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if entries is not UNSET:
            field_dict["entries"] = entries

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.upload_entry_spec import UploadEntrySpec

        d = dict(src_dict)
        kind = cast(Literal["upload"] | Unset, d.pop("kind", UNSET))
        if kind != "upload" and not isinstance(kind, Unset):
            raise ValueError(f"kind must match const 'upload', got '{kind}'")

        _entries = d.pop("entries", UNSET)
        entries: list[UploadEntrySpec] | Unset = UNSET
        if _entries is not UNSET:
            entries = []
            for entries_item_data in _entries:
                entries_item = UploadEntrySpec.from_dict(entries_item_data)

                entries.append(entries_item)

        upload_source_spec = cls(
            kind=kind,
            entries=entries,
        )

        return upload_source_spec
