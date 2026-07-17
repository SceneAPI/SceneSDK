from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_create import ImageCreate


T = TypeVar("T", bound="BatchCreateImagesRequest")


@_attrs_define
class BatchCreateImagesRequest:
    """AIP-231 batch-create request body. Each entry is a complete
    ``ImageCreate``; the server registers them all in a single
    transaction.

        Attributes:
            requests (list[ImageCreate] | Unset):
    """

    requests: list[ImageCreate] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        requests: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.requests, Unset):
            requests = []
            for requests_item_data in self.requests:
                requests_item = requests_item_data.to_dict()
                requests.append(requests_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if requests is not UNSET:
            field_dict["requests"] = requests

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.image_create import ImageCreate

        d = dict(src_dict)
        _requests = d.pop("requests", UNSET)
        requests: list[ImageCreate] | Unset = UNSET
        if _requests is not UNSET:
            requests = []
            for requests_item_data in _requests:
                requests_item = ImageCreate.from_dict(requests_item_data)

                requests.append(requests_item)

        batch_create_images_request = cls(
            requests=requests,
        )

        return batch_create_images_request
