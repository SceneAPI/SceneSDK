from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cubemap_projection_request import CubemapProjectionRequest
from ...models.job_accepted_response import JobAcceptedResponse
from ...models.problem_response import ProblemResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dataset_id: str,
    *,
    body: CubemapProjectionRequest | None | Unset = UNSET,
    face_size: int | None | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_face_size: int | None | Unset
    if isinstance(face_size, Unset):
        json_face_size = UNSET
    else:
        json_face_size = face_size
    params["face_size"] = json_face_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/datasets/{dataset_id}:render_cubemap".format(
            dataset_id=quote(str(dataset_id), safe=""),
        ),
        "params": params,
    }

    if isinstance(body, CubemapProjectionRequest):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> JobAcceptedResponse | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 202:
        response_202 = JobAcceptedResponse.from_dict(response.json())

        return response_202

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
) -> Response[JobAcceptedResponse | ProblemResponse]:
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
    body: CubemapProjectionRequest | None | Unset = UNSET,
    face_size: int | None | Unset = UNSET,
) -> Response[JobAcceptedResponse | ProblemResponse]:
    """Render Cubemap

     Render every spherical panorama in this dataset into 6 cubemap faces.

    Requires the dataset to be marked ``is_spherical=true``. The
    output directory is returned in the task result; clients can then
    register it as a new ``local`` source for downstream pinhole-only
    pipelines.

    Args:
        dataset_id (str):
        face_size (int | None | Unset): Pixel edge length per cubemap face
        body (CubemapProjectionRequest | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobAcceptedResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        body=body,
        face_size=face_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CubemapProjectionRequest | None | Unset = UNSET,
    face_size: int | None | Unset = UNSET,
) -> JobAcceptedResponse | ProblemResponse | None:
    """Render Cubemap

     Render every spherical panorama in this dataset into 6 cubemap faces.

    Requires the dataset to be marked ``is_spherical=true``. The
    output directory is returned in the task result; clients can then
    register it as a new ``local`` source for downstream pinhole-only
    pipelines.

    Args:
        dataset_id (str):
        face_size (int | None | Unset): Pixel edge length per cubemap face
        body (CubemapProjectionRequest | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobAcceptedResponse | ProblemResponse
    """

    return sync_detailed(
        dataset_id=dataset_id,
        client=client,
        body=body,
        face_size=face_size,
    ).parsed


async def asyncio_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CubemapProjectionRequest | None | Unset = UNSET,
    face_size: int | None | Unset = UNSET,
) -> Response[JobAcceptedResponse | ProblemResponse]:
    """Render Cubemap

     Render every spherical panorama in this dataset into 6 cubemap faces.

    Requires the dataset to be marked ``is_spherical=true``. The
    output directory is returned in the task result; clients can then
    register it as a new ``local`` source for downstream pinhole-only
    pipelines.

    Args:
        dataset_id (str):
        face_size (int | None | Unset): Pixel edge length per cubemap face
        body (CubemapProjectionRequest | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobAcceptedResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        body=body,
        face_size=face_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CubemapProjectionRequest | None | Unset = UNSET,
    face_size: int | None | Unset = UNSET,
) -> JobAcceptedResponse | ProblemResponse | None:
    """Render Cubemap

     Render every spherical panorama in this dataset into 6 cubemap faces.

    Requires the dataset to be marked ``is_spherical=true``. The
    output directory is returned in the task result; clients can then
    register it as a new ``local`` source for downstream pinhole-only
    pipelines.

    Args:
        dataset_id (str):
        face_size (int | None | Unset): Pixel edge length per cubemap face
        body (CubemapProjectionRequest | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobAcceptedResponse | ProblemResponse
    """

    return (
        await asyncio_detailed(
            dataset_id=dataset_id,
            client=client,
            body=body,
            face_size=face_size,
        )
    ).parsed
