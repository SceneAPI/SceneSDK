from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.plugin_install_request import PluginInstallRequest
from ...models.plugin_install_response import PluginInstallResponse
from ...models.problem_response import ProblemResponse
from ...types import Response


def _get_kwargs(
    plugin_id: str,
    *,
    body: PluginInstallRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/admin/plugins/{plugin_id}:install".format(
            plugin_id=quote(str(plugin_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PluginInstallResponse | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = PluginInstallResponse.from_dict(response.json())

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
) -> Response[PluginInstallResponse | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    plugin_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PluginInstallRequest,
) -> Response[PluginInstallResponse | ProblemResponse]:
    """Install Plugin

     Plan or run an operator-scoped plugin install.

    Args:
        plugin_id (str):
        body (PluginInstallRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PluginInstallResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        plugin_id=plugin_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    plugin_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PluginInstallRequest,
) -> PluginInstallResponse | ProblemResponse | None:
    """Install Plugin

     Plan or run an operator-scoped plugin install.

    Args:
        plugin_id (str):
        body (PluginInstallRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PluginInstallResponse | ProblemResponse
    """

    return sync_detailed(
        plugin_id=plugin_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    plugin_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PluginInstallRequest,
) -> Response[PluginInstallResponse | ProblemResponse]:
    """Install Plugin

     Plan or run an operator-scoped plugin install.

    Args:
        plugin_id (str):
        body (PluginInstallRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PluginInstallResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        plugin_id=plugin_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    plugin_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PluginInstallRequest,
) -> PluginInstallResponse | ProblemResponse | None:
    """Install Plugin

     Plan or run an operator-scoped plugin install.

    Args:
        plugin_id (str):
        body (PluginInstallRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PluginInstallResponse | ProblemResponse
    """

    return (
        await asyncio_detailed(
            plugin_id=plugin_id,
            client=client,
            body=body,
        )
    ).parsed
