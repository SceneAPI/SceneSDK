from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.localization_request_sift_type_0 import LocalizationRequestSiftType0


T = TypeVar("T", bound="LocalizationRequest")


@_attrs_define
class LocalizationRequest:
    """Request body for ``POST /v1/reconstructions/{rid}/localize``.

    Attributes:
        blob_sha (str):
        sift (LocalizationRequestSiftType0 | None | Unset):
        provider (None | str | Unset): Optional provider id to execute this localize job.
    """

    blob_sha: str
    sift: LocalizationRequestSiftType0 | None | Unset = UNSET
    provider: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.localization_request_sift_type_0 import (
            LocalizationRequestSiftType0,
        )

        blob_sha = self.blob_sha

        sift: dict[str, Any] | None | Unset
        if isinstance(self.sift, Unset):
            sift = UNSET
        elif isinstance(self.sift, LocalizationRequestSiftType0):
            sift = self.sift.to_dict()
        else:
            sift = self.sift

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "blob_sha": blob_sha,
            }
        )
        if sift is not UNSET:
            field_dict["sift"] = sift
        if provider is not UNSET:
            field_dict["provider"] = provider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.localization_request_sift_type_0 import (
            LocalizationRequestSiftType0,
        )

        d = dict(src_dict)
        blob_sha = d.pop("blob_sha")

        def _parse_sift(data: object) -> LocalizationRequestSiftType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sift_type_0 = LocalizationRequestSiftType0.from_dict(data)

                return sift_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LocalizationRequestSiftType0 | None | Unset, data)

        sift = _parse_sift(d.pop("sift", UNSET))

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        localization_request = cls(
            blob_sha=blob_sha,
            sift=sift,
            provider=provider,
        )

        return localization_request
