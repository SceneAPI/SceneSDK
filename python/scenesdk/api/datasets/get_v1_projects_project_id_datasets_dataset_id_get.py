from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dataset_out import DatasetOut
from ...models.problem_response import ProblemResponse
from ...types import Response


def _get_kwargs(
    project_id: str,
    dataset_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/projects/{project_id}/datasets/{dataset_id}".format(
            project_id=quote(str(project_id), safe=""),
            dataset_id=quote(str(dataset_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DatasetOut | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = DatasetOut.from_dict(response.json())

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
) -> Response[DatasetOut | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[DatasetOut | ProblemResponse]:
    """Get

     Read a single dataset by id.

    422 ``ValidationError`` if the dataset belongs to a different
    project than the one in the path; 404 if it doesn't exist for
    this tenant at all.

    Args:
        project_id (str):
        dataset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> DatasetOut | ProblemResponse | None:
    """Get

     Read a single dataset by id.

    422 ``ValidationError`` if the dataset belongs to a different
    project than the one in the path; 404 if it doesn't exist for
    this tenant at all.

    Args:
        project_id (str):
        dataset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetOut | ProblemResponse
    """

    return sync_detailed(
        project_id=project_id,
        dataset_id=dataset_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[DatasetOut | ProblemResponse]:
    """Get

     Read a single dataset by id.

    422 ``ValidationError`` if the dataset belongs to a different
    project than the one in the path; 404 if it doesn't exist for
    this tenant at all.

    Args:
        project_id (str):
        dataset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> DatasetOut | ProblemResponse | None:
    """Get

     Read a single dataset by id.

    422 ``ValidationError`` if the dataset belongs to a different
    project than the one in the path; 404 if it doesn't exist for
    this tenant at all.

    Args:
        project_id (str):
        dataset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetOut | ProblemResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            dataset_id=dataset_id,
            client=client,
        )
    ).parsed
