from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.artifact_import_request import ArtifactImportRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.stage_artifact_out import StageArtifactOut
from ...types import Response


def _get_kwargs(
    *,
    body: ArtifactImportRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/artifacts:import",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | StageArtifactOut | None:
    if response.status_code == 201:
        response_201 = StageArtifactOut.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | StageArtifactOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ArtifactImportRequest,
) -> Response[HTTPValidationError | StageArtifactOut]:
    """Import Artifact

     Register an existing artifact URI for validation and downstream reuse.

    Args:
        body (ArtifactImportRequest): Register an existing artifact URI as a typed sfmapi
            artifact.

            Imports do not copy bytes. They create a completed import job/task
            that owns the artifact descriptor so the artifact can be validated,
            converted, and used as a downstream stage input.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | StageArtifactOut]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ArtifactImportRequest,
) -> HTTPValidationError | StageArtifactOut | None:
    """Import Artifact

     Register an existing artifact URI for validation and downstream reuse.

    Args:
        body (ArtifactImportRequest): Register an existing artifact URI as a typed sfmapi
            artifact.

            Imports do not copy bytes. They create a completed import job/task
            that owns the artifact descriptor so the artifact can be validated,
            converted, and used as a downstream stage input.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | StageArtifactOut
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ArtifactImportRequest,
) -> Response[HTTPValidationError | StageArtifactOut]:
    """Import Artifact

     Register an existing artifact URI for validation and downstream reuse.

    Args:
        body (ArtifactImportRequest): Register an existing artifact URI as a typed sfmapi
            artifact.

            Imports do not copy bytes. They create a completed import job/task
            that owns the artifact descriptor so the artifact can be validated,
            converted, and used as a downstream stage input.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | StageArtifactOut]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ArtifactImportRequest,
) -> HTTPValidationError | StageArtifactOut | None:
    """Import Artifact

     Register an existing artifact URI for validation and downstream reuse.

    Args:
        body (ArtifactImportRequest): Register an existing artifact URI as a typed sfmapi
            artifact.

            Imports do not copy bytes. They create a completed import job/task
            that owns the artifact descriptor so the artifact can be validated,
            converted, and used as a downstream stage input.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | StageArtifactOut
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
