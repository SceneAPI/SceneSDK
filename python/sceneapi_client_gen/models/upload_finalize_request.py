from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadFinalizeRequest")


@_attrs_define
class UploadFinalizeRequest:
    """
    Attributes:
        content_sha (None | str | Unset):
    """

    content_sha: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        content_sha: None | str | Unset
        if isinstance(self.content_sha, Unset):
            content_sha = UNSET
        else:
            content_sha = self.content_sha

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if content_sha is not UNSET:
            field_dict["content_sha"] = content_sha

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_content_sha(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        content_sha = _parse_content_sha(d.pop("content_sha", UNSET))

        upload_finalize_request = cls(
            content_sha=content_sha,
        )

        return upload_finalize_request
