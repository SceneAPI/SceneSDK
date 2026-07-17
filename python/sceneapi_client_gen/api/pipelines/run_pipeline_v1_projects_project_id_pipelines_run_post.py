from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.job_accepted_response import JobAcceptedResponse
from ...models.pipeline_run_request import PipelineRunRequest
from ...models.problem_response import ProblemResponse
from ...types import Response


def _get_kwargs(
    project_id: str,
    *,
    body: PipelineRunRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/projects/{project_id}/pipelines:run".format(
            project_id=quote(str(project_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> JobAcceptedResponse | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 202:
        response_202 = JobAcceptedResponse.from_dict(response.json())

        return response_202

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
) -> Response[JobAcceptedResponse | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PipelineRunRequest,
) -> Response[JobAcceptedResponse | ProblemResponse]:
    """Run Pipeline

     Submit a pipeline through the typed Processor preflight surface.

    Processor steps are type-checked against named consumer/supplier ports
    before any job is created. Legacy operation-id list steps remain accepted
    as a compatibility input shape and are projected through the legacy
    operation contract. The legacy flat SfM chain is routed through the recipe
    DAG executor and returns 202. Native typed DAG execution is not available
    yet, so type-valid native requests return 501 after project/dataset
    validation rather than creating jobs that would fail later as ``UnknownTask``.

    Args:
        project_id (str):
        body (PipelineRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobAcceptedResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PipelineRunRequest,
) -> JobAcceptedResponse | ProblemResponse | None:
    """Run Pipeline

     Submit a pipeline through the typed Processor preflight surface.

    Processor steps are type-checked against named consumer/supplier ports
    before any job is created. Legacy operation-id list steps remain accepted
    as a compatibility input shape and are projected through the legacy
    operation contract. The legacy flat SfM chain is routed through the recipe
    DAG executor and returns 202. Native typed DAG execution is not available
    yet, so type-valid native requests return 501 after project/dataset
    validation rather than creating jobs that would fail later as ``UnknownTask``.

    Args:
        project_id (str):
        body (PipelineRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobAcceptedResponse | ProblemResponse
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PipelineRunRequest,
) -> Response[JobAcceptedResponse | ProblemResponse]:
    """Run Pipeline

     Submit a pipeline through the typed Processor preflight surface.

    Processor steps are type-checked against named consumer/supplier ports
    before any job is created. Legacy operation-id list steps remain accepted
    as a compatibility input shape and are projected through the legacy
    operation contract. The legacy flat SfM chain is routed through the recipe
    DAG executor and returns 202. Native typed DAG execution is not available
    yet, so type-valid native requests return 501 after project/dataset
    validation rather than creating jobs that would fail later as ``UnknownTask``.

    Args:
        project_id (str):
        body (PipelineRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobAcceptedResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PipelineRunRequest,
) -> JobAcceptedResponse | ProblemResponse | None:
    """Run Pipeline

     Submit a pipeline through the typed Processor preflight surface.

    Processor steps are type-checked against named consumer/supplier ports
    before any job is created. Legacy operation-id list steps remain accepted
    as a compatibility input shape and are projected through the legacy
    operation contract. The legacy flat SfM chain is routed through the recipe
    DAG executor and returns 202. Native typed DAG execution is not available
    yet, so type-valid native requests return 501 after project/dataset
    validation rather than creating jobs that would fail later as ``UnknownTask``.

    Args:
        project_id (str):
        body (PipelineRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobAcceptedResponse | ProblemResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
