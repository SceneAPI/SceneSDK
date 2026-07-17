from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_key_out import ApiKeyOut
from ...models.problem_response import ProblemResponse
from ...types import Response


def _get_kwargs(
    api_key_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/admin/api-keys/{api_key_id}".format(
            api_key_id=quote(str(api_key_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiKeyOut | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = ApiKeyOut.from_dict(response.json())

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
) -> Response[ApiKeyOut | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    api_key_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiKeyOut | ProblemResponse]:
    """Revoke

     Revoke a previously-issued API key.

    Soft-delete: the row stays for audit, ``revoked_at`` is stamped
    and ``revoked=true`` shipped on the next read. Subsequent auth
    attempts with that key will fail. Idempotent; revoking an
    already-revoked key is a 200 no-op.

    See WARNING on ``POST /v1/admin/api-keys``; this route is an
    operator route and must be protected by deployment infrastructure.

    Args:
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        api_key_id=api_key_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    api_key_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ApiKeyOut | ProblemResponse | None:
    """Revoke

     Revoke a previously-issued API key.

    Soft-delete: the row stays for audit, ``revoked_at`` is stamped
    and ``revoked=true`` shipped on the next read. Subsequent auth
    attempts with that key will fail. Idempotent; revoking an
    already-revoked key is a 200 no-op.

    See WARNING on ``POST /v1/admin/api-keys``; this route is an
    operator route and must be protected by deployment infrastructure.

    Args:
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyOut | ProblemResponse
    """

    return sync_detailed(
        api_key_id=api_key_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    api_key_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ApiKeyOut | ProblemResponse]:
    """Revoke

     Revoke a previously-issued API key.

    Soft-delete: the row stays for audit, ``revoked_at`` is stamped
    and ``revoked=true`` shipped on the next read. Subsequent auth
    attempts with that key will fail. Idempotent; revoking an
    already-revoked key is a 200 no-op.

    See WARNING on ``POST /v1/admin/api-keys``; this route is an
    operator route and must be protected by deployment infrastructure.

    Args:
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        api_key_id=api_key_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    api_key_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ApiKeyOut | ProblemResponse | None:
    """Revoke

     Revoke a previously-issued API key.

    Soft-delete: the row stays for audit, ``revoked_at`` is stamped
    and ``revoked=true`` shipped on the next read. Subsequent auth
    attempts with that key will fail. Idempotent; revoking an
    already-revoked key is a 200 no-op.

    See WARNING on ``POST /v1/admin/api-keys``; this route is an
    operator route and must be protected by deployment infrastructure.

    Args:
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyOut | ProblemResponse
    """

    return (
        await asyncio_detailed(
            api_key_id=api_key_id,
            client=client,
        )
    ).parsed
