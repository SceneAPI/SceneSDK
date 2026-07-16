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
from sfmapi_client import (
    AsyncSfmApiClient,
    BackendUnavailableError,
    BundleAdjustmentSpec,
    CapabilityUnavailableError,
    FeaturesSpec,
    IncrementalSpec,
    NotFoundError,
    PycolmapUnavailableError,
    SfmApiClient,
    SfmApiError,
    ValidationError,
)
from sfmapi_client_gen import Client
from sfmapi_client_gen import errors as generated_errors
from sfmapi_client_gen._ergonomics import SfmApiError as GeneratedSfmApiError
from sfmapi_client_gen._ergonomics import NotFoundError as GeneratedNotFoundError
from sfmapi_client_gen._ergonomics import raise_for_status
from sfmapi_client_gen.api.projects import get_v1_projects_project_id_get as get_project
from sfmapi_client_gen.models import ArtifactConversionPlanRequest, ArtifactConvertRequest

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
        page = c.list_datasets_page("PR", page_size=7, page_token="tok")
        items = c.list_datasets("PR", page_size=7, page_token="tok")

    assert page.next_page_token == "next"
    assert page.items[0].name == "dataset"
    assert items[0].name == "dataset"
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
        page = c.list_submodels_page("REC", page_size=2, page_token="tok")
        items = c.list_submodels("REC", page_size=2, page_token="tok")

    assert page.next_page_token == "next"
    assert page.items[0].submodel_id == "S" * 26
    assert items[0].submodel_id == "S" * 26
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


def test_generated_error_root_is_legacy_error_root() -> None:
    err = GeneratedNotFoundError(404, "missing", {"status": 404})

    assert issubclass(GeneratedSfmApiError, SfmApiError)
    assert isinstance(err, SfmApiError)
    assert err.status_code == 404


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
