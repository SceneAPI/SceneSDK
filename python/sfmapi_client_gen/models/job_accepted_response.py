from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sim_3 import Sim3


T = TypeVar("T", bound="JobAcceptedResponse")


@_attrs_define
class JobAcceptedResponse:
    """Canonical 202 envelope for endpoints that submit a Job.

    Returned by every ``POST`` that enqueues SfM work — the decomposed
    pipeline stages (``features`` / ``matches`` / ``verify`` / ``map`` /
    ``ba`` / ``triangulate`` / ``relocalize`` / ``pgo`` / ``export`` /
    ``undistort`` / ...), the ``/pipelines/{recipe}`` recipe sugar, the
    ``localize`` / ``georegister`` / ``reconstructions:merge`` /
    ``similarity:build`` / ``artifacts:convert`` stages, and
    backend-native extension actions. Clients should follow
    ``Location`` to ``GET /v1/jobs/{job_id}`` for status.

    Stage-specific optional fields are typed here so SDK codegen can
    surface them as named accessors:

    - ``recon_id`` — endpoints nested under a reconstruction
    - ``dataset_id`` / ``project_id`` — parent-pointer for top-level routes
    - ``method`` — optional stage/backend method selector echoed by
      submitters that accept one
    - ``applied_sim3`` — georegister applied transform
    - ``target_recon_id`` / ``source_recon_ids`` — ``reconstructions:merge``
    - ``strategy`` — ``similarity:build``
    - ``action_id`` / ``backend`` — backend-native extension actions
    - ``provider`` — sfm_hub provider id selected for execution (echoed
      from the request so clients can confirm routing)
    - ``artifact_id`` / ``target_format`` — ``artifacts:convert`` echoes
      the source artifact and the chosen conversion target format

        Attributes:
            job_id (str):
            task_ids (list[str] | Unset):
            recon_id (None | str | Unset):
            dataset_id (None | str | Unset):
            project_id (None | str | Unset):
            method (None | str | Unset):
            applied_sim3 (None | Sim3 | Unset):
            target_recon_id (None | str | Unset):
            source_recon_ids (list[str] | None | Unset):
            strategy (None | str | Unset):
            action_id (None | str | Unset):
            backend (None | str | Unset):
            provider (None | str | Unset):
            artifact_id (None | str | Unset):
            target_format (None | str | Unset):
            radiance_field_id (None | str | Unset):
            radiance_evaluation_id (None | str | Unset):
    """

    job_id: str
    task_ids: list[str] | Unset = UNSET
    recon_id: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    project_id: None | str | Unset = UNSET
    method: None | str | Unset = UNSET
    applied_sim3: None | Sim3 | Unset = UNSET
    target_recon_id: None | str | Unset = UNSET
    source_recon_ids: list[str] | None | Unset = UNSET
    strategy: None | str | Unset = UNSET
    action_id: None | str | Unset = UNSET
    backend: None | str | Unset = UNSET
    provider: None | str | Unset = UNSET
    artifact_id: None | str | Unset = UNSET
    target_format: None | str | Unset = UNSET
    radiance_field_id: None | str | Unset = UNSET
    radiance_evaluation_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sim_3 import Sim3

        job_id = self.job_id

        task_ids: list[str] | Unset = UNSET
        if not isinstance(self.task_ids, Unset):
            task_ids = self.task_ids

        recon_id: None | str | Unset
        if isinstance(self.recon_id, Unset):
            recon_id = UNSET
        else:
            recon_id = self.recon_id

        dataset_id: None | str | Unset
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        method: None | str | Unset
        if isinstance(self.method, Unset):
            method = UNSET
        else:
            method = self.method

        applied_sim3: dict[str, Any] | None | Unset
        if isinstance(self.applied_sim3, Unset):
            applied_sim3 = UNSET
        elif isinstance(self.applied_sim3, Sim3):
            applied_sim3 = self.applied_sim3.to_dict()
        else:
            applied_sim3 = self.applied_sim3

        target_recon_id: None | str | Unset
        if isinstance(self.target_recon_id, Unset):
            target_recon_id = UNSET
        else:
            target_recon_id = self.target_recon_id

        source_recon_ids: list[str] | None | Unset
        if isinstance(self.source_recon_ids, Unset):
            source_recon_ids = UNSET
        elif isinstance(self.source_recon_ids, list):
            source_recon_ids = self.source_recon_ids

        else:
            source_recon_ids = self.source_recon_ids

        strategy: None | str | Unset
        if isinstance(self.strategy, Unset):
            strategy = UNSET
        else:
            strategy = self.strategy

        action_id: None | str | Unset
        if isinstance(self.action_id, Unset):
            action_id = UNSET
        else:
            action_id = self.action_id

        backend: None | str | Unset
        if isinstance(self.backend, Unset):
            backend = UNSET
        else:
            backend = self.backend

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        artifact_id: None | str | Unset
        if isinstance(self.artifact_id, Unset):
            artifact_id = UNSET
        else:
            artifact_id = self.artifact_id

        target_format: None | str | Unset
        if isinstance(self.target_format, Unset):
            target_format = UNSET
        else:
            target_format = self.target_format

        radiance_field_id: None | str | Unset
        if isinstance(self.radiance_field_id, Unset):
            radiance_field_id = UNSET
        else:
            radiance_field_id = self.radiance_field_id

        radiance_evaluation_id: None | str | Unset
        if isinstance(self.radiance_evaluation_id, Unset):
            radiance_evaluation_id = UNSET
        else:
            radiance_evaluation_id = self.radiance_evaluation_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
            }
        )
        if task_ids is not UNSET:
            field_dict["task_ids"] = task_ids
        if recon_id is not UNSET:
            field_dict["recon_id"] = recon_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if method is not UNSET:
            field_dict["method"] = method
        if applied_sim3 is not UNSET:
            field_dict["applied_sim3"] = applied_sim3
        if target_recon_id is not UNSET:
            field_dict["target_recon_id"] = target_recon_id
        if source_recon_ids is not UNSET:
            field_dict["source_recon_ids"] = source_recon_ids
        if strategy is not UNSET:
            field_dict["strategy"] = strategy
        if action_id is not UNSET:
            field_dict["action_id"] = action_id
        if backend is not UNSET:
            field_dict["backend"] = backend
        if provider is not UNSET:
            field_dict["provider"] = provider
        if artifact_id is not UNSET:
            field_dict["artifact_id"] = artifact_id
        if target_format is not UNSET:
            field_dict["target_format"] = target_format
        if radiance_field_id is not UNSET:
            field_dict["radiance_field_id"] = radiance_field_id
        if radiance_evaluation_id is not UNSET:
            field_dict["radiance_evaluation_id"] = radiance_evaluation_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sim_3 import Sim3

        d = dict(src_dict)
        job_id = d.pop("job_id")

        task_ids = cast(list[str], d.pop("task_ids", UNSET))

        def _parse_recon_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recon_id = _parse_recon_id(d.pop("recon_id", UNSET))

        def _parse_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_method(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        method = _parse_method(d.pop("method", UNSET))

        def _parse_applied_sim3(data: object) -> None | Sim3 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                applied_sim3_type_0 = Sim3.from_dict(data)

                return applied_sim3_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Sim3 | Unset, data)

        applied_sim3 = _parse_applied_sim3(d.pop("applied_sim3", UNSET))

        def _parse_target_recon_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_recon_id = _parse_target_recon_id(d.pop("target_recon_id", UNSET))

        def _parse_source_recon_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                source_recon_ids_type_0 = cast(list[str], data)

                return source_recon_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        source_recon_ids = _parse_source_recon_ids(d.pop("source_recon_ids", UNSET))

        def _parse_strategy(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        strategy = _parse_strategy(d.pop("strategy", UNSET))

        def _parse_action_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        action_id = _parse_action_id(d.pop("action_id", UNSET))

        def _parse_backend(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        backend = _parse_backend(d.pop("backend", UNSET))

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        def _parse_artifact_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        artifact_id = _parse_artifact_id(d.pop("artifact_id", UNSET))

        def _parse_target_format(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_format = _parse_target_format(d.pop("target_format", UNSET))

        def _parse_radiance_field_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        radiance_field_id = _parse_radiance_field_id(d.pop("radiance_field_id", UNSET))

        def _parse_radiance_evaluation_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        radiance_evaluation_id = _parse_radiance_evaluation_id(
            d.pop("radiance_evaluation_id", UNSET)
        )

        job_accepted_response = cls(
            job_id=job_id,
            task_ids=task_ids,
            recon_id=recon_id,
            dataset_id=dataset_id,
            project_id=project_id,
            method=method,
            applied_sim3=applied_sim3,
            target_recon_id=target_recon_id,
            source_recon_ids=source_recon_ids,
            strategy=strategy,
            action_id=action_id,
            backend=backend,
            provider=provider,
            artifact_id=artifact_id,
            target_format=target_format,
            radiance_field_id=radiance_field_id,
            radiance_evaluation_id=radiance_evaluation_id,
        )

        job_accepted_response.additional_properties = d
        return job_accepted_response

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
