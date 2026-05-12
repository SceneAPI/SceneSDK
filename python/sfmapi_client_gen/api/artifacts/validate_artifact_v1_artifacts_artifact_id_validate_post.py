from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.artifact_validation_out import ArtifactValidationOut
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    artifact_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/artifacts/{artifact_id}:validate".format(
            artifact_id=quote(str(artifact_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ArtifactValidationOut | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = ArtifactValidationOut.from_dict(response.json())

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
) -> Response[ArtifactValidationOut | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    artifact_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ArtifactValidationOut | HTTPValidationError]:
    """Validate Artifact

     Validate an artifact descriptor and any local server-managed bytes.

    Args:
        artifact_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArtifactValidationOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        artifact_id=artifact_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    artifact_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ArtifactValidationOut | HTTPValidationError | None:
    """Validate Artifact

     Validate an artifact descriptor and any local server-managed bytes.

    Args:
        artifact_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArtifactValidationOut | HTTPValidationError
    """

    return sync_detailed(
        artifact_id=artifact_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    artifact_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ArtifactValidationOut | HTTPValidationError]:
    """Validate Artifact

     Validate an artifact descriptor and any local server-managed bytes.

    Args:
        artifact_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArtifactValidationOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        artifact_id=artifact_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    artifact_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ArtifactValidationOut | HTTPValidationError | None:
    """Validate Artifact

     Validate an artifact descriptor and any local server-managed bytes.

    Args:
        artifact_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArtifactValidationOut | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            artifact_id=artifact_id,
            client=client,
        )
    ).parsed
