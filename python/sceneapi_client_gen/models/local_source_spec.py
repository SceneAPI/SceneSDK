from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="LocalSourceSpec")


@_attrs_define
class LocalSourceSpec:
    """Image source pointing at a worker-local directory tree. Bytes
    are NEVER copied — workers stream from ``root`` in place. Locked
    by ``L3`` in ``docs/guides/decisions.md`` (50GB local dirs).

        Attributes:
            root (str):
            kind (Literal['local'] | Unset):  Default: 'local'.
            recursive (bool | Unset):  Default: True.
    """

    root: str
    kind: Literal["local"] | Unset = "local"
    recursive: bool | Unset = True

    def to_dict(self) -> dict[str, Any]:
        root = self.root

        kind = self.kind

        recursive = self.recursive

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "root": root,
            }
        )
        if kind is not UNSET:
            field_dict["kind"] = kind
        if recursive is not UNSET:
            field_dict["recursive"] = recursive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        root = d.pop("root")

        kind = cast(Literal["local"] | Unset, d.pop("kind", UNSET))
        if kind != "local" and not isinstance(kind, Unset):
            raise ValueError(f"kind must match const 'local', got '{kind}'")

        recursive = d.pop("recursive", UNSET)

        local_source_spec = cls(
            root=root,
            kind=kind,
            recursive=recursive,
        )

        return local_source_spec
