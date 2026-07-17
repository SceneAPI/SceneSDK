from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_response import ProblemResponse
from ...models.tiles_index_v1_reconstructions_recon_id_snapshots_seq_tiles_index_json_get_response_200 import (
    TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    recon_id: str,
    seq: int,
    *,
    max_level: int | Unset = 4,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["max_level"] = max_level

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/reconstructions/{recon_id}/snapshots/{seq}/tiles/index.json".format(
            recon_id=quote(str(recon_id), safe=""),
            seq=quote(str(seq), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ProblemResponse
    | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200
    | None
):
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200.from_dict(
            response.json()
        )

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
) -> Response[
    ProblemResponse
    | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    recon_id: str,
    seq: int,
    *,
    client: AuthenticatedClient | Client,
    max_level: int | Unset = 4,
) -> Response[
    ProblemResponse
    | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200
]:
    """Tiles Index

     Octree tile index for the snapshot's `points.bin`. Tiles are
    generated lazily on first request, then cached on disk under
    `<snapshot>/tiles/`. Subsequent requests for tile bytes hit the
    cache directly.

    Args:
        recon_id (str):
        seq (int):
        max_level (int | Unset):  Default: 4.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200]
    """

    kwargs = _get_kwargs(
        recon_id=recon_id,
        seq=seq,
        max_level=max_level,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    recon_id: str,
    seq: int,
    *,
    client: AuthenticatedClient | Client,
    max_level: int | Unset = 4,
) -> (
    ProblemResponse
    | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200
    | None
):
    """Tiles Index

     Octree tile index for the snapshot's `points.bin`. Tiles are
    generated lazily on first request, then cached on disk under
    `<snapshot>/tiles/`. Subsequent requests for tile bytes hit the
    cache directly.

    Args:
        recon_id (str):
        seq (int):
        max_level (int | Unset):  Default: 4.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200
    """

    return sync_detailed(
        recon_id=recon_id,
        seq=seq,
        client=client,
        max_level=max_level,
    ).parsed


async def asyncio_detailed(
    recon_id: str,
    seq: int,
    *,
    client: AuthenticatedClient | Client,
    max_level: int | Unset = 4,
) -> Response[
    ProblemResponse
    | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200
]:
    """Tiles Index

     Octree tile index for the snapshot's `points.bin`. Tiles are
    generated lazily on first request, then cached on disk under
    `<snapshot>/tiles/`. Subsequent requests for tile bytes hit the
    cache directly.

    Args:
        recon_id (str):
        seq (int):
        max_level (int | Unset):  Default: 4.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200]
    """

    kwargs = _get_kwargs(
        recon_id=recon_id,
        seq=seq,
        max_level=max_level,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    recon_id: str,
    seq: int,
    *,
    client: AuthenticatedClient | Client,
    max_level: int | Unset = 4,
) -> (
    ProblemResponse
    | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200
    | None
):
    """Tiles Index

     Octree tile index for the snapshot's `points.bin`. Tiles are
    generated lazily on first request, then cached on disk under
    `<snapshot>/tiles/`. Subsequent requests for tile bytes hit the
    cache directly.

    Args:
        recon_id (str):
        seq (int):
        max_level (int | Unset):  Default: 4.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200
    """

    return (
        await asyncio_detailed(
            recon_id=recon_id,
            seq=seq,
            client=client,
            max_level=max_level,
        )
    ).parsed
