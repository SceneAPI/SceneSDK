from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_response import ProblemResponse
from ...models.upload_finalize_request import UploadFinalizeRequest
from ...models.upload_out import UploadOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    upload_id: str,
    *,
    body: UploadFinalizeRequest | Unset = UNSET,
    x_content_sha256: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_content_sha256, Unset):
        headers["X-Content-SHA256"] = x_content_sha256

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/uploads/{upload_id}:finalize".format(
            upload_id=quote(str(upload_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

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
    body: UploadFinalizeRequest | Unset = UNSET,
    x_content_sha256: None | str | Unset = UNSET,
) -> Response[ProblemResponse | UploadOut]:
    """Finalize

     Seal an upload — verify the assembled bytes match the
    expected size and (when supplied) ``X-Content-SHA256``, then
    transition the row to ``finalized`` with the canonical
    ``blob_sha``. AIP-136 ``:finalize`` colon verb (the operation
    has side effects beyond a Standard Update).

    Args:
        upload_id (str):
        x_content_sha256 (None | str | Unset):
        body (UploadFinalizeRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | UploadOut]
    """

    kwargs = _get_kwargs(
        upload_id=upload_id,
        body=body,
        x_content_sha256=x_content_sha256,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    upload_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UploadFinalizeRequest | Unset = UNSET,
    x_content_sha256: None | str | Unset = UNSET,
) -> ProblemResponse | UploadOut | None:
    """Finalize

     Seal an upload — verify the assembled bytes match the
    expected size and (when supplied) ``X-Content-SHA256``, then
    transition the row to ``finalized`` with the canonical
    ``blob_sha``. AIP-136 ``:finalize`` colon verb (the operation
    has side effects beyond a Standard Update).

    Args:
        upload_id (str):
        x_content_sha256 (None | str | Unset):
        body (UploadFinalizeRequest | Unset):

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
        x_content_sha256=x_content_sha256,
    ).parsed


async def asyncio_detailed(
    upload_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UploadFinalizeRequest | Unset = UNSET,
    x_content_sha256: None | str | Unset = UNSET,
) -> Response[ProblemResponse | UploadOut]:
    """Finalize

     Seal an upload — verify the assembled bytes match the
    expected size and (when supplied) ``X-Content-SHA256``, then
    transition the row to ``finalized`` with the canonical
    ``blob_sha``. AIP-136 ``:finalize`` colon verb (the operation
    has side effects beyond a Standard Update).

    Args:
        upload_id (str):
        x_content_sha256 (None | str | Unset):
        body (UploadFinalizeRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemResponse | UploadOut]
    """

    kwargs = _get_kwargs(
        upload_id=upload_id,
        body=body,
        x_content_sha256=x_content_sha256,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    upload_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UploadFinalizeRequest | Unset = UNSET,
    x_content_sha256: None | str | Unset = UNSET,
) -> ProblemResponse | UploadOut | None:
    """Finalize

     Seal an upload — verify the assembled bytes match the
    expected size and (when supplied) ``X-Content-SHA256``, then
    transition the row to ``finalized`` with the canonical
    ``blob_sha``. AIP-136 ``:finalize`` colon verb (the operation
    has side effects beyond a Standard Update).

    Args:
        upload_id (str):
        x_content_sha256 (None | str | Unset):
        body (UploadFinalizeRequest | Unset):

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
            x_content_sha256=x_content_sha256,
        )
    ).parsed
