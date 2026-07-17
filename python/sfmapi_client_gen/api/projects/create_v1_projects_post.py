from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_response import ProblemResponse
from ...models.project_create import ProjectCreate
from ...models.project_out import ProjectOut
from ...types import Response


def _get_kwargs(
    *,
    body: ProjectCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/projects",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemResponse | ProjectOut | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 201:
        response_201 = ProjectOut.from_dict(response.json())

        return response_201

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
) -> Response[ProblemResponse | ProjectOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ProjectCreate,
) -> Response[ProblemResponse | ProjectOut]:
    """Create

     Create a new Project under the caller's tenant.

    Projects are the top-level workspace; every Dataset / Reconstruction
    rolls up under one. ``name`` is a human label and is NOT unique —
    rely on the returned ``project_id`` (a ULID) as the canonical key.

    Args:
        body (ProjectCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | ProjectOut]
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
    body: ProjectCreate,
) -> ProblemResponse | ProjectOut | None:
    """Create

     Create a new Project under the caller's tenant.

    Projects are the top-level workspace; every Dataset / Reconstruction
    rolls up under one. ``name`` is a human label and is NOT unique —
    rely on the returned ``project_id`` (a ULID) as the canonical key.

    Args:
        body (ProjectCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | ProjectOut
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ProjectCreate,
) -> Response[ProblemResponse | ProjectOut]:
    """Create

     Create a new Project under the caller's tenant.

    Projects are the top-level workspace; every Dataset / Reconstruction
    rolls up under one. ``name`` is a human label and is NOT unique —
    rely on the returned ``project_id`` (a ULID) as the canonical key.

    Args:
        body (ProjectCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | ProjectOut]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ProjectCreate,
) -> ProblemResponse | ProjectOut | None:
    """Create

     Create a new Project under the caller's tenant.

    Projects are the top-level workspace; every Dataset / Reconstruction
    rolls up under one. ``name`` is a human label and is NOT unique —
    rely on the returned ``project_id`` (a ULID) as the canonical key.

    Args:
        body (ProjectCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | ProjectOut
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
