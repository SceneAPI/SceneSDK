from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plugin_provision_step_out import PluginProvisionStepOut
    from ..models.plugin_provisioning_out_metadata import PluginProvisioningOutMetadata
    from ..models.plugin_provisioning_out_outputs import PluginProvisioningOutOutputs
    from ..models.plugin_provisioning_out_redacted_env import (
        PluginProvisioningOutRedactedEnv,
    )


T = TypeVar("T", bound="PluginProvisioningOut")


@_attrs_define
class PluginProvisioningOut:
    """
    Attributes:
        available (bool | Unset):  Default: False.
        provisioned (bool | Unset):  Default: False.
        steps (list[PluginProvisionStepOut] | Unset):
        env_keys (list[str] | Unset):
        redacted_env (PluginProvisioningOutRedactedEnv | Unset):
        outputs (PluginProvisioningOutOutputs | Unset):
        warnings (list[str] | Unset):
        metadata (PluginProvisioningOutMetadata | Unset):
    """

    available: bool | Unset = False
    provisioned: bool | Unset = False
    steps: list[PluginProvisionStepOut] | Unset = UNSET
    env_keys: list[str] | Unset = UNSET
    redacted_env: PluginProvisioningOutRedactedEnv | Unset = UNSET
    outputs: PluginProvisioningOutOutputs | Unset = UNSET
    warnings: list[str] | Unset = UNSET
    metadata: PluginProvisioningOutMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        available = self.available

        provisioned = self.provisioned

        steps: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item = steps_item_data.to_dict()
                steps.append(steps_item)

        env_keys: list[str] | Unset = UNSET
        if not isinstance(self.env_keys, Unset):
            env_keys = self.env_keys

        redacted_env: dict[str, Any] | Unset = UNSET
        if not isinstance(self.redacted_env, Unset):
            redacted_env = self.redacted_env.to_dict()

        outputs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.outputs, Unset):
            outputs = self.outputs.to_dict()

        warnings: list[str] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if available is not UNSET:
            field_dict["available"] = available
        if provisioned is not UNSET:
            field_dict["provisioned"] = provisioned
        if steps is not UNSET:
            field_dict["steps"] = steps
        if env_keys is not UNSET:
            field_dict["env_keys"] = env_keys
        if redacted_env is not UNSET:
            field_dict["redacted_env"] = redacted_env
        if outputs is not UNSET:
            field_dict["outputs"] = outputs
        if warnings is not UNSET:
            field_dict["warnings"] = warnings
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_provision_step_out import PluginProvisionStepOut
        from ..models.plugin_provisioning_out_metadata import (
            PluginProvisioningOutMetadata,
        )
        from ..models.plugin_provisioning_out_outputs import (
            PluginProvisioningOutOutputs,
        )
        from ..models.plugin_provisioning_out_redacted_env import (
            PluginProvisioningOutRedactedEnv,
        )

        d = dict(src_dict)
        available = d.pop("available", UNSET)

        provisioned = d.pop("provisioned", UNSET)

        _steps = d.pop("steps", UNSET)
        steps: list[PluginProvisionStepOut] | Unset = UNSET
        if _steps is not UNSET:
            steps = []
            for steps_item_data in _steps:
                steps_item = PluginProvisionStepOut.from_dict(steps_item_data)

                steps.append(steps_item)

        env_keys = cast(list[str], d.pop("env_keys", UNSET))

        _redacted_env = d.pop("redacted_env", UNSET)
        redacted_env: PluginProvisioningOutRedactedEnv | Unset
        if isinstance(_redacted_env, Unset):
            redacted_env = UNSET
        else:
            redacted_env = PluginProvisioningOutRedactedEnv.from_dict(_redacted_env)

        _outputs = d.pop("outputs", UNSET)
        outputs: PluginProvisioningOutOutputs | Unset
        if isinstance(_outputs, Unset):
            outputs = UNSET
        else:
            outputs = PluginProvisioningOutOutputs.from_dict(_outputs)

        warnings = cast(list[str], d.pop("warnings", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: PluginProvisioningOutMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = PluginProvisioningOutMetadata.from_dict(_metadata)

        plugin_provisioning_out = cls(
            available=available,
            provisioned=provisioned,
            steps=steps,
            env_keys=env_keys,
            redacted_env=redacted_env,
            outputs=outputs,
            warnings=warnings,
            metadata=metadata,
        )

        return plugin_provisioning_out
