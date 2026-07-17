from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.job_progress_out import JobProgressOut
from ...models.problem_response import ProblemResponse
from ...types import Response


def _get_kwargs(
    job_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/jobs/{job_id}/progress".format(
            job_id=quote(str(job_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> JobProgressOut | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = JobProgressOut.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ProblemResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ProblemResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ProblemResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ProblemResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ProblemResponse.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = ProblemResponse.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = ProblemResponse.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ProblemResponse.from_dict(response.json())

        return response_429

    if response.status_code == 501:
        response_501 = ProblemResponse.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = ProblemResponse.from_dict(response.json())

        return response_503

    if response.status_code == 507:
        response_507 = ProblemResponse.from_dict(response.json())

        return response_507

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[JobProgressOut | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[JobProgressOut | ProblemResponse]:
    """Progress

     Return a compact progress snapshot for a job.

    This is the polling counterpart to ``GET /v1/jobs/{job_id}/events``.
    It always works from durable state: task lifecycle rows plus the
    latest persisted progress events. ``progress`` is a best-effort
    fraction, so clients should treat it as UI telemetry rather than a
    scheduling guarantee.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobProgressOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> JobProgressOut | ProblemResponse | None:
    """Progress

     Return a compact progress snapshot for a job.

    This is the polling counterpart to ``GET /v1/jobs/{job_id}/events``.
    It always works from durable state: task lifecycle rows plus the
    latest persisted progress events. ``progress`` is a best-effort
    fraction, so clients should treat it as UI telemetry rather than a
    scheduling guarantee.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobProgressOut | ProblemResponse
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[JobProgressOut | ProblemResponse]:
    """Progress

     Return a compact progress snapshot for a job.

    This is the polling counterpart to ``GET /v1/jobs/{job_id}/events``.
    It always works from durable state: task lifecycle rows plus the
    latest persisted progress events. ``progress`` is a best-effort
    fraction, so clients should treat it as UI telemetry rather than a
    scheduling guarantee.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobProgressOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> JobProgressOut | ProblemResponse | None:
    """Progress

     Return a compact progress snapshot for a job.

    This is the polling counterpart to ``GET /v1/jobs/{job_id}/events``.
    It always works from durable state: task lifecycle rows plus the
    latest persisted progress events. ``progress`` is a best-effort
    fraction, so clients should treat it as UI telemetry rather than a
    scheduling guarantee.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobProgressOut | ProblemResponse
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
        )
    ).parsed
