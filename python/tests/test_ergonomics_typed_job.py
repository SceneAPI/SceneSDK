# SPDX-License-Identifier: AGPL-3.0-or-later
"""Unit tests for sfmapi_client_gen._ergonomics.wait_for_job_typed and
submit_and_wait_typed."""

from __future__ import annotations

from typing import Any
from unittest import mock

from sfmapi_client_gen._ergonomics import (
    JobDetail,
    submit_and_wait_typed,
    wait_for_job_typed,
)


def _minimal_job_body(status: str = "succeeded") -> dict[str, Any]:
    """Smallest JobDetail body that `from_dict` accepts (every field the
    generated model declares as required must be present).
    """
    return {
        "job_id": "01JZABCDEFGHJKMNPQRSTVWXYZ",
        "tenant_id": "default",
        "project_id": "01JZ00000000000000000000AB",
        "recipe": "incremental",
        "status": status,
        "cancel_requested": False,
        "cancel_force": False,
        "created_at": "2026-05-28T00:00:00Z",
        "updated_at": "2026-05-28T00:01:00Z",
        "tasks": [],
        "progress": 1.0,
    }


def test_wait_for_job_typed_returns_jobdetail() -> None:
    body = _minimal_job_body()
    with mock.patch(
        "sfmapi_client_gen._ergonomics.wait_for_job",
        return_value=body,
    ) as wait_for_job:
        result = wait_for_job_typed(
            "http://localhost:8000",
            "01JZABCDEFGHJKMNPQRSTVWXYZ",
            api_key="k",
            timeout=30.0,
        )
    assert isinstance(result, JobDetail)
    # Verify the wrapper actually decoded the body, not just re-emitted
    # a placeholder JobDetail.
    assert result.job_id == body["job_id"]
    assert result.status.value == "succeeded"
    # Confirm the wait helper got the kwargs the wrapper was supposed to
    # forward (api_key, timeout) -- guard against silent shadowing.
    wait_for_job.assert_called_once()
    _, call_kwargs = wait_for_job.call_args
    assert call_kwargs["api_key"] == "k"
    assert call_kwargs["timeout"] == 30.0


def test_submit_and_wait_typed_returns_jobdetail() -> None:
    body = _minimal_job_body(status="failed")
    with mock.patch(
        "sfmapi_client_gen._ergonomics.submit_and_wait",
        return_value=body,
    ) as submit_and_wait:
        result = submit_and_wait_typed(
            "http://localhost:8000",
            submit_fn=lambda: {"job_id": "x"},
            api_key="k",
        )
    assert isinstance(result, JobDetail)
    assert result.status.value == "failed"
    submit_and_wait.assert_called_once()
