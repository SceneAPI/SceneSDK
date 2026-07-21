from http import HTTPStatus
from io import BytesIO
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_response import ProblemResponse
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    image_id: str,
    *,
    size: int | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_size: int | None | Unset
    if isinstance(size, Unset):
        json_size = UNSET
    else:
        json_size = size
    params["size"] = json_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/images/{image_id}/thumbnail".format(
            image_id=quote(str(image_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> File | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

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
) -> Response[File | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    image_id: str,
    *,
    client: AuthenticatedClient | Client,
    size: int | None | Unset = UNSET,
) -> Response[File | ProblemResponse]:
    """Get Image Thumbnail

     JPEG thumbnail, max edge `size` (default 256, hard-cap from settings).

    Args:
        image_id (str):
        size (int | None | Unset): Max edge length in pixels.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File | ProblemResponse]
    """

    kwargs = _get_kwargs(
        image_id=image_id,
        size=size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    image_id: str,
    *,
    client: AuthenticatedClient | Client,
    size: int | None | Unset = UNSET,
) -> File | ProblemResponse | None:
    """Get Image Thumbnail

     JPEG thumbnail, max edge `size` (default 256, hard-cap from settings).

    Args:
        image_id (str):
        size (int | None | Unset): Max edge length in pixels.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File | ProblemResponse
    """

    return sync_detailed(
        image_id=image_id,
        client=client,
        size=size,
    ).parsed


async def asyncio_detailed(
    image_id: str,
    *,
    client: AuthenticatedClient | Client,
    size: int | None | Unset = UNSET,
) -> Response[File | ProblemResponse]:
    """Get Image Thumbnail

     JPEG thumbnail, max edge `size` (default 256, hard-cap from settings).

    Args:
        image_id (str):
        size (int | None | Unset): Max edge length in pixels.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File | ProblemResponse]
    """

    kwargs = _get_kwargs(
        image_id=image_id,
        size=size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    image_id: str,
    *,
    client: AuthenticatedClient | Client,
    size: int | None | Unset = UNSET,
) -> File | ProblemResponse | None:
    """Get Image Thumbnail

     JPEG thumbnail, max edge `size` (default 256, hard-cap from settings).

    Args:
        image_id (str):
        size (int | None | Unset): Max edge length in pixels.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File | ProblemResponse
    """

    return (
        await asyncio_detailed(
            image_id=image_id,
            client=client,
            size=size,
        )
    ).parsed
