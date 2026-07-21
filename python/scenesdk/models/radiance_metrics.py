from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RadianceMetrics")


@_attrs_define
class RadianceMetrics:
    """Canonical aggregate radiance evaluation metrics.

    Attributes:
        psnr_db (float | None | Unset):
        ssim (float | None | Unset):
        lpips (float | None | Unset):
        num_images (int | Unset):  Default: 0.
        duration_s (float | None | Unset):
        render_time_s_total (float | None | Unset):
        render_time_s_mean (float | None | Unset):
    """

    psnr_db: float | None | Unset = UNSET
    ssim: float | None | Unset = UNSET
    lpips: float | None | Unset = UNSET
    num_images: int | Unset = 0
    duration_s: float | None | Unset = UNSET
    render_time_s_total: float | None | Unset = UNSET
    render_time_s_mean: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        psnr_db: float | None | Unset
        if isinstance(self.psnr_db, Unset):
            psnr_db = UNSET
        else:
            psnr_db = self.psnr_db

        ssim: float | None | Unset
        if isinstance(self.ssim, Unset):
            ssim = UNSET
        else:
            ssim = self.ssim

        lpips: float | None | Unset
        if isinstance(self.lpips, Unset):
            lpips = UNSET
        else:
            lpips = self.lpips

        num_images = self.num_images

        duration_s: float | None | Unset
        if isinstance(self.duration_s, Unset):
            duration_s = UNSET
        else:
            duration_s = self.duration_s

        render_time_s_total: float | None | Unset
        if isinstance(self.render_time_s_total, Unset):
            render_time_s_total = UNSET
        else:
            render_time_s_total = self.render_time_s_total

        render_time_s_mean: float | None | Unset
        if isinstance(self.render_time_s_mean, Unset):
            render_time_s_mean = UNSET
        else:
            render_time_s_mean = self.render_time_s_mean

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if psnr_db is not UNSET:
            field_dict["psnr_db"] = psnr_db
        if ssim is not UNSET:
            field_dict["ssim"] = ssim
        if lpips is not UNSET:
            field_dict["lpips"] = lpips
        if num_images is not UNSET:
            field_dict["num_images"] = num_images
        if duration_s is not UNSET:
            field_dict["duration_s"] = duration_s
        if render_time_s_total is not UNSET:
            field_dict["render_time_s_total"] = render_time_s_total
        if render_time_s_mean is not UNSET:
            field_dict["render_time_s_mean"] = render_time_s_mean

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_psnr_db(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        psnr_db = _parse_psnr_db(d.pop("psnr_db", UNSET))

        def _parse_ssim(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        ssim = _parse_ssim(d.pop("ssim", UNSET))

        def _parse_lpips(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        lpips = _parse_lpips(d.pop("lpips", UNSET))

        num_images = d.pop("num_images", UNSET)

        def _parse_duration_s(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration_s = _parse_duration_s(d.pop("duration_s", UNSET))

        def _parse_render_time_s_total(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        render_time_s_total = _parse_render_time_s_total(
            d.pop("render_time_s_total", UNSET)
        )

        def _parse_render_time_s_mean(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        render_time_s_mean = _parse_render_time_s_mean(
            d.pop("render_time_s_mean", UNSET)
        )

        radiance_metrics = cls(
            psnr_db=psnr_db,
            ssim=ssim,
            lpips=lpips,
            num_images=num_images,
            duration_s=duration_s,
            render_time_s_total=render_time_s_total,
            render_time_s_mean=render_time_s_mean,
        )

        radiance_metrics.additional_properties = d
        return radiance_metrics

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
