"""SDK tests using respx to mock httpx.

We only assert the SDK's request shape and response parsing; the server
contract itself is covered by the sfmapi tests.
"""

from __future__ import annotations

import hashlib
import json

import pytest
import respx
from httpx import Response
from pydantic import ValidationError as PydanticValidationError
from sfmapi_client import (
    AsyncSfmApiClient,
    AttributesContractOut,
    BackendUnavailableError,
    BundleAdjustmentSpec,
    CapabilityUnavailableError,
    DataTypesContractOut,
    Dataset,
    FeaturesSpec,
    Image,
    IncrementalSpec,
    Job,
    JobDetail,
    NotFoundError,
    OperationsContractOut,
    PipelineRunRequest,
    PipelineValidateRequest,
    PipelinesContractOut,
    ProcessorsContractOut,
    Project,
    ProjectCreate,
    Reconstruction,
    PycolmapUnavailableError,
    SfmApiClient,
    SfmApiError,
    SubModel,
    ValidationError,
)
from sceneapi_client_gen import Client
from sceneapi_client_gen import errors as generated_errors
from sceneapi_client_gen._ergonomics import SfmApiError as GeneratedSfmApiError
from sceneapi_client_gen._ergonomics import NotFoundError as GeneratedNotFoundError
from sceneapi_client_gen._ergonomics import raise_for_status
from sceneapi_client_gen.api.projects import get_v1_projects_project_id_get as get_project
from sceneapi_client_gen.models import ArtifactConversionPlanRequest, ArtifactConvertRequest
from sfmapi_client.models import JobSubmitResponse, Sim3
from sfmapi_client.models import (
    ArtifactConversionPlanRequest as LegacyArtifactConversionPlanRequest,
)
from sfmapi_client.models import ArtifactConvertRequest as LegacyArtifactConvertRequest
from sfmapi_client.models import ArtifactFileRef as LegacyArtifactFileRef
from sfmapi_client.models import ArtifactImportRequest as LegacyArtifactImportRequest

BASE = "http://api.test"


def _project_payload(name: str = "p") -> dict:
    return {
        "project_id": "01" * 13,
        "tenant_id": "default",
        "name": name,
        "description": None,
        "created_at": "2026-05-02T00:00:00Z",
    }


def _dataset_payload(name: str = "dataset") -> dict:
    return {
        "dataset_id": "D" * 26,
        "tenant_id": "default",
        "project_id": "P" * 26,
        "source_id": "S" * 26,
        "name": name,
        "camera_model": "SIMPLE_RADIAL",
        "intrinsics_mode": "single_camera",
        "is_spherical": False,
        "respect_exif_orientation": False,
        "rig_config_json": None,
        "active_maskset_id": None,
        "manifest_hash": "h",
        "created_at": "2026-05-02T00:00:00Z",
    }


def _stage_artifact_payload(artifact_id: str = "ART") -> dict:
    return {
        "artifact_id": artifact_id,
        "job_id": "JOB",
        "task_id": "TASK",
        "recon_id": "RECON",
        "dataset_id": None,
        "kind": "features.local.v1",
        "name": "features.json",
        "uri": "https://artifacts.example/features.json",
        "media_type": "application/json",
        "artifact_format": "sfmapi.features.local.v1",
        "datatype": "feature_set",
        "schema_version": 1,
        "files": [],
        "sha256": None,
        "byte_size": None,
        "coordinate_frame": None,
        "producer": None,
        "summary": None,
        "metadata": {},
        "created_at": "2026-05-02T00:00:00Z",
        "_links": {"self": {"href": f"/v1/artifacts/{artifact_id}"}},
    }


def _submodel_payload() -> dict:
    return {
        "submodel_id": "S" * 26,
        "recon_id": "R" * 26,
        "idx": 0,
        "parent_submodel_id": None,
        "summary": None,
        "rigidity": None,
        "snapshot_seq": 1,
        "sealed_path": None,
        "created_at": "2026-05-02T00:00:00Z",
    }


def _image_payload() -> dict:
    return {
        "image_id": "I" * 26,
        "dataset_id": "D" * 26,
        "name": "a.jpg",
        "content_sha": "0" * 64,
        "source_kind": "upload",
        "rel_path": None,
        "byte_size": 5,
        "width": None,
        "height": None,
        "created_at": "2026-05-02T00:00:00Z",
    }


def _job_payload() -> dict:
    return {
        "job_id": "J" * 26,
        "tenant_id": "default",
        "project_id": "P" * 26,
        "recipe": "incremental",
        "status": "pending",
        "cancel_requested": False,
        "cancel_force": False,
        "created_at": "2026-05-02T00:00:00Z",
    }


def _reconstruction_payload() -> dict:
    return {
        "recon_id": "R" * 26,
        "project_id": "P" * 26,
        "dataset_id": "D" * 26,
        "dataset_snapshot_hash": "snapshot",
        "spec": {"kind": "incremental"},
        "rv_id": "rv",
        "status": "pending",
        "created_at": "2026-05-02T00:00:00Z",
    }


@pytest.mark.parametrize(
    ("model", "payload"),
    [
        (
            Project,
            {
                **_project_payload(),
                "updated_at": "2026-05-03T00:00:00Z",
            },
        ),
        (
            Dataset,
            {
                **_dataset_payload(),
                "updated_at": "2026-05-03T00:00:00Z",
            },
        ),
        (Image, _image_payload()),
        (Job, _job_payload()),
        (Reconstruction, _reconstruction_payload()),
        (SubModel, _submodel_payload()),
    ],
)
def test_handwritten_resource_models_preserve_links_and_ignore_unknown_fields(
    model: type[object],
    payload: dict[str, object],
) -> None:
    linked = {
        **payload,
        "_links": {"self": {"href": "/v1/resource/id"}, "content": None},
    }
    parsed = model.model_validate(linked)  # type: ignore[attr-defined]

    assert parsed.links["self"].href == "/v1/resource/id"  # type: ignore[attr-defined]
    assert parsed.links["content"] is None  # type: ignore[attr-defined]
    parsed_with_extra = model.model_validate(  # type: ignore[attr-defined]
        {**linked, "unexpected_contract_field": True}
    )
    assert not hasattr(parsed_with_extra, "unexpected_contract_field")


def test_handwritten_request_models_still_forbid_unknown_fields() -> None:
    with pytest.raises(PydanticValidationError):
        ProjectCreate.model_validate({"name": "p", "unexpected_contract_field": True})


@respx.mock
def test_sync_create_project_sets_auth_header() -> None:
    route = respx.post(f"{BASE}/v1/projects").mock(
        return_value=Response(201, json=_project_payload("alpha"))
    )
    with SfmApiClient(BASE, api_key="sfm_test") as c:
        p = c.create_project("alpha")
    assert p.name == "alpha"
    assert route.calls.last.request.headers["Authorization"] == "Bearer sfm_test"
    assert route.calls.last.request.read() != b""  # body sent


@respx.mock
def test_sync_create_api_key_sends_current_body_and_parses_response() -> None:
    route = respx.post(f"{BASE}/v1/admin/api-keys").mock(
        return_value=Response(
            201,
            json={
                "raw_key": "sfm_secret",
                "api_key_id": "key-1",
                "tenant_id": "tenant-1",
                "name": "ci",
            },
        )
    )
    with SfmApiClient(BASE) as c:
        key = c.create_api_key_for_tenant(tenant_id="tenant-1", name="ci")

    assert key.raw_key == "sfm_secret"
    assert key.name == "ci"
    assert key.revoked is False
    assert json.loads(route.calls.last.request.content) == {
        "tenant_id": "tenant-1",
        "name": "ci",
    }


@respx.mock
def test_sync_create_api_key_compat_defaults_tenant() -> None:
    route = respx.post(f"{BASE}/v1/admin/api-keys").mock(
        return_value=Response(
            201,
            json={
                "raw_key": "sfm_secret",
                "api_key_id": "key-1",
                "tenant_id": "default",
                "name": "ci",
            },
        )
    )
    with SfmApiClient(BASE) as c:
        key = c.create_api_key("ci")

    assert key.tenant_id == "default"
    assert json.loads(route.calls.last.request.content) == {
        "tenant_id": "default",
        "name": "ci",
    }


@respx.mock
def test_sync_create_api_key_legacy_label_keyword() -> None:
    route = respx.post(f"{BASE}/v1/admin/api-keys").mock(
        return_value=Response(
            201,
            json={
                "raw_key": "sfm_secret",
                "api_key_id": "key-1",
                "tenant_id": "default",
                "name": "ci",
            },
        )
    )
    with SfmApiClient(BASE) as c:
        key = c.create_api_key(label="ci")

    assert key.label == "ci"
    assert json.loads(route.calls.last.request.content) == {
        "tenant_id": "default",
        "name": "ci",
    }


@respx.mock
def test_sync_list_api_keys_preserves_legacy_label_response() -> None:
    respx.get(f"{BASE}/v1/admin/api-keys").mock(
        return_value=Response(
            200,
            json=[
                {
                    "api_key_id": "key-1",
                    "tenant_id": "default",
                    "name": None,
                    "label": "ci",
                    "revoked": False,
                }
            ],
        )
    )
    with SfmApiClient(BASE) as c:
        key = c.list_api_keys()[0]

    assert key.name == "ci"
    assert key.label == "ci"


@respx.mock
def test_sync_dense_mesh_helpers_fail_before_request() -> None:
    with SfmApiClient(BASE) as c:
        with pytest.raises(NotImplementedError, match="out of scope"):
            c.submit_dense("R" * 26)
        with pytest.raises(NotImplementedError, match="out of scope"):
            c.submit_mesh("R" * 26)
        with pytest.raises(NotImplementedError, match="out of scope"):
            c.read_dense_index("R" * 26, 1)
        with pytest.raises(NotImplementedError, match="out of scope"):
            c.read_mesh_ply("R" * 26, 1)
    assert not respx.calls


@respx.mock
def test_sync_404_raises_not_found() -> None:
    respx.get(f"{BASE}/v1/projects/missing").mock(
        return_value=Response(
            404,
            json={
                "type": "https://sfmapi/errors/not_found",
                "title": "Resource not found",
                "status": 404,
                "detail": "Project missing not found",
            },
            headers={"content-type": "application/problem+json"},
        )
    )
    with SfmApiClient(BASE) as c, pytest.raises(NotFoundError) as ei:
        c.get_project("missing")
    assert ei.value.status_code == 404
    assert "missing" in str(ei.value)


@respx.mock
def test_sync_list_datasets_parses_page_envelope_and_sends_params() -> None:
    route = respx.get(f"{BASE}/v1/projects/PR/datasets").mock(
        return_value=Response(
            200,
            json={"items": [_dataset_payload()], "next_page_token": "next"},
        )
    )
    with SfmApiClient(BASE) as c:
        default_page = c.list_datasets_page("PR")
        page = c.list_datasets_page("PR", page_size=7, page_token="tok")
        items = c.list_datasets("PR", page_size=7, page_token="tok")

    assert default_page.items[0].name == "dataset"
    assert page.next_page_token == "next"
    assert page.items[0].name == "dataset"
    assert items[0].name == "dataset"
    assert route.calls[0].request.url.params["page_size"] == "100"
    assert route.calls.last.request.url.params["page_size"] == "7"
    assert route.calls.last.request.url.params["page_token"] == "tok"


@respx.mock
def test_sync_list_submodels_parses_page_envelope_and_sends_params() -> None:
    route = respx.get(f"{BASE}/v1/reconstructions/REC/submodels").mock(
        return_value=Response(
            200,
            json={"items": [_submodel_payload()], "next_page_token": "next"},
        )
    )
    with SfmApiClient(BASE) as c:
        default_page = c.list_submodels_page("REC")
        page = c.list_submodels_page("REC", page_size=2, page_token="tok")
        items = c.list_submodels("REC", page_size=2, page_token="tok")

    assert default_page.items[0].submodel_id == "S" * 26
    assert page.next_page_token == "next"
    assert page.items[0].submodel_id == "S" * 26
    assert items[0].submodel_id == "S" * 26
    assert route.calls[0].request.url.params["page_size"] == "100"
    assert route.calls.last.request.url.params["page_size"] == "2"
    assert route.calls.last.request.url.params["page_token"] == "tok"


@respx.mock
def test_sync_upload_bytes_full_handshake() -> None:
    payload = b"\xff\xd8\xff\xe0" + b"x" * 256
    sha = hashlib.sha256(payload).hexdigest()

    init = respx.post(f"{BASE}/v1/uploads").mock(
        return_value=Response(
            201,
            json={
                "upload_id": "U1" * 13,
                "state": "open",
                "expected_size": len(payload),
                "received_bytes": 0,
                "blob_sha": None,
                "expires_at": "2026-05-03T00:00:00Z",
            },
        )
    )
    patch = respx.patch(f"{BASE}/v1/uploads/{'U1' * 13}").mock(
        return_value=Response(
            200,
            json={
                "upload_id": "U1" * 13,
                "state": "received",
                "expected_size": len(payload),
                "received_bytes": len(payload),
                "blob_sha": None,
                "expires_at": "2026-05-03T00:00:00Z",
            },
        )
    )
    finalize = respx.post(f"{BASE}/v1/uploads/{'U1' * 13}:finalize").mock(
        return_value=Response(
            200,
            json={
                "upload_id": "U1" * 13,
                "state": "finalized",
                "expected_size": len(payload),
                "received_bytes": len(payload),
                "blob_sha": sha,
                "expires_at": "2026-05-03T00:00:00Z",
            },
        )
    )

    with SfmApiClient(BASE) as c:
        result = c.upload_bytes(payload, chunk_size=8)
    assert result == sha
    assert init.called
    assert patch.called
    assert finalize.called

    init_req = init.calls.last.request
    body = init_req.read().decode()
    assert f'"expected_size":{len(payload)}' in body.replace(" ", "")
    assert sha in body  # client passes the precomputed sha
    assert [call.request.headers["Content-Range"] for call in patch.calls] == [
        f"bytes {start}-{min(start + 8, len(payload)) - 1}/{len(payload)}"
        for start in range(0, len(payload), 8)
    ]


@respx.mock
def test_sync_upload_bytes_rejects_server_sha_mismatch() -> None:
    payload = b"abcdef"
    sha = hashlib.sha256(payload).hexdigest()

    respx.post(f"{BASE}/v1/uploads").mock(
        return_value=Response(
            201,
            json={
                "upload_id": "U2" * 13,
                "state": "open",
                "expected_size": len(payload),
                "received_bytes": 0,
                "blob_sha": None,
                "expires_at": "2026-05-03T00:00:00Z",
            },
        )
    )
    respx.patch(f"{BASE}/v1/uploads/{'U2' * 13}").mock(
        return_value=Response(
            200,
            json={
                "upload_id": "U2" * 13,
                "state": "received",
                "expected_size": len(payload),
                "received_bytes": len(payload),
                "blob_sha": None,
                "expires_at": "2026-05-03T00:00:00Z",
            },
        )
    )
    respx.post(f"{BASE}/v1/uploads/{'U2' * 13}:finalize").mock(
        return_value=Response(
            200,
            json={
                "upload_id": "U2" * 13,
                "state": "finalized",
                "expected_size": len(payload),
                "received_bytes": len(payload),
                "blob_sha": "0" * 64,
                "expires_at": "2026-05-03T00:00:00Z",
            },
        )
    )

    with SfmApiClient(BASE) as c, pytest.raises(SfmApiError, match=sha):
        c.upload_bytes(payload, chunk_size=3)


@respx.mock
def test_run_pipeline_routes_to_kind_path() -> None:
    job = {
        "job_id": "JJ" * 13,
        "task_ids": ["T1" * 13, "T2" * 13, "T3" * 13, "T4" * 13],
        "recon_id": "R1" * 13,
    }
    route = respx.post(f"{BASE}/v1/projects/PR/pipelines/incremental").mock(
        return_value=Response(202, json=job)
    )
    with SfmApiClient(BASE) as c:
        result = c.run_pipeline(
            "PR",
            dataset_id="DS",
            spec=IncrementalSpec(),
            features=FeaturesSpec(use_gpu=False),
        )
    assert result.recon_id == "R1" * 13
    assert len(result.task_ids) == 4
    body = route.calls.last.request.read().decode()
    assert '"kind":"incremental"' in body.replace(" ", "")


@respx.mock
def test_validate_pipeline_routes_to_typed_preflight() -> None:
    route = respx.post(f"{BASE}/v1/pipelines:validate").mock(
        return_value=Response(200, json={"valid": True, "errors": []})
    )
    with SfmApiClient(BASE) as c:
        _ = PipelineValidateRequest(steps=[{"processor": "features"}])
        result = c.validate_pipeline({"steps": [{"processor": "features"}]})
    assert result.valid is True
    assert route.calls.call_count == 1
    body = json.loads(route.calls.last.request.read())
    assert body == {"steps": [{"processor": "features"}]}


@respx.mock
def test_validate_pipeline_model_uses_server_default_initial_inputs() -> None:
    route = respx.post(f"{BASE}/v1/pipelines:validate").mock(
        return_value=Response(200, json={"valid": True, "errors": []})
    )
    with SfmApiClient(BASE) as c:
        result = c.validate_pipeline(
            PipelineValidateRequest(steps=["features"])
        )
    assert result.valid is True
    body = json.loads(route.calls.last.request.read())
    assert body == {
        "initial_inputs": ["image_sequence"],
        "steps": ["features"],
    }


@respx.mock
def test_run_typed_pipeline_routes_to_processor_run() -> None:
    job = {
        "job_id": "JY" * 13,
        "task_ids": ["TY" * 13],
        "recon_id": "RY" * 13,
    }
    route = respx.post(f"{BASE}/v1/projects/PR/pipelines:run").mock(
        return_value=Response(202, json=job)
    )
    with SfmApiClient(BASE) as c:
        _ = PipelineRunRequest(dataset_id="DS", steps=["features", "pairs"])
        result = c.run_typed_pipeline(
            "PR",
            {"dataset_id": "DS", "steps": ["features", "pairs"]},
        )
    assert result.recon_id == "RY" * 13
    body = json.loads(route.calls.last.request.read())
    assert body == {
        "dataset_id": "DS",
        "steps": ["features", "pairs"],
    }


@respx.mock
def test_run_typed_pipeline_model_uses_server_default_initial_inputs() -> None:
    route = respx.post(f"{BASE}/v1/projects/PR/pipelines:run").mock(
        return_value=Response(
            202,
            json={"job_id": "JY" * 13, "task_ids": ["TY" * 13], "recon_id": "RY" * 13},
        )
    )
    with SfmApiClient(BASE) as c:
        c.run_typed_pipeline(
            "PR",
            PipelineRunRequest(dataset_id="DS", steps=["features", "pairs"]),
        )
    body = json.loads(route.calls.last.request.read())
    assert body == {
        "dataset_id": "DS",
        "initial_inputs": ["image_sequence"],
        "steps": ["features", "pairs"],
    }


def test_job_detail_task_preserves_provider_and_outputs_ref() -> None:
    detail = JobDetail.model_validate(
        {
            **_job_payload(),
            "status": "succeeded",
            "tasks": [
                {
                    "task_id": "T" * 26,
                    "job_id": "J" * 26,
                    "kind": "features",
                    "status": "skipped",
                    "provider": "hloc",
                    "cache_key": "c" * 64,
                    "inputs_hash": "i" * 64,
                    "params_hash": "p" * 64,
                    "outputs_ref": {"num_keypoints": 12},
                }
            ],
            "events": [],
        }
    )
    assert detail.tasks[0].provider == "hloc"
    assert detail.tasks[0].outputs_ref == {"num_keypoints": 12}


def test_job_submit_response_preserves_accepted_response_metadata() -> None:
    response = JobSubmitResponse.model_validate(
        {
            "job_id": "JOB",
            "task_ids": ["TASK"],
            "recon_id": "RECON",
            "dataset_id": "DATASET",
            "project_id": "PROJECT",
            "method": "stub",
            "provider": "gsplat",
            "artifact_id": "ARTIFACT",
            "target_format": "sfmapi.radiance.3dgs.v1",
            "radiance_field_id": "FIELD",
            "radiance_evaluation_id": "EVAL",
            "source_recon_ids": ["SRC1", "SRC2"],
            "target_recon_id": "TARGET",
            "strategy": "dhash",
            "action_id": "hloc.extractFeatures",
            "backend": "hloc",
            "applied_sim3": {
                "rotation": {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0},
                "translation": [1.0, 2.0, 3.0],
                "scale": 1.0,
            },
        }
    )

    assert response.provider == "gsplat"
    assert response.artifact_id == "ARTIFACT"
    assert response.target_format == "sfmapi.radiance.3dgs.v1"
    assert response.radiance_field_id == "FIELD"
    assert response.radiance_evaluation_id == "EVAL"
    assert response.source_recon_ids == ["SRC1", "SRC2"]
    assert isinstance(response.applied_sim3, Sim3)
    assert response.applied_sim3.scale == 1.0
    assert response.applied_sim3.translation == (1.0, 2.0, 3.0)


@respx.mock
def test_typed_dataflow_discovery_helpers_route() -> None:
    routes = {
        "/v1/attributes": {
            "contract": "attributes",
            "contract_schema_version": 1,
            "attribute_types": ["str"],
            "rules": {"enum": "optional"},
        },
        "/v1/datatypes": {
            "contract": "datatypes",
            "contract_schema_version": 1,
            "kinds": ["logical"],
            "types": [
                {
                    "type_id": "feature_set",
                    "title": "Feature Set",
                    "kind": "logical",
                    "aliases": [],
                    "description": "",
                }
            ],
        },
        "/v1/operations": {
            "contract": "operations",
            "contract_schema_version": 1,
            "operations": [
                {
                    "op_id": "features",
                    "title": "Features",
                    "consumes": [],
                    "produces": ["feature_set"],
                    "capabilities": [],
                    "config_stage": "features",
                    "description": "",
                }
            ],
            "compatibility": {"features": "features"},
        },
        "/v1/processors": {
            "contract": "processors",
            "contract_schema_version": 1,
            "processors": [
                {
                    "processor_id": "features",
                    "title": "Features",
                    "consumer": {},
                    "supplier": {
                        "features": {
                            "datatype": "feature_set",
                            "required": True,
                            "multiple": False,
                            "description": "",
                        }
                    },
                    "attributes": [],
                    "special_inputs": {},
                    "special_attributes": [],
                    "capabilities": [],
                    "config_stage": "features",
                    "aliases": [],
                    "description": "",
                }
            ],
            "rules": {"composition": "datatype_match"},
        },
        "/v1/pipelines": {
            "contract": "pipelines",
            "contract_schema_version": 1,
            "composition_rule": "supplier.datatype == consumer.datatype",
            "initial_inputs": ["images"],
            "canonical_pipelines": {"incremental": ["features"]},
            "plugin_pipelines": [
                {
                    "pipeline_id": "incremental",
                    "title": "Incremental",
                    "aliases": [],
                    "initial_inputs": ["images"],
                    "steps": [
                        {
                            "ref": "features",
                            "processor": "features",
                            "attributes": {},
                            "wires": {},
                        }
                    ],
                    "description": "",
                }
            ],
            "step_schema": {"type": "object"},
            "validation_reasons": ["unknown_processor"],
        },
    }
    mocked_routes = [
        respx.get(f"{BASE}{path}").mock(return_value=Response(200, json=payload))
        for path, payload in routes.items()
    ]

    with SfmApiClient(BASE) as c:
        assert c.list_attributes().attribute_types == ["str"]
        assert c.list_datatypes().types[0].type_id == "feature_set"
        assert c.list_operations().operations[0].op_id == "features"
        assert c.list_processors().processors[0].supplier["features"].datatype == "feature_set"
        assert c.list_pipelines().canonical_pipelines["incremental"] == ["features"]

    for route in mocked_routes:
        assert route.calls.call_count == 1


@respx.mock
def test_artifact_helpers_route_and_parse() -> None:
    artifact = _stage_artifact_payload()
    respx.get(f"{BASE}/v1/artifacts/kinds").mock(
        return_value=Response(
            200,
            json={
                "items": [
                    {
                        "kind": "features.local.v1",
                        "datatype": "feature_set",
                        "title": "Features",
                        "description": "Local features",
                        "durable": True,
                        "artifact_format": "sfmapi.features.local.v1",
                        "schema_version": 1,
                    }
                ],
                "next_page_token": None,
            },
        )
    )
    respx.get(f"{BASE}/v1/artifacts/formats").mock(
        return_value=Response(
            200,
            json={
                "items": [
                    {
                        "format_id": "sfmapi.features.local.v1",
                        "datatype": "feature_set",
                        "title": "Features",
                        "description": "Local features",
                        "schema_version": 1,
                        "media_types": ["application/json"],
                    }
                ],
                "next_page_token": None,
            },
        )
    )
    import_route = respx.post(f"{BASE}/v1/artifacts:import").mock(
        return_value=Response(201, json=artifact)
    )
    respx.get(f"{BASE}/v1/artifacts/ART").mock(return_value=Response(200, json=artifact))
    plan_route = respx.post(f"{BASE}/v1/artifacts/ART:conversionPlan").mock(
        return_value=Response(
            200,
            json={
                "artifact_id": "ART",
                "source_format": "provider.native",
                "target_format": "sfmapi.features.local.v1",
                "conversion_required": True,
                "executable": True,
                "steps": [
                    {
                        "from_format": "provider.native",
                        "to_format": "sfmapi.features.local.v1",
                        "lossless": True,
                    }
                ],
            },
        )
    )
    convert_route = respx.post(f"{BASE}/v1/artifacts/ART:convert").mock(
        return_value=Response(
            202,
            json={
                "job_id": "JOB",
                "task_ids": ["TASK"],
                "artifact_id": "ART",
                "target_format": "sfmapi.features.local.v1",
            },
        )
    )
    respx.post(f"{BASE}/v1/artifacts/ART:validate").mock(
        return_value=Response(
            200,
            json={
                "artifact_id": "ART",
                "valid": True,
                "artifact_format": "sfmapi.features.local.v1",
                "datatype": "feature_set",
                "checked_content": False,
                "issues": [],
            },
        )
    )
    job_route = respx.get(f"{BASE}/v1/jobs/JOB/artifacts").mock(
        return_value=Response(200, json={"items": [artifact], "next_page_token": None})
    )
    recon_route = respx.get(f"{BASE}/v1/reconstructions/RECON/artifacts").mock(
        return_value=Response(200, json={"items": [artifact], "next_page_token": None})
    )
    content_route = respx.get(f"{BASE}/v1/artifacts/ART/content").mock(
        return_value=Response(200, content=b"abc")
    )

    with SfmApiClient(BASE) as c:
        assert c.list_artifact_kinds().items[0].kind == "features.local.v1"
        assert c.list_artifact_formats().items[0].format_id == "sfmapi.features.local.v1"
        imported = c.import_artifact(
            LegacyArtifactImportRequest(
                project_id="PROJECT",
                kind="features.local.v1",
                artifact_format="sfmapi.features.local.v1",
                uri="https://artifacts.example/features.json",
            )
        )
        assert imported.artifact_id == "ART"
        assert c.get_artifact("ART").links["self"].href == "/v1/artifacts/ART"  # type: ignore[index]
        plan = c.plan_artifact_conversion(
            "ART",
            LegacyArtifactConversionPlanRequest(to_format="sfmapi.features.local.v1"),
        )
        assert plan.executable is True
        accepted = c.convert_artifact(
            "ART",
            LegacyArtifactConvertRequest(to_format="sfmapi.features.local.v1"),
        )
        assert accepted.artifact_id == "ART"
        assert c.validate_artifact("ART").valid is True
        assert c.list_job_artifacts_page("JOB").items[0].artifact_id == "ART"
        assert c.list_reconstruction_artifacts_page("RECON").items[0].artifact_id == "ART"
        assert c.list_job_artifacts(
            "JOB",
            page_size=1,
            kind="features.local.v1",
            task_id="TASK",
            name="features",
        )[0].artifact_id == "ART"
        assert c.list_reconstruction_artifacts(
            "RECON",
            page_size=1,
            kind="features.local.v1",
            name="features",
        )[0].artifact_id == "ART"
        assert c.read_artifact_content("ART") == b"abc"

    assert json.loads(import_route.calls.last.request.content)["artifact_format"] == (
        "sfmapi.features.local.v1"
    )
    assert json.loads(plan_route.calls.last.request.content) == {
        "to_format": "sfmapi.features.local.v1",
    }
    assert json.loads(convert_route.calls.last.request.content) == {
        "to_format": "sfmapi.features.local.v1",
    }
    assert job_route.calls[0].request.url.query == b"page_size=100"
    assert recon_route.calls[0].request.url.query == b"page_size=100"
    assert job_route.calls.last.request.url.query == (
        b"page_size=1&kind=features.local.v1&task_id=TASK&name=features"
    )
    assert recon_route.calls.last.request.url.query == (
        b"page_size=1&kind=features.local.v1&name=features"
    )
    assert content_route.calls.last.request.url.query == b""


@pytest.mark.parametrize(
    ("model", "payload", "required_fields"),
    [
        (
            AttributesContractOut,
            {
                "contract": "attributes",
                "contract_schema_version": 1,
                "attribute_types": ["str"],
                "rules": {},
            },
            ["contract", "contract_schema_version", "attribute_types", "rules"],
        ),
        (
            DataTypesContractOut,
            {
                "contract": "datatypes",
                "contract_schema_version": 1,
                "kinds": [],
                "types": [],
            },
            ["contract", "contract_schema_version", "kinds", "types"],
        ),
        (
            OperationsContractOut,
            {
                "contract": "operations",
                "contract_schema_version": 1,
                "operations": [],
                "compatibility": {},
            },
            ["contract", "contract_schema_version", "operations", "compatibility"],
        ),
        (
            ProcessorsContractOut,
            {
                "contract": "processors",
                "contract_schema_version": 1,
                "processors": [],
                "rules": {},
            },
            ["contract", "contract_schema_version", "processors", "rules"],
        ),
        (
            PipelinesContractOut,
            {
                "contract": "pipelines",
                "contract_schema_version": 1,
                "composition_rule": "supplier.datatype == consumer.datatype",
                "initial_inputs": [],
                "canonical_pipelines": {},
                "plugin_pipelines": [],
                "step_schema": {},
                "validation_reasons": [],
            },
            [
                "contract",
                "contract_schema_version",
                "composition_rule",
                "initial_inputs",
                "canonical_pipelines",
                "plugin_pipelines",
                "step_schema",
                "validation_reasons",
            ],
        ),
    ],
)
def test_typed_dataflow_discovery_envelopes_preserve_required_fields(
    model: type[object],
    payload: dict[str, object],
    required_fields: list[str],
) -> None:
    for missing_field in required_fields:
        invalid = {key: value for key, value in payload.items() if key != missing_field}
        with pytest.raises(PydanticValidationError) as exc_info:
            model.model_validate(invalid)  # type: ignore[attr-defined]

        assert missing_field in str(exc_info.value)


def test_typed_pipeline_steps_reject_untyped_dicts() -> None:
    with pytest.raises(PydanticValidationError):
        PipelineValidateRequest(steps=[{"not_a_processor_or_operation": "x"}])


@respx.mock
def test_validation_error_propagates() -> None:
    respx.post(f"{BASE}/v1/datasets/DS/matches").mock(
        return_value=Response(
            422,
            json={"title": "Validation error", "status": 422, "detail": "vocab missing"},
            headers={"content-type": "application/problem+json"},
        )
    )
    with SfmApiClient(BASE) as c, pytest.raises(ValidationError):
        c.submit_matches("DS", pairs={"strategy": "vocabtree"})


@respx.mock
def test_legacy_error_map_distinguishes_generic_and_pycolmap_501() -> None:
    respx.get(f"{BASE}/v1/projects/generic").mock(
        return_value=Response(
            501,
            json={
                "title": "Capability not available in this deployment",
                "status": 501,
                "detail": "custom pipeline unavailable",
                "capability": "pipelines.custom_execution",
            },
            headers={"content-type": "application/problem+json"},
        )
    )
    with SfmApiClient(BASE) as c, pytest.raises(CapabilityUnavailableError) as generic:
        c.get_project("generic")
    assert not isinstance(generic.value, PycolmapUnavailableError)

    respx.get(f"{BASE}/v1/projects/pycolmap").mock(
        return_value=Response(
            501,
            json={
                "title": "Capability not available in this deployment",
                "status": 501,
                "detail": "pycolmap unavailable",
                "capability": "pycolmap",
            },
            headers={"content-type": "application/problem+json"},
        )
    )
    with SfmApiClient(BASE) as c, pytest.raises(PycolmapUnavailableError):
        c.get_project("pycolmap")


def test_legacy_error_exports_include_backend_unavailable() -> None:
    from sfmapi_client import BackendUnavailableError as Exported

    assert Exported is BackendUnavailableError


def test_generated_error_root_is_self_rooted() -> None:
    """The supported generated SDK owns its exception root: it must NOT
    derive from the deprecated ``sfmapi_client`` package (lean audit
    2026-07 item 5.1 — the old guarded import made the supported
    package's hierarchy depend on the deprecated one whenever both were
    installed). The attribute surface stays a superset of the legacy
    root so migrating callers only swap the import.
    """
    err = GeneratedNotFoundError(404, "missing", {"status": 404})

    assert not issubclass(GeneratedSfmApiError, SfmApiError)
    assert GeneratedSfmApiError.__bases__ == (Exception,)
    assert isinstance(err, GeneratedSfmApiError)
    assert err.status_code == 404
    assert err.detail == "missing"
    assert err.problem == {"status": 404}
    assert err.body == {"status": 404}
    assert err.response is None


def test_handwritten_bundle_adjustment_spec_allows_rig_mode() -> None:
    spec = BundleAdjustmentSpec(mode="rig")

    assert spec.mode == "rig"


@respx.mock
def test_generated_client_raises_for_documented_problem_response() -> None:
    respx.get(f"{BASE}/v1/projects/missing").mock(
        return_value=Response(
            404,
            json={
                "type": "https://sfmapi/errors/not_found",
                "title": "Resource not found",
                "status": 404,
                "detail": "Project missing not found",
            },
            headers={"content-type": "application/problem+json"},
        )
    )
    client = Client(base_url=BASE, raise_on_unexpected_status=True)

    with pytest.raises(generated_errors.UnexpectedStatus) as exc_info:
        get_project.sync(project_id="missing", client=client)

    with pytest.raises(GeneratedNotFoundError) as generated_exc:
        raise_for_status(exc_info.value)
    assert generated_exc.value.problem["status"] == 404
    assert generated_exc.value.response is None
    assert generated_exc.value.body["detail"] == "Project missing not found"


@pytest.mark.parametrize(
    "model",
    [
        ArtifactConversionPlanRequest(),
        ArtifactConversionPlanRequest(accepted_formats=[]),
        ArtifactConvertRequest(),
        ArtifactConvertRequest(accepted_formats=[]),
    ],
)
def test_generated_conversion_requests_require_a_target(model: object) -> None:
    with pytest.raises(ValueError, match="to_format or non-empty accepted_formats"):
        model.to_dict()


@pytest.mark.parametrize(
    "model",
    [
        ArtifactConversionPlanRequest(to_format="sfmapi.reconstruction.sparse.v1"),
        ArtifactConversionPlanRequest(
            accepted_formats=["sfmapi.reconstruction.sparse.v1"]
        ),
        ArtifactConvertRequest(to_format="sfmapi.reconstruction.sparse.v1"),
        ArtifactConvertRequest(accepted_formats=["sfmapi.reconstruction.sparse.v1"]),
    ],
)
def test_generated_conversion_requests_accept_target(model: object) -> None:
    assert model.to_dict()


@pytest.mark.parametrize(
    "factory",
    [
        LegacyArtifactConversionPlanRequest,
        LegacyArtifactConvertRequest,
    ],
)
def test_legacy_conversion_requests_require_a_target(factory: object) -> None:
    with pytest.raises(PydanticValidationError, match="to_format or non-empty accepted_formats"):
        factory()  # type: ignore[misc]
    with pytest.raises(PydanticValidationError, match="to_format or non-empty accepted_formats"):
        factory(accepted_formats=[])  # type: ignore[misc]


def test_legacy_artifact_import_files_require_typed_refs_with_uri() -> None:
    with pytest.raises(PydanticValidationError, match="uri"):
        LegacyArtifactFileRef(name="features")
    with pytest.raises(PydanticValidationError, match="ArtifactFileRef"):
        LegacyArtifactImportRequest(
            project_id="PROJECT",
            kind="features.local.v1",
            files=[{"name": "features", "uri": "https://artifacts.example/features.json"}],
        )
    request = LegacyArtifactImportRequest(
        project_id="PROJECT",
        kind="features.local.v1",
        files=[
            LegacyArtifactFileRef(
                name="features",
                uri="https://artifacts.example/features.json",
            )
        ],
    )
    assert request.files[0].uri == "https://artifacts.example/features.json"


# ----- async -----------------------------------------------------------------


@pytest.mark.asyncio
@respx.mock
async def test_async_create_project_round_trip() -> None:
    respx.post(f"{BASE}/v1/projects").mock(
        return_value=Response(201, json=_project_payload("beta"))
    )
    async with AsyncSfmApiClient(BASE, api_key="sfm_async") as c:
        p = await c.create_project("beta")
    assert p.name == "beta"


@pytest.mark.asyncio
@respx.mock
async def test_async_list_dataset_and_submodel_defaults_match_contract() -> None:
    datasets = respx.get(f"{BASE}/v1/projects/PR/datasets").mock(
        return_value=Response(200, json={"items": [_dataset_payload()], "next_page_token": None})
    )
    submodels = respx.get(f"{BASE}/v1/reconstructions/REC/submodels").mock(
        return_value=Response(200, json={"items": [_submodel_payload()], "next_page_token": None})
    )

    async with AsyncSfmApiClient(BASE) as c:
        assert (await c.list_datasets_page("PR")).items[0].name == "dataset"
        assert (await c.list_submodels_page("REC")).items[0].submodel_id == "S" * 26

    assert datasets.calls[0].request.url.params["page_size"] == "100"
    assert submodels.calls[0].request.url.params["page_size"] == "100"


@pytest.mark.asyncio
@respx.mock
async def test_async_artifact_helpers_route() -> None:
    artifact = _stage_artifact_payload()
    respx.get(f"{BASE}/v1/artifacts/ART").mock(return_value=Response(200, json=artifact))
    list_route = respx.get(f"{BASE}/v1/jobs/JOB/artifacts").mock(
        return_value=Response(200, json={"items": [artifact], "next_page_token": None})
    )
    respx.get(f"{BASE}/v1/artifacts/ART/content").mock(
        return_value=Response(200, content=b"abc")
    )

    async with AsyncSfmApiClient(BASE) as c:
        assert (await c.get_artifact("ART")).artifact_id == "ART"
        assert (await c.list_job_artifacts_page("JOB")).items[0].artifact_id == "ART"
        assert (
            await c.list_job_artifacts(
                "JOB",
                page_size=1,
                kind="features.local.v1",
                task_id="TASK",
                name="features",
            )
        )[0].artifact_id == "ART"
        assert await c.read_artifact_content("ART") == b"abc"

    assert list_route.calls[0].request.url.query == b"page_size=100"
    assert list_route.calls.last.request.url.query == (
        b"page_size=1&kind=features.local.v1&task_id=TASK&name=features"
    )


@pytest.mark.asyncio
@respx.mock
async def test_async_typed_pipeline_helpers_route() -> None:
    validate = respx.post(f"{BASE}/v1/pipelines:validate").mock(
        return_value=Response(200, json={"valid": True, "errors": []})
    )
    run = respx.post(f"{BASE}/v1/projects/PR/pipelines:run").mock(
        return_value=Response(
            202,
            json={
                "job_id": "JA" * 13,
                "task_ids": ["TA" * 13],
                "recon_id": None,
            },
        )
    )
    async with AsyncSfmApiClient(BASE) as c:
        valid = await c.validate_pipeline({"steps": ["features"]})
        accepted = await c.run_typed_pipeline(
            "PR", {"dataset_id": "DS", "steps": ["features"]}
        )
    assert valid.valid is True
    assert accepted.job_id == "JA" * 13
    assert validate.calls.call_count == 1
    assert run.calls.call_count == 1


@pytest.mark.asyncio
@respx.mock
async def test_async_typed_dataflow_discovery_helpers_route() -> None:
    respx.get(f"{BASE}/v1/attributes").mock(
        return_value=Response(
            200,
            json={
                "contract": "attributes",
                "contract_schema_version": 1,
                "attribute_types": ["str"],
                "rules": {},
            },
        )
    )
    respx.get(f"{BASE}/v1/datatypes").mock(
        return_value=Response(
            200,
            json={
                "contract": "datatypes",
                "contract_schema_version": 1,
                "kinds": [],
                "types": [],
            },
        )
    )
    respx.get(f"{BASE}/v1/operations").mock(
        return_value=Response(
            200,
            json={
                "contract": "operations",
                "contract_schema_version": 1,
                "operations": [],
                "compatibility": {},
            },
        )
    )
    respx.get(f"{BASE}/v1/processors").mock(
        return_value=Response(
            200,
            json={
                "contract": "processors",
                "contract_schema_version": 1,
                "processors": [],
                "rules": {},
            },
        )
    )
    respx.get(f"{BASE}/v1/pipelines").mock(
        return_value=Response(
            200,
            json={
                "contract": "pipelines",
                "contract_schema_version": 1,
                "composition_rule": "supplier.datatype == consumer.datatype",
                "initial_inputs": [],
                "canonical_pipelines": {},
                "plugin_pipelines": [],
                "step_schema": {},
                "validation_reasons": [],
            },
        )
    )

    async with AsyncSfmApiClient(BASE) as c:
        assert (await c.list_attributes()).contract == "attributes"
        assert (await c.list_datatypes()).contract == "datatypes"
        assert (await c.list_operations()).contract == "operations"
        assert (await c.list_processors()).contract == "processors"
        assert (await c.list_pipelines()).contract == "pipelines"


@pytest.mark.asyncio
@respx.mock
async def test_async_dense_mesh_helpers_fail_before_request() -> None:
    async with AsyncSfmApiClient(BASE) as c:
        with pytest.raises(NotImplementedError, match="out of scope"):
            await c.submit_dense("R" * 26)
        with pytest.raises(NotImplementedError, match="out of scope"):
            await c.submit_mesh("R" * 26)
        with pytest.raises(NotImplementedError, match="out of scope"):
            await c.read_dense_index("R" * 26, 1)
        with pytest.raises(NotImplementedError, match="out of scope"):
            await c.read_mesh_ply("R" * 26, 1)
    assert not respx.calls


@pytest.mark.asyncio
@respx.mock
async def test_async_upload_bytes_uses_total_size_and_verifies_sha() -> None:
    payload = b"0123456789abcdef"
    sha = hashlib.sha256(payload).hexdigest()

    respx.post(f"{BASE}/v1/uploads").mock(
        return_value=Response(
            201,
            json={
                "upload_id": "AU" * 13,
                "state": "open",
                "expected_size": len(payload),
                "received_bytes": 0,
                "blob_sha": None,
                "expires_at": "2026-05-03T00:00:00Z",
            },
        )
    )
    patch = respx.patch(f"{BASE}/v1/uploads/{'AU' * 13}").mock(
        return_value=Response(
            200,
            json={
                "upload_id": "AU" * 13,
                "state": "received",
                "expected_size": len(payload),
                "received_bytes": len(payload),
                "blob_sha": None,
                "expires_at": "2026-05-03T00:00:00Z",
            },
        )
    )
    respx.post(f"{BASE}/v1/uploads/{'AU' * 13}:finalize").mock(
        return_value=Response(
            200,
            json={
                "upload_id": "AU" * 13,
                "state": "finalized",
                "expected_size": len(payload),
                "received_bytes": len(payload),
                "blob_sha": sha,
                "expires_at": "2026-05-03T00:00:00Z",
            },
        )
    )

    async with AsyncSfmApiClient(BASE) as c:
        result = await c.upload_bytes(payload, chunk_size=5)
    assert result == sha
    assert [call.request.headers["Content-Range"] for call in patch.calls] == [
        "bytes 0-4/16",
        "bytes 5-9/16",
        "bytes 10-14/16",
        "bytes 15-15/16",
    ]


@pytest.mark.asyncio
@respx.mock
async def test_async_resume_job() -> None:
    respx.post(f"{BASE}/v1/jobs/J1:resume").mock(
        return_value=Response(
            202,
            json={
                "job_id": "J1",
                "tenant_id": "default",
                "project_id": "PR",
                "recipe": "incremental",
                "status": "pending",
                "cancel_requested": False,
                "cancel_force": False,
                "created_at": "2026-05-02T00:00:00Z",
            },
        )
    )
    async with AsyncSfmApiClient(BASE) as c:
        j = await c.resume_job("J1")
    assert j.status == "pending"
