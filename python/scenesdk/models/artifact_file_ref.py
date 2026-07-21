from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArtifactFileRef")


@_attrs_define
class ArtifactFileRef:
    """One file that belongs to a portable artifact manifest.

    Attributes:
        name (str):
        uri (str):
        media_type (None | str | Unset):
        sha256 (None | str | Unset):
        byte_size (int | None | Unset):
    """

    name: str
    uri: str
    media_type: None | str | Unset = UNSET
    sha256: None | str | Unset = UNSET
    byte_size: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uri = self.uri

        media_type: None | str | Unset
        if isinstance(self.media_type, Unset):
            media_type = UNSET
        else:
            media_type = self.media_type

        sha256: None | str | Unset
        if isinstance(self.sha256, Unset):
            sha256 = UNSET
        else:
            sha256 = self.sha256

        byte_size: int | None | Unset
        if isinstance(self.byte_size, Unset):
            byte_size = UNSET
        else:
            byte_size = self.byte_size

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "uri": uri,
            }
        )
        if media_type is not UNSET:
            field_dict["media_type"] = media_type
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if byte_size is not UNSET:
            field_dict["byte_size"] = byte_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        uri = d.pop("uri")

        def _parse_media_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        media_type = _parse_media_type(d.pop("media_type", UNSET))

        def _parse_sha256(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sha256 = _parse_sha256(d.pop("sha256", UNSET))

        def _parse_byte_size(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        byte_size = _parse_byte_size(d.pop("byte_size", UNSET))

        artifact_file_ref = cls(
            name=name,
            uri=uri,
            media_type=media_type,
            sha256=sha256,
            byte_size=byte_size,
        )

        return artifact_file_ref
