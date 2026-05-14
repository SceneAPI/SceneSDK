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

from ..models.bundle_adjustment_spec_loss_kernel import BundleAdjustmentSpecLossKernel
from ..models.bundle_adjustment_spec_mode import BundleAdjustmentSpecMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bundle_adjustment_spec_backend_options import (
        BundleAdjustmentSpecBackendOptions,
    )


T = TypeVar("T", bound="BundleAdjustmentSpec")


@_attrs_define
class BundleAdjustmentSpec:
    """Standalone bundle-adjustment spec.

    ``mode`` selects the algorithm:
      - ``standard``: a single ceres / baxx solve over all
        registered cameras + 3D points (capability ``ba.standard``).
      - ``two_stage``: a two-pass refinement (capability ``ba.two_stage``).
      - ``featuremetric``: Pixel-Perfect SfM-style refinement that
        minimizes a CNN-feature error, not raw reprojection
        (capability ``ba.featuremetric``). Requires a backend with
        learned-feature support.
      - ``rig``: rig-aware refinement that shares intrinsics + relative
        extrinsics across a multi-camera rig (capability ``ba.rig``).

    ``loss_kernel`` chooses the robust loss applied to per-residual
    cost: ``squared`` (no robustification), ``huber``, ``cauchy``,
    ``soft_l1``, ``tukey``. ``loss_threshold`` is the kernel scale
    (in pixels for reprojection loss).

        Attributes:
            version (Literal[1] | Unset):  Default: 1.
            mode (BundleAdjustmentSpecMode | Unset):  Default: BundleAdjustmentSpecMode.STANDARD.
            provider (None | str | Unset): Optional backend implementation selector for bundle adjustment when multiple
                providers expose the requested ba.* capability.
            refine_focal_length (bool | Unset):  Default: True.
            refine_principal_point (bool | Unset):  Default: False.
            refine_extra_params (bool | Unset):  Default: True.
            max_num_iterations (int | Unset):  Default: 100.
            loss_kernel (BundleAdjustmentSpecLossKernel | Unset):  Default: BundleAdjustmentSpecLossKernel.SQUARED.
            loss_threshold (float | Unset):  Default: 1.0.
            backend_options (BundleAdjustmentSpecBackendOptions | Unset): Backend-specific bundle-adjustment options.
                Discover supported keys with GET /v1/backend/config-schemas.
    """

    version: Literal[1] | Unset = 1
    mode: BundleAdjustmentSpecMode | Unset = BundleAdjustmentSpecMode.STANDARD
    provider: None | str | Unset = UNSET
    refine_focal_length: bool | Unset = True
    refine_principal_point: bool | Unset = False
    refine_extra_params: bool | Unset = True
    max_num_iterations: int | Unset = 100
    loss_kernel: BundleAdjustmentSpecLossKernel | Unset = (
        BundleAdjustmentSpecLossKernel.SQUARED
    )
    loss_threshold: float | Unset = 1.0
    backend_options: BundleAdjustmentSpecBackendOptions | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        refine_focal_length = self.refine_focal_length

        refine_principal_point = self.refine_principal_point

        refine_extra_params = self.refine_extra_params

        max_num_iterations = self.max_num_iterations

        loss_kernel: str | Unset = UNSET
        if not isinstance(self.loss_kernel, Unset):
            loss_kernel = self.loss_kernel.value

        loss_threshold = self.loss_threshold

        backend_options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.backend_options, Unset):
            backend_options = self.backend_options.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if mode is not UNSET:
            field_dict["mode"] = mode
        if provider is not UNSET:
            field_dict["provider"] = provider
        if refine_focal_length is not UNSET:
            field_dict["refine_focal_length"] = refine_focal_length
        if refine_principal_point is not UNSET:
            field_dict["refine_principal_point"] = refine_principal_point
        if refine_extra_params is not UNSET:
            field_dict["refine_extra_params"] = refine_extra_params
        if max_num_iterations is not UNSET:
            field_dict["max_num_iterations"] = max_num_iterations
        if loss_kernel is not UNSET:
            field_dict["loss_kernel"] = loss_kernel
        if loss_threshold is not UNSET:
            field_dict["loss_threshold"] = loss_threshold
        if backend_options is not UNSET:
            field_dict["backend_options"] = backend_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bundle_adjustment_spec_backend_options import (
            BundleAdjustmentSpecBackendOptions,
        )

        d = dict(src_dict)
        version = cast(Literal[1] | Unset, d.pop("version", UNSET))
        if version != 1 and not isinstance(version, Unset):
            raise ValueError(f"version must match const 1, got '{version}'")

        _mode = d.pop("mode", UNSET)
        mode: BundleAdjustmentSpecMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = BundleAdjustmentSpecMode(_mode)

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        refine_focal_length = d.pop("refine_focal_length", UNSET)

        refine_principal_point = d.pop("refine_principal_point", UNSET)

        refine_extra_params = d.pop("refine_extra_params", UNSET)

        max_num_iterations = d.pop("max_num_iterations", UNSET)

        _loss_kernel = d.pop("loss_kernel", UNSET)
        loss_kernel: BundleAdjustmentSpecLossKernel | Unset
        if isinstance(_loss_kernel, Unset):
            loss_kernel = UNSET
        else:
            loss_kernel = BundleAdjustmentSpecLossKernel(_loss_kernel)

        loss_threshold = d.pop("loss_threshold", UNSET)

        _backend_options = d.pop("backend_options", UNSET)
        backend_options: BundleAdjustmentSpecBackendOptions | Unset
        if isinstance(_backend_options, Unset):
            backend_options = UNSET
        else:
            backend_options = BundleAdjustmentSpecBackendOptions.from_dict(
                _backend_options
            )

        bundle_adjustment_spec = cls(
            version=version,
            mode=mode,
            provider=provider,
            refine_focal_length=refine_focal_length,
            refine_principal_point=refine_principal_point,
            refine_extra_params=refine_extra_params,
            max_num_iterations=max_num_iterations,
            loss_kernel=loss_kernel,
            loss_threshold=loss_threshold,
            backend_options=backend_options,
        )

        return bundle_adjustment_spec
