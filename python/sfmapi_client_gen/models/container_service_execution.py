from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.container_service_execution_gpu import ContainerServiceExecutionGpu
from ..models.container_service_execution_log_collection import (
    ContainerServiceExecutionLogCollection,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.container_service_mounts import ContainerServiceMounts
    from ..models.container_service_retry import ContainerServiceRetry


T = TypeVar("T", bound="ContainerServiceExecution")


@_attrs_define
class ContainerServiceExecution:
    """
    Attributes:
        path (str | Unset):  Default: '/execute'.
        timeout_seconds (int | Unset):  Default: 3600.
        mounts (ContainerServiceMounts | Unset):
        gpu (ContainerServiceExecutionGpu | Unset):  Default: ContainerServiceExecutionGpu.OPTIONAL.
        env (list[str] | Unset):
        secrets (list[str] | Unset):
        retry (ContainerServiceRetry | Unset):
        shutdown_timeout_seconds (int | Unset):  Default: 10.
        log_collection (ContainerServiceExecutionLogCollection | Unset):  Default:
            ContainerServiceExecutionLogCollection.BOTH.
        artifact_collection (bool | Unset):  Default: True.
    """

    path: str | Unset = "/execute"
    timeout_seconds: int | Unset = 3600
    mounts: ContainerServiceMounts | Unset = UNSET
    gpu: ContainerServiceExecutionGpu | Unset = ContainerServiceExecutionGpu.OPTIONAL
    env: list[str] | Unset = UNSET
    secrets: list[str] | Unset = UNSET
    retry: ContainerServiceRetry | Unset = UNSET
    shutdown_timeout_seconds: int | Unset = 10
    log_collection: ContainerServiceExecutionLogCollection | Unset = (
        ContainerServiceExecutionLogCollection.BOTH
    )
    artifact_collection: bool | Unset = True

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        timeout_seconds = self.timeout_seconds

        mounts: dict[str, Any] | Unset = UNSET
        if not isinstance(self.mounts, Unset):
            mounts = self.mounts.to_dict()

        gpu: str | Unset = UNSET
        if not isinstance(self.gpu, Unset):
            gpu = self.gpu.value

        env: list[str] | Unset = UNSET
        if not isinstance(self.env, Unset):
            env = self.env

        secrets: list[str] | Unset = UNSET
        if not isinstance(self.secrets, Unset):
            secrets = self.secrets

        retry: dict[str, Any] | Unset = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        shutdown_timeout_seconds = self.shutdown_timeout_seconds

        log_collection: str | Unset = UNSET
        if not isinstance(self.log_collection, Unset):
            log_collection = self.log_collection.value

        artifact_collection = self.artifact_collection

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds
        if mounts is not UNSET:
            field_dict["mounts"] = mounts
        if gpu is not UNSET:
            field_dict["gpu"] = gpu
        if env is not UNSET:
            field_dict["env"] = env
        if secrets is not UNSET:
            field_dict["secrets"] = secrets
        if retry is not UNSET:
            field_dict["retry"] = retry
        if shutdown_timeout_seconds is not UNSET:
            field_dict["shutdown_timeout_seconds"] = shutdown_timeout_seconds
        if log_collection is not UNSET:
            field_dict["log_collection"] = log_collection
        if artifact_collection is not UNSET:
            field_dict["artifact_collection"] = artifact_collection

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_service_mounts import ContainerServiceMounts
        from ..models.container_service_retry import ContainerServiceRetry

        d = dict(src_dict)
        path = d.pop("path", UNSET)

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        _mounts = d.pop("mounts", UNSET)
        mounts: ContainerServiceMounts | Unset
        if isinstance(_mounts, Unset):
            mounts = UNSET
        else:
            mounts = ContainerServiceMounts.from_dict(_mounts)

        _gpu = d.pop("gpu", UNSET)
        gpu: ContainerServiceExecutionGpu | Unset
        if isinstance(_gpu, Unset):
            gpu = UNSET
        else:
            gpu = ContainerServiceExecutionGpu(_gpu)

        env = cast(list[str], d.pop("env", UNSET))

        secrets = cast(list[str], d.pop("secrets", UNSET))

        _retry = d.pop("retry", UNSET)
        retry: ContainerServiceRetry | Unset
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = ContainerServiceRetry.from_dict(_retry)

        shutdown_timeout_seconds = d.pop("shutdown_timeout_seconds", UNSET)

        _log_collection = d.pop("log_collection", UNSET)
        log_collection: ContainerServiceExecutionLogCollection | Unset
        if isinstance(_log_collection, Unset):
            log_collection = UNSET
        else:
            log_collection = ContainerServiceExecutionLogCollection(_log_collection)

        artifact_collection = d.pop("artifact_collection", UNSET)

        container_service_execution = cls(
            path=path,
            timeout_seconds=timeout_seconds,
            mounts=mounts,
            gpu=gpu,
            env=env,
            secrets=secrets,
            retry=retry,
            shutdown_timeout_seconds=shutdown_timeout_seconds,
            log_collection=log_collection,
            artifact_collection=artifact_collection,
        )

        return container_service_execution
