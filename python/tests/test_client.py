"""Generated-SDK tests using respx to mock httpx.

We only assert the SDK's request shape, response parsing, and typed
error surface; the server contract itself is covered by the server
repo's contract tests. The hand-rolled ``sfmapi_client`` package these
tests once exercised was removed at 0.1.0 as scheduled — the generated
``scenesdk`` package is the only Python SDK surface.
"""

from __future__ import annotations

import pytest
import respx
from httpx import Response
from scenesdk import Client
from scenesdk import errors as generated_errors
from scenesdk._ergonomics import NotFoundError as GeneratedNotFoundError
from scenesdk._ergonomics import SfmApiError as GeneratedSfmApiError
from scenesdk._ergonomics import raise_for_status
from scenesdk.api.projects import get_v1_projects_project_id_get as get_project
from scenesdk.models import ArtifactConversionPlanRequest, ArtifactConvertRequest

BASE = "http://api.test"


def test_generated_error_root_is_self_rooted() -> None:
    """The generated SDK owns its exception root: it derives straight
    from ``Exception`` (lean audit 2026-07 item 5.1 — an old guarded
    import once made this hierarchy depend on the hand-rolled
    ``sfmapi_client`` package whenever both were installed; that
    package was removed at 0.1.0). The attribute surface stays a
    superset of the legacy root so migrated callers keep working.
    """
    err = GeneratedNotFoundError(404, "missing", {"status": 404})

    assert GeneratedSfmApiError.__bases__ == (Exception,)
    assert isinstance(err, GeneratedSfmApiError)
    assert err.status_code == 404
    assert err.detail == "missing"
    assert err.problem == {"status": 404}
    assert err.body == {"status": 404}
    assert err.response is None


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
