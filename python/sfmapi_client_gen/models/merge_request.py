from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.merge_request_sim_3_aligners_type_0_item import (
        MergeRequestSim3AlignersType0Item,
    )


T = TypeVar("T", bound="MergeRequest")


@_attrs_define
class MergeRequest:
    """Request body for ``POST /v1/reconstructions:merge``.

    Attributes:
        target_recon_id (str):
        source_recon_ids (list[str]):
        sim3_aligners (list[MergeRequestSim3AlignersType0Item] | None | Unset):
        provider (None | str | Unset): Optional provider id to execute the merge.
    """

    target_recon_id: str
    source_recon_ids: list[str]
    sim3_aligners: list[MergeRequestSim3AlignersType0Item] | None | Unset = UNSET
    provider: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        target_recon_id = self.target_recon_id

        source_recon_ids = self.source_recon_ids

        sim3_aligners: list[dict[str, Any]] | None | Unset
        if isinstance(self.sim3_aligners, Unset):
            sim3_aligners = UNSET
        elif isinstance(self.sim3_aligners, list):
            sim3_aligners = []
            for sim3_aligners_type_0_item_data in self.sim3_aligners:
                sim3_aligners_type_0_item = sim3_aligners_type_0_item_data.to_dict()
                sim3_aligners.append(sim3_aligners_type_0_item)

        else:
            sim3_aligners = self.sim3_aligners

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "target_recon_id": target_recon_id,
                "source_recon_ids": source_recon_ids,
            }
        )
        if sim3_aligners is not UNSET:
            field_dict["sim3_aligners"] = sim3_aligners
        if provider is not UNSET:
            field_dict["provider"] = provider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.merge_request_sim_3_aligners_type_0_item import (
            MergeRequestSim3AlignersType0Item,
        )

        d = dict(src_dict)
        target_recon_id = d.pop("target_recon_id")

        source_recon_ids = cast(list[str], d.pop("source_recon_ids"))

        def _parse_sim3_aligners(
            data: object,
        ) -> list[MergeRequestSim3AlignersType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sim3_aligners_type_0 = []
                _sim3_aligners_type_0 = data
                for sim3_aligners_type_0_item_data in _sim3_aligners_type_0:
                    sim3_aligners_type_0_item = (
                        MergeRequestSim3AlignersType0Item.from_dict(
                            sim3_aligners_type_0_item_data
                        )
                    )

                    sim3_aligners_type_0.append(sim3_aligners_type_0_item)

                return sim3_aligners_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[MergeRequestSim3AlignersType0Item] | None | Unset, data)

        sim3_aligners = _parse_sim3_aligners(d.pop("sim3_aligners", UNSET))

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        merge_request = cls(
            target_recon_id=target_recon_id,
            source_recon_ids=source_recon_ids,
            sim3_aligners=sim3_aligners,
            provider=provider,
        )

        return merge_request
