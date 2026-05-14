from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.job_accepted_response import JobAcceptedResponse
from ...models.similarity_build_response import SimilarityBuildResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dataset_id: str,
    *,
    strategy: str | Unset = "dhash",
    force: bool | Unset = True,
    provider: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["strategy"] = strategy

    params["force"] = force

    json_provider: None | str | Unset
    if isinstance(provider, Unset):
        json_provider = UNSET
    else:
        json_provider = provider
    params["provider"] = json_provider

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/datasets/{dataset_id}/similarity:build".format(
            dataset_id=quote(str(dataset_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse | None:
    if response.status_code == 200:
        response_200 = SimilarityBuildResponse.from_dict(response.json())

        return response_200

    if response.status_code == 202:
        response_202 = JobAcceptedResponse.from_dict(response.json())

        return response_202

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    strategy: str | Unset = "dhash",
    force: bool | Unset = True,
    provider: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse]:
    """Build

     Build (or rebuild) the similarity index for the dataset.

    `dhash` builds synchronously using the optional image-processing
    dependency. `vlad` enqueues a worker job (requires pycolmap + SIFT
    extraction per image) and returns ``202`` with a `Location` header
    pointing at the job.

    Args:
        dataset_id (str):
        strategy (str | Unset):  Default: 'dhash'.
        force (bool | Unset):  Default: True.
        provider (None | str | Unset): Optional provider id to execute a vlad build job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        strategy=strategy,
        force=force,
        provider=provider,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    strategy: str | Unset = "dhash",
    force: bool | Unset = True,
    provider: None | str | Unset = UNSET,
) -> HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse | None:
    """Build

     Build (or rebuild) the similarity index for the dataset.

    `dhash` builds synchronously using the optional image-processing
    dependency. `vlad` enqueues a worker job (requires pycolmap + SIFT
    extraction per image) and returns ``202`` with a `Location` header
    pointing at the job.

    Args:
        dataset_id (str):
        strategy (str | Unset):  Default: 'dhash'.
        force (bool | Unset):  Default: True.
        provider (None | str | Unset): Optional provider id to execute a vlad build job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse
    """

    return sync_detailed(
        dataset_id=dataset_id,
        client=client,
        strategy=strategy,
        force=force,
        provider=provider,
    ).parsed


async def asyncio_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    strategy: str | Unset = "dhash",
    force: bool | Unset = True,
    provider: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse]:
    """Build

     Build (or rebuild) the similarity index for the dataset.

    `dhash` builds synchronously using the optional image-processing
    dependency. `vlad` enqueues a worker job (requires pycolmap + SIFT
    extraction per image) and returns ``202`` with a `Location` header
    pointing at the job.

    Args:
        dataset_id (str):
        strategy (str | Unset):  Default: 'dhash'.
        force (bool | Unset):  Default: True.
        provider (None | str | Unset): Optional provider id to execute a vlad build job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        strategy=strategy,
        force=force,
        provider=provider,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    strategy: str | Unset = "dhash",
    force: bool | Unset = True,
    provider: None | str | Unset = UNSET,
) -> HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse | None:
    """Build

     Build (or rebuild) the similarity index for the dataset.

    `dhash` builds synchronously using the optional image-processing
    dependency. `vlad` enqueues a worker job (requires pycolmap + SIFT
    extraction per image) and returns ``202`` with a `Location` header
    pointing at the job.

    Args:
        dataset_id (str):
        strategy (str | Unset):  Default: 'dhash'.
        force (bool | Unset):  Default: True.
        provider (None | str | Unset): Optional provider id to execute a vlad build job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | JobAcceptedResponse | SimilarityBuildResponse
    """

    return (
        await asyncio_detailed(
            dataset_id=dataset_id,
            client=client,
            strategy=strategy,
            force=force,
            provider=provider,
        )
    ).parsed
