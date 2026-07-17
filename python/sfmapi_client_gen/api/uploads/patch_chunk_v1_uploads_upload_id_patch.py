from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_response import ProblemResponse
from ...models.upload_out import UploadOut
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    upload_id: str,
    *,
    body: File,
    content_range: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(content_range, Unset):
        headers["Content-Range"] = content_range

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/uploads/{upload_id}".format(
            upload_id=quote(str(upload_id), safe=""),
        ),
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemResponse | UploadOut | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = UploadOut.from_dict(response.json())

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
) -> Response[ProblemResponse | UploadOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    upload_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: File,
    content_range: None | str | Unset = UNSET,
) -> Response[ProblemResponse | UploadOut]:
    """Patch Chunk

     Append one chunk of bytes to the upload.

    Requires ``Content-Range: bytes <start>-<end>/<total>`` (RFC 7233);
    the body length MUST equal the byte range. 422
    ``ValidationError`` on malformed Content-Range or length mismatch.
    To retry after a lost response, first read upload status and resume
    at ``received_bytes``; already-committed offsets are rejected as
    out of order.

    Args:
        upload_id (str):
        content_range (None | str | Unset):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | UploadOut]
    """

    kwargs = _get_kwargs(
        upload_id=upload_id,
        body=body,
        content_range=content_range,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    upload_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: File,
    content_range: None | str | Unset = UNSET,
) -> ProblemResponse | UploadOut | None:
    """Patch Chunk

     Append one chunk of bytes to the upload.

    Requires ``Content-Range: bytes <start>-<end>/<total>`` (RFC 7233);
    the body length MUST equal the byte range. 422
    ``ValidationError`` on malformed Content-Range or length mismatch.
    To retry after a lost response, first read upload status and resume
    at ``received_bytes``; already-committed offsets are rejected as
    out of order.

    Args:
        upload_id (str):
        content_range (None | str | Unset):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | UploadOut
    """

    return sync_detailed(
        upload_id=upload_id,
        client=client,
        body=body,
        content_range=content_range,
    ).parsed


async def asyncio_detailed(
    upload_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: File,
    content_range: None | str | Unset = UNSET,
) -> Response[ProblemResponse | UploadOut]:
    """Patch Chunk

     Append one chunk of bytes to the upload.

    Requires ``Content-Range: bytes <start>-<end>/<total>`` (RFC 7233);
    the body length MUST equal the byte range. 422
    ``ValidationError`` on malformed Content-Range or length mismatch.
    To retry after a lost response, first read upload status and resume
    at ``received_bytes``; already-committed offsets are rejected as
    out of order.

    Args:
        upload_id (str):
        content_range (None | str | Unset):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | UploadOut]
    """

    kwargs = _get_kwargs(
        upload_id=upload_id,
        body=body,
        content_range=content_range,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    upload_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: File,
    content_range: None | str | Unset = UNSET,
) -> ProblemResponse | UploadOut | None:
    """Patch Chunk

     Append one chunk of bytes to the upload.

    Requires ``Content-Range: bytes <start>-<end>/<total>`` (RFC 7233);
    the body length MUST equal the byte range. 422
    ``ValidationError`` on malformed Content-Range or length mismatch.
    To retry after a lost response, first read upload status and resume
    at ``received_bytes``; already-committed offsets are rejected as
    out of order.

    Args:
        upload_id (str):
        content_range (None | str | Unset):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemResponse | UploadOut
    """

    return (
        await asyncio_detailed(
            upload_id=upload_id,
            client=client,
            body=body,
            content_range=content_range,
        )
    ).parsed
