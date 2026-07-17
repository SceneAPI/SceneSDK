from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.radiance_eval_config_background import RadianceEvalConfigBackground
from ..models.radiance_eval_config_lpips_net import RadianceEvalConfigLpipsNet
from ..models.radiance_eval_config_metrics_item import RadianceEvalConfigMetricsItem
from ..models.radiance_eval_config_split import RadianceEvalConfigSplit
from ..types import UNSET, Unset

T = TypeVar("T", bound="RadianceEvalConfig")


@_attrs_define
class RadianceEvalConfig:
    """Portable evaluation settings for splat providers.

    Provider-specific eval knobs stay in ``backend_options``; this shape
    captures the stable cross-provider contract exposed through the SDK.

        Attributes:
            enabled (bool | Unset):  Default: False.
            split (RadianceEvalConfigSplit | Unset):  Default: RadianceEvalConfigSplit.TEST.
            every_steps (int | None | Unset):
            final (bool | Unset):  Default: True.
            metrics (list[RadianceEvalConfigMetricsItem] | Unset):
            max_images (int | None | Unset):
            image_downscale (int | Unset):  Default: 1.
            crop_border_px (int | Unset):  Default: 0.
            save_images (bool | Unset):  Default: False.
            lpips_net (RadianceEvalConfigLpipsNet | Unset):  Default: RadianceEvalConfigLpipsNet.ALEX.
            background (RadianceEvalConfigBackground | Unset):  Default: RadianceEvalConfigBackground.DATASET.
    """

    enabled: bool | Unset = False
    split: RadianceEvalConfigSplit | Unset = RadianceEvalConfigSplit.TEST
    every_steps: int | None | Unset = UNSET
    final: bool | Unset = True
    metrics: list[RadianceEvalConfigMetricsItem] | Unset = UNSET
    max_images: int | None | Unset = UNSET
    image_downscale: int | Unset = 1
    crop_border_px: int | Unset = 0
    save_images: bool | Unset = False
    lpips_net: RadianceEvalConfigLpipsNet | Unset = RadianceEvalConfigLpipsNet.ALEX
    background: RadianceEvalConfigBackground | Unset = (
        RadianceEvalConfigBackground.DATASET
    )

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        split: str | Unset = UNSET
        if not isinstance(self.split, Unset):
            split = self.split.value

        every_steps: int | None | Unset
        if isinstance(self.every_steps, Unset):
            every_steps = UNSET
        else:
            every_steps = self.every_steps

        final = self.final

        metrics: list[str] | Unset = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = []
            for metrics_item_data in self.metrics:
                metrics_item = metrics_item_data.value
                metrics.append(metrics_item)

        max_images: int | None | Unset
        if isinstance(self.max_images, Unset):
            max_images = UNSET
        else:
            max_images = self.max_images

        image_downscale = self.image_downscale

        crop_border_px = self.crop_border_px

        save_images = self.save_images

        lpips_net: str | Unset = UNSET
        if not isinstance(self.lpips_net, Unset):
            lpips_net = self.lpips_net.value

        background: str | Unset = UNSET
        if not isinstance(self.background, Unset):
            background = self.background.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if split is not UNSET:
            field_dict["split"] = split
        if every_steps is not UNSET:
            field_dict["every_steps"] = every_steps
        if final is not UNSET:
            field_dict["final"] = final
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if max_images is not UNSET:
            field_dict["max_images"] = max_images
        if image_downscale is not UNSET:
            field_dict["image_downscale"] = image_downscale
        if crop_border_px is not UNSET:
            field_dict["crop_border_px"] = crop_border_px
        if save_images is not UNSET:
            field_dict["save_images"] = save_images
        if lpips_net is not UNSET:
            field_dict["lpips_net"] = lpips_net
        if background is not UNSET:
            field_dict["background"] = background

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        _split = d.pop("split", UNSET)
        split: RadianceEvalConfigSplit | Unset
        if isinstance(_split, Unset):
            split = UNSET
        else:
            split = RadianceEvalConfigSplit(_split)

        def _parse_every_steps(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        every_steps = _parse_every_steps(d.pop("every_steps", UNSET))

        final = d.pop("final", UNSET)

        _metrics = d.pop("metrics", UNSET)
        metrics: list[RadianceEvalConfigMetricsItem] | Unset = UNSET
        if _metrics is not UNSET:
            metrics = []
            for metrics_item_data in _metrics:
                metrics_item = RadianceEvalConfigMetricsItem(metrics_item_data)

                metrics.append(metrics_item)

        def _parse_max_images(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_images = _parse_max_images(d.pop("max_images", UNSET))

        image_downscale = d.pop("image_downscale", UNSET)

        crop_border_px = d.pop("crop_border_px", UNSET)

        save_images = d.pop("save_images", UNSET)

        _lpips_net = d.pop("lpips_net", UNSET)
        lpips_net: RadianceEvalConfigLpipsNet | Unset
        if isinstance(_lpips_net, Unset):
            lpips_net = UNSET
        else:
            lpips_net = RadianceEvalConfigLpipsNet(_lpips_net)

        _background = d.pop("background", UNSET)
        background: RadianceEvalConfigBackground | Unset
        if isinstance(_background, Unset):
            background = UNSET
        else:
            background = RadianceEvalConfigBackground(_background)

        radiance_eval_config = cls(
            enabled=enabled,
            split=split,
            every_steps=every_steps,
            final=final,
            metrics=metrics,
            max_images=max_images,
            image_downscale=image_downscale,
            crop_border_px=crop_border_px,
            save_images=save_images,
            lpips_net=lpips_net,
            background=background,
        )

        return radiance_eval_config
