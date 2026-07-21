from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.radiance_evaluation_out_status import RadianceEvaluationOutStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.radiance_evaluation_out_artifacts_type_0_item import (
        RadianceEvaluationOutArtifactsType0Item,
    )
    from ..models.radiance_evaluation_out_config import RadianceEvaluationOutConfig
    from ..models.radiance_evaluation_out_error_type_0 import (
        RadianceEvaluationOutErrorType0,
    )
    from ..models.radiance_evaluation_out_links_type_0 import (
        RadianceEvaluationOutLinksType0,
    )
    from ..models.radiance_metrics import RadianceMetrics


T = TypeVar("T", bound="RadianceEvaluationOut")


@_attrs_define
class RadianceEvaluationOut:
    """
    Attributes:
        evaluation_id (str):
        radiance_field_id (str):
        snapshot_seq (int):
        provider (str):
        method (str):
        split (str):
        status (RadianceEvaluationOutStatus):
        config (RadianceEvaluationOutConfig):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        field_links (None | RadianceEvaluationOutLinksType0 | Unset):
        dataset_id (None | str | Unset):
        metrics (None | RadianceMetrics | Unset):
        artifacts (list[RadianceEvaluationOutArtifactsType0Item] | None | Unset):
        error (None | RadianceEvaluationOutErrorType0 | Unset):
        job_id (None | str | Unset):
    """

    evaluation_id: str
    radiance_field_id: str
    snapshot_seq: int
    provider: str
    method: str
    split: str
    status: RadianceEvaluationOutStatus
    config: RadianceEvaluationOutConfig
    created_at: datetime.datetime
    updated_at: datetime.datetime
    field_links: None | RadianceEvaluationOutLinksType0 | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    metrics: None | RadianceMetrics | Unset = UNSET
    artifacts: list[RadianceEvaluationOutArtifactsType0Item] | None | Unset = UNSET
    error: None | RadianceEvaluationOutErrorType0 | Unset = UNSET
    job_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.radiance_evaluation_out_error_type_0 import (
            RadianceEvaluationOutErrorType0,
        )
        from ..models.radiance_evaluation_out_links_type_0 import (
            RadianceEvaluationOutLinksType0,
        )
        from ..models.radiance_metrics import RadianceMetrics

        evaluation_id = self.evaluation_id

        radiance_field_id = self.radiance_field_id

        snapshot_seq = self.snapshot_seq

        provider = self.provider

        method = self.method

        split = self.split

        status = self.status.value

        config = self.config.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_links: dict[str, Any] | None | Unset
        if isinstance(self.field_links, Unset):
            field_links = UNSET
        elif isinstance(self.field_links, RadianceEvaluationOutLinksType0):
            field_links = self.field_links.to_dict()
        else:
            field_links = self.field_links

        dataset_id: None | str | Unset
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        metrics: dict[str, Any] | None | Unset
        if isinstance(self.metrics, Unset):
            metrics = UNSET
        elif isinstance(self.metrics, RadianceMetrics):
            metrics = self.metrics.to_dict()
        else:
            metrics = self.metrics

        artifacts: list[dict[str, Any]] | None | Unset
        if isinstance(self.artifacts, Unset):
            artifacts = UNSET
        elif isinstance(self.artifacts, list):
            artifacts = []
            for artifacts_type_0_item_data in self.artifacts:
                artifacts_type_0_item = artifacts_type_0_item_data.to_dict()
                artifacts.append(artifacts_type_0_item)

        else:
            artifacts = self.artifacts

        error: dict[str, Any] | None | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        elif isinstance(self.error, RadianceEvaluationOutErrorType0):
            error = self.error.to_dict()
        else:
            error = self.error

        job_id: None | str | Unset
        if isinstance(self.job_id, Unset):
            job_id = UNSET
        else:
            job_id = self.job_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "evaluation_id": evaluation_id,
                "radiance_field_id": radiance_field_id,
                "snapshot_seq": snapshot_seq,
                "provider": provider,
                "method": method,
                "split": split,
                "status": status,
                "config": config,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if artifacts is not UNSET:
            field_dict["artifacts"] = artifacts
        if error is not UNSET:
            field_dict["error"] = error
        if job_id is not UNSET:
            field_dict["job_id"] = job_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.radiance_evaluation_out_artifacts_type_0_item import (
            RadianceEvaluationOutArtifactsType0Item,
        )
        from ..models.radiance_evaluation_out_config import RadianceEvaluationOutConfig
        from ..models.radiance_evaluation_out_error_type_0 import (
            RadianceEvaluationOutErrorType0,
        )
        from ..models.radiance_evaluation_out_links_type_0 import (
            RadianceEvaluationOutLinksType0,
        )
        from ..models.radiance_metrics import RadianceMetrics

        d = dict(src_dict)
        evaluation_id = d.pop("evaluation_id")

        radiance_field_id = d.pop("radiance_field_id")

        snapshot_seq = d.pop("snapshot_seq")

        provider = d.pop("provider")

        method = d.pop("method")

        split = d.pop("split")

        status = RadianceEvaluationOutStatus(d.pop("status"))

        config = RadianceEvaluationOutConfig.from_dict(d.pop("config"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        def _parse_field_links(
            data: object,
        ) -> None | RadianceEvaluationOutLinksType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                field_links_type_0 = RadianceEvaluationOutLinksType0.from_dict(data)

                return field_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RadianceEvaluationOutLinksType0 | Unset, data)

        field_links = _parse_field_links(d.pop("_links", UNSET))

        def _parse_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_metrics(data: object) -> None | RadianceMetrics | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metrics_type_0 = RadianceMetrics.from_dict(data)

                return metrics_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RadianceMetrics | Unset, data)

        metrics = _parse_metrics(d.pop("metrics", UNSET))

        def _parse_artifacts(
            data: object,
        ) -> list[RadianceEvaluationOutArtifactsType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                artifacts_type_0 = []
                _artifacts_type_0 = data
                for artifacts_type_0_item_data in _artifacts_type_0:
                    artifacts_type_0_item = (
                        RadianceEvaluationOutArtifactsType0Item.from_dict(
                            artifacts_type_0_item_data
                        )
                    )

                    artifacts_type_0.append(artifacts_type_0_item)

                return artifacts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                list[RadianceEvaluationOutArtifactsType0Item] | None | Unset, data
            )

        artifacts = _parse_artifacts(d.pop("artifacts", UNSET))

        def _parse_error(
            data: object,
        ) -> None | RadianceEvaluationOutErrorType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = RadianceEvaluationOutErrorType0.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RadianceEvaluationOutErrorType0 | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_job_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        job_id = _parse_job_id(d.pop("job_id", UNSET))

        radiance_evaluation_out = cls(
            evaluation_id=evaluation_id,
            radiance_field_id=radiance_field_id,
            snapshot_seq=snapshot_seq,
            provider=provider,
            method=method,
            split=split,
            status=status,
            config=config,
            created_at=created_at,
            updated_at=updated_at,
            field_links=field_links,
            dataset_id=dataset_id,
            metrics=metrics,
            artifacts=artifacts,
            error=error,
            job_id=job_id,
        )

        radiance_evaluation_out.additional_properties = d
        return radiance_evaluation_out

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
