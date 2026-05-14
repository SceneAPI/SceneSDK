from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_config_schema_out import BackendConfigSchemaOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    config_id: str,
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
        "url": "/v1/backend/config-schemas/{config_id}".format(
            config_id=quote(str(config_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BackendConfigSchemaOut | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = BackendConfigSchemaOut.from_dict(response.json())

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
) -> Response[BackendConfigSchemaOut | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    config_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> Response[BackendConfigSchemaOut | HTTPValidationError]:
    """Get Config Schema

     Read one backend-specific option schema.

    Args:
        config_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendConfigSchemaOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        config_id=config_id,
        provider=provider,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    config_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> BackendConfigSchemaOut | HTTPValidationError | None:
    """Get Config Schema

     Read one backend-specific option schema.

    Args:
        config_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendConfigSchemaOut | HTTPValidationError
    """

    return sync_detailed(
        config_id=config_id,
        client=client,
        provider=provider,
    ).parsed


async def asyncio_detailed(
    config_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> Response[BackendConfigSchemaOut | HTTPValidationError]:
    """Get Config Schema

     Read one backend-specific option schema.

    Args:
        config_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendConfigSchemaOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        config_id=config_id,
        provider=provider,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    config_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> BackendConfigSchemaOut | HTTPValidationError | None:
    """Get Config Schema

     Read one backend-specific option schema.

    Args:
        config_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendConfigSchemaOut | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            config_id=config_id,
            client=client,
            provider=provider,
        )
    ).parsed
