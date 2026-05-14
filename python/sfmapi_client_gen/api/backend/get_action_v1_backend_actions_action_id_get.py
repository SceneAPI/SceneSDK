from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_action_out import BackendActionOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    action_id: str,
    *,
    provider: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_provider: None | str | Unset
    if isinstance(provider, Unset):
        json_provider = UNSET
    else:
        json_provider = provider
    params["provider"] = json_provider

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/backend/actions/{action_id}".format(
            action_id=quote(str(action_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BackendActionOut | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = BackendActionOut.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BackendActionOut | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    action_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> Response[BackendActionOut | HTTPValidationError]:
    """Get Action

     Read one backend action descriptor including schemas.

    Args:
        action_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendActionOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        action_id=action_id,
        provider=provider,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    action_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> BackendActionOut | HTTPValidationError | None:
    """Get Action

     Read one backend action descriptor including schemas.

    Args:
        action_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendActionOut | HTTPValidationError
    """

    return sync_detailed(
        action_id=action_id,
        client=client,
        provider=provider,
    ).parsed


async def asyncio_detailed(
    action_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> Response[BackendActionOut | HTTPValidationError]:
    """Get Action

     Read one backend action descriptor including schemas.

    Args:
        action_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendActionOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        action_id=action_id,
        provider=provider,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    action_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> BackendActionOut | HTTPValidationError | None:
    """Get Action

     Read one backend action descriptor including schemas.

    Args:
        action_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendActionOut | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            action_id=action_id,
            client=client,
            provider=provider,
        )
    ).parsed
