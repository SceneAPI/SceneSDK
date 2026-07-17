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

T = TypeVar("T", bound="UvRuntime")


@_attrs_define
class UvRuntime:
    """
    Attributes:
        url (str):
        package (str):
        source (Literal['git'] | Unset):  Default: 'git'.
        ref (str | Unset):  Default: 'main'.
    """

    url: str
    package: str
    source: Literal["git"] | Unset = "git"
    ref: str | Unset = "main"

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        package = self.package

        source = self.source

        ref = self.ref

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
                "package": package,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if ref is not UNSET:
            field_dict["ref"] = ref

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        package = d.pop("package")

        source = cast(Literal["git"] | Unset, d.pop("source", UNSET))
        if source != "git" and not isinstance(source, Unset):
            raise ValueError(f"source must match const 'git', got '{source}'")

        ref = d.pop("ref", UNSET)

        uv_runtime = cls(
            url=url,
            package=package,
            source=source,
            ref=ref,
        )

        return uv_runtime
