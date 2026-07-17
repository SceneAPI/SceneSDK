from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_v1_jobs_get_status_type_0 import ListV1JobsGetStatusType0
from ...models.page_job_out import PageJobOut
from ...models.problem_response import ProblemResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page_token: None | str | Unset = UNSET,
    page_size: int | Unset = 50,
    status: ListV1JobsGetStatusType0 | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_page_token: None | str | Unset
    if isinstance(page_token, Unset):
        json_page_token = UNSET
    else:
        json_page_token = page_token
    params["page_token"] = json_page_token

    params["page_size"] = page_size

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, ListV1JobsGetStatusType0):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/jobs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PageJobOut | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = PageJobOut.from_dict(response.json())

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
) -> Response[PageJobOut | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    page_token: None | str | Unset = UNSET,
    page_size: int | Unset = 50,
    status: ListV1JobsGetStatusType0 | None | Unset = UNSET,
) -> Response[PageJobOut | ProblemResponse]:
    """List

     List jobs for the caller's tenant (AIP-158 paginated).

    Most-recent first (sorted by ``job_id`` descending — ULIDs are
    timestamp-prefixed). Pass ``status=running`` to find active work
    or ``status=failed`` to triage. Without ``status``, all jobs in
    every state are returned. ``next_page_token=null`` ends the
    cursor.

    Args:
        page_token (None | str | Unset):
        page_size (int | Unset):  Default: 50.
        status (ListV1JobsGetStatusType0 | None | Unset): Filter to one lifecycle state. Closed
            set: pending | running | succeeded | failed | cancelled | cancelled_dirty.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PageJobOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        page_token=page_token,
        page_size=page_size,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    page_token: None | str | Unset = UNSET,
    page_size: int | Unset = 50,
    status: ListV1JobsGetStatusType0 | None | Unset = UNSET,
) -> PageJobOut | ProblemResponse | None:
    """List

     List jobs for the caller's tenant (AIP-158 paginated).

    Most-recent first (sorted by ``job_id`` descending — ULIDs are
    timestamp-prefixed). Pass ``status=running`` to find active work
    or ``status=failed`` to triage. Without ``status``, all jobs in
    every state are returned. ``next_page_token=null`` ends the
    cursor.

    Args:
        page_token (None | str | Unset):
        page_size (int | Unset):  Default: 50.
        status (ListV1JobsGetStatusType0 | None | Unset): Filter to one lifecycle state. Closed
            set: pending | running | succeeded | failed | cancelled | cancelled_dirty.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PageJobOut | ProblemResponse
    """

    return sync_detailed(
        client=client,
        page_token=page_token,
        page_size=page_size,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    page_token: None | str | Unset = UNSET,
    page_size: int | Unset = 50,
    status: ListV1JobsGetStatusType0 | None | Unset = UNSET,
) -> Response[PageJobOut | ProblemResponse]:
    """List

     List jobs for the caller's tenant (AIP-158 paginated).

    Most-recent first (sorted by ``job_id`` descending — ULIDs are
    timestamp-prefixed). Pass ``status=running`` to find active work
    or ``status=failed`` to triage. Without ``status``, all jobs in
    every state are returned. ``next_page_token=null`` ends the
    cursor.

    Args:
        page_token (None | str | Unset):
        page_size (int | Unset):  Default: 50.
        status (ListV1JobsGetStatusType0 | None | Unset): Filter to one lifecycle state. Closed
            set: pending | running | succeeded | failed | cancelled | cancelled_dirty.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PageJobOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        page_token=page_token,
        page_size=page_size,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    page_token: None | str | Unset = UNSET,
    page_size: int | Unset = 50,
    status: ListV1JobsGetStatusType0 | None | Unset = UNSET,
) -> PageJobOut | ProblemResponse | None:
    """List

     List jobs for the caller's tenant (AIP-158 paginated).

    Most-recent first (sorted by ``job_id`` descending — ULIDs are
    timestamp-prefixed). Pass ``status=running`` to find active work
    or ``status=failed`` to triage. Without ``status``, all jobs in
    every state are returned. ``next_page_token=null`` ends the
    cursor.

    Args:
        page_token (None | str | Unset):
        page_size (int | Unset):  Default: 50.
        status (ListV1JobsGetStatusType0 | None | Unset): Filter to one lifecycle state. Closed
            set: pending | running | succeeded | failed | cancelled | cancelled_dirty.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PageJobOut | ProblemResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            page_token=page_token,
            page_size=page_size,
            status=status,
        )
    ).parsed
