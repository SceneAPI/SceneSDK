from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_response import ProblemResponse
from ...models.upload_init import UploadInit
from ...models.upload_out import UploadOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: UploadInit,
    idempotency_key: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/uploads",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemResponse | UploadOut | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 201:
        response_201 = UploadOut.from_dict(response.json())

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
) -> Response[ProblemResponse | UploadOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: UploadInit,
    idempotency_key: None | str | Unset = UNSET,
) -> Response[ProblemResponse | UploadOut]:
    r"""Init

     Open a chunked-upload session.

    Reserves an ``upload_id`` for the caller to ``PATCH`` chunks into.
    ``Idempotency-Key`` (recommended) makes init replay-safe — a retry
    with the same key returns the same upload row. Returns
    :class:`UploadOut` with ``state=\"open\"``; the row expires at
    ``expires_at`` if the client never finalizes.

    Args:
        idempotency_key (None | str | Unset):
        body (UploadInit):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | UploadOut]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: UploadInit,
    idempotency_key: None | str | Unset = UNSET,
) -> ProblemResponse | UploadOut | None:
    r"""Init

     Open a chunked-upload session.

    Reserves an ``upload_id`` for the caller to ``PATCH`` chunks into.
    ``Idempotency-Key`` (recommended) makes init replay-safe — a retry
    with the same key returns the same upload row. Returns
    :class:`UploadOut` with ``state=\"open\"``; the row expires at
    ``expires_at`` if the client never finalizes.

    Args:
        idempotency_key (None | str | Unset):
        body (UploadInit):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | UploadOut
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: UploadInit,
    idempotency_key: None | str | Unset = UNSET,
) -> Response[ProblemResponse | UploadOut]:
    r"""Init

     Open a chunked-upload session.

    Reserves an ``upload_id`` for the caller to ``PATCH`` chunks into.
    ``Idempotency-Key`` (recommended) makes init replay-safe — a retry
    with the same key returns the same upload row. Returns
    :class:`UploadOut` with ``state=\"open\"``; the row expires at
    ``expires_at`` if the client never finalizes.

    Args:
        idempotency_key (None | str | Unset):
        body (UploadInit):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | UploadOut]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: UploadInit,
    idempotency_key: None | str | Unset = UNSET,
) -> ProblemResponse | UploadOut | None:
    r"""Init

     Open a chunked-upload session.

    Reserves an ``upload_id`` for the caller to ``PATCH`` chunks into.
    ``Idempotency-Key`` (recommended) makes init replay-safe — a retry
    with the same key returns the same upload row. Returns
    :class:`UploadOut` with ``state=\"open\"``; the row expires at
    ``expires_at`` if the client never finalizes.

    Args:
        idempotency_key (None | str | Unset):
        body (UploadInit):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | UploadOut
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
