from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.torch_runtime_device import TorchRuntimeDevice
from ..models.torch_runtime_policy import TorchRuntimePolicy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.torch_runtime_install_env import TorchRuntimeInstallEnv


T = TypeVar("T", bound="TorchRuntime")


@_attrs_define
class TorchRuntime:
    """
    Attributes:
        policy (TorchRuntimePolicy | Unset):  Default: TorchRuntimePolicy.RECOMMENDED.
        device (TorchRuntimeDevice | Unset):  Default: TorchRuntimeDevice.CUDA.
        index_url (str | Unset):  Default: 'https://download.pytorch.org/whl/cu128'.
        cpu_index_url (str | Unset):  Default: 'https://download.pytorch.org/whl/cpu'.
        packages (list[str] | Unset):
        install_env (TorchRuntimeInstallEnv | Unset):
    """

    policy: TorchRuntimePolicy | Unset = TorchRuntimePolicy.RECOMMENDED
    device: TorchRuntimeDevice | Unset = TorchRuntimeDevice.CUDA
    index_url: str | Unset = "https://download.pytorch.org/whl/cu128"
    cpu_index_url: str | Unset = "https://download.pytorch.org/whl/cpu"
    packages: list[str] | Unset = UNSET
    install_env: TorchRuntimeInstallEnv | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        policy: str | Unset = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.value

        device: str | Unset = UNSET
        if not isinstance(self.device, Unset):
            device = self.device.value

        index_url = self.index_url

        cpu_index_url = self.cpu_index_url

        packages: list[str] | Unset = UNSET
        if not isinstance(self.packages, Unset):
            packages = self.packages

        install_env: dict[str, Any] | Unset = UNSET
        if not isinstance(self.install_env, Unset):
            install_env = self.install_env.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if policy is not UNSET:
            field_dict["policy"] = policy
        if device is not UNSET:
            field_dict["device"] = device
        if index_url is not UNSET:
            field_dict["index_url"] = index_url
        if cpu_index_url is not UNSET:
            field_dict["cpu_index_url"] = cpu_index_url
        if packages is not UNSET:
            field_dict["packages"] = packages
        if install_env is not UNSET:
            field_dict["install_env"] = install_env

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.torch_runtime_install_env import TorchRuntimeInstallEnv

        d = dict(src_dict)
        _policy = d.pop("policy", UNSET)
        policy: TorchRuntimePolicy | Unset
        if isinstance(_policy, Unset):
            policy = UNSET
        else:
            policy = TorchRuntimePolicy(_policy)

        _device = d.pop("device", UNSET)
        device: TorchRuntimeDevice | Unset
        if isinstance(_device, Unset):
            device = UNSET
        else:
            device = TorchRuntimeDevice(_device)

        index_url = d.pop("index_url", UNSET)

        cpu_index_url = d.pop("cpu_index_url", UNSET)

        packages = cast(list[str], d.pop("packages", UNSET))

        _install_env = d.pop("install_env", UNSET)
        install_env: TorchRuntimeInstallEnv | Unset
        if isinstance(_install_env, Unset):
            install_env = UNSET
        else:
            install_env = TorchRuntimeInstallEnv.from_dict(_install_env)

        torch_runtime = cls(
            policy=policy,
            device=device,
            index_url=index_url,
            cpu_index_url=cpu_index_url,
            packages=packages,
            install_env=install_env,
        )

        return torch_runtime
