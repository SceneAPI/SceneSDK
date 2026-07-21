from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_artifact_contract_out import BackendArtifactContractOut
from ...models.problem_response import ProblemResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    contract_id: str,
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
        "url": "/v1/backend/artifact-contracts/{contract_id}".format(
            contract_id=quote(str(contract_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BackendArtifactContractOut | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = BackendArtifactContractOut.from_dict(response.json())

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
) -> Response[BackendArtifactContractOut | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    contract_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> Response[BackendArtifactContractOut | ProblemResponse]:
    """Get Artifact Contract

     Read one backend artifact input/output contract.

    Args:
        contract_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendArtifactContractOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        contract_id=contract_id,
        provider=provider,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    contract_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> BackendArtifactContractOut | ProblemResponse | None:
    """Get Artifact Contract

     Read one backend artifact input/output contract.

    Args:
        contract_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendArtifactContractOut | ProblemResponse
    """

    return sync_detailed(
        contract_id=contract_id,
        client=client,
        provider=provider,
    ).parsed


async def asyncio_detailed(
    contract_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> Response[BackendArtifactContractOut | ProblemResponse]:
    """Get Artifact Contract

     Read one backend artifact input/output contract.

    Args:
        contract_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendArtifactContractOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        contract_id=contract_id,
        provider=provider,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    contract_id: str,
    *,
    client: AuthenticatedClient | Client,
    provider: None | str | Unset = UNSET,
) -> BackendArtifactContractOut | ProblemResponse | None:
    """Get Artifact Contract

     Read one backend artifact input/output contract.

    Args:
        contract_id (str):
        provider (None | str | Unset): Optional provider id to inspect.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendArtifactContractOut | ProblemResponse
    """

    return (
        await asyncio_detailed(
            contract_id=contract_id,
            client=client,
            provider=provider,
        )
    ).parsed
