from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_response import ProblemResponse
from ...models.snapshot_list_response import SnapshotListResponse
from ...types import Response


def _get_kwargs(
    recon_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/reconstructions/{recon_id}/snapshots".format(
            recon_id=quote(str(recon_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemResponse | SnapshotListResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = SnapshotListResponse.from_dict(response.json())

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
) -> Response[ProblemResponse | SnapshotListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    recon_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ProblemResponse | SnapshotListResponse]:
    r"""List Snapshots

     List sealed snapshots for a reconstruction.

    Returns the full sequence of ``seq`` ints + a HAL ``_links`` block
    keyed by ``str(seq)`` plus a ``\"latest\"`` shortcut. Each link
    block points at the per-snapshot files (``points.bin``,
    ``cameras.json``, etc). Snapshots are immutable once sealed — the
    file routes carry strong ETags + ``immutable`` Cache-Control.

    Args:
        recon_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | SnapshotListResponse]
    """

    kwargs = _get_kwargs(
        recon_id=recon_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    recon_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ProblemResponse | SnapshotListResponse | None:
    r"""List Snapshots

     List sealed snapshots for a reconstruction.

    Returns the full sequence of ``seq`` ints + a HAL ``_links`` block
    keyed by ``str(seq)`` plus a ``\"latest\"`` shortcut. Each link
    block points at the per-snapshot files (``points.bin``,
    ``cameras.json``, etc). Snapshots are immutable once sealed — the
    file routes carry strong ETags + ``immutable`` Cache-Control.

    Args:
        recon_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | SnapshotListResponse
    """

    return sync_detailed(
        recon_id=recon_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    recon_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ProblemResponse | SnapshotListResponse]:
    r"""List Snapshots

     List sealed snapshots for a reconstruction.

    Returns the full sequence of ``seq`` ints + a HAL ``_links`` block
    keyed by ``str(seq)`` plus a ``\"latest\"`` shortcut. Each link
    block points at the per-snapshot files (``points.bin``,
    ``cameras.json``, etc). Snapshots are immutable once sealed — the
    file routes carry strong ETags + ``immutable`` Cache-Control.

    Args:
        recon_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | SnapshotListResponse]
    """

    kwargs = _get_kwargs(
        recon_id=recon_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    recon_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ProblemResponse | SnapshotListResponse | None:
    r"""List Snapshots

     List sealed snapshots for a reconstruction.

    Returns the full sequence of ``seq`` ints + a HAL ``_links`` block
    keyed by ``str(seq)`` plus a ``\"latest\"`` shortcut. Each link
    block points at the per-snapshot files (``points.bin``,
    ``cameras.json``, etc). Snapshots are immutable once sealed — the
    file routes carry strong ETags + ``immutable`` Cache-Control.

    Args:
        recon_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | SnapshotListResponse
    """

    return (
        await asyncio_detailed(
            recon_id=recon_id,
            client=client,
        )
    ).parsed
