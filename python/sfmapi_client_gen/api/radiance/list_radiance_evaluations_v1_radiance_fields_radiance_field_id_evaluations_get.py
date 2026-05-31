from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.page_radiance_evaluation_out import PageRadianceEvaluationOut
from ...types import Response


def _get_kwargs(
    radiance_field_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/radiance_fields/{radiance_field_id}/evaluations".format(
            radiance_field_id=quote(str(radiance_field_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PageRadianceEvaluationOut | None:
    if response.status_code == 200:
        response_200 = PageRadianceEvaluationOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | PageRadianceEvaluationOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    radiance_field_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | PageRadianceEvaluationOut]:
    """List Radiance Evaluations

    Args:
        radiance_field_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PageRadianceEvaluationOut]
    """

    kwargs = _get_kwargs(
        radiance_field_id=radiance_field_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    radiance_field_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | PageRadianceEvaluationOut | None:
    """List Radiance Evaluations

    Args:
        radiance_field_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PageRadianceEvaluationOut
    """

    return sync_detailed(
        radiance_field_id=radiance_field_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    radiance_field_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | PageRadianceEvaluationOut]:
    """List Radiance Evaluations

    Args:
        radiance_field_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PageRadianceEvaluationOut]
    """

    kwargs = _get_kwargs(
        radiance_field_id=radiance_field_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    radiance_field_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | PageRadianceEvaluationOut | None:
    """List Radiance Evaluations

    Args:
        radiance_field_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PageRadianceEvaluationOut
    """

    return (
        await asyncio_detailed(
            radiance_field_id=radiance_field_id,
            client=client,
        )
    ).parsed
