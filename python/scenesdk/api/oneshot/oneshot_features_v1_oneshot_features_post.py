from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.one_shot_features_response import OneShotFeaturesResponse
from ...models.oneshot_features_v1_oneshot_features_post_type import (
    OneshotFeaturesV1OneshotFeaturesPostType,
)
from ...models.problem_response import ProblemResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    type_: OneshotFeaturesV1OneshotFeaturesPostType
    | Unset = OneshotFeaturesV1OneshotFeaturesPostType.SIFT,
    provider: None | str | Unset = UNSET,
    max_num_features: int | Unset = 8192,
    use_gpu: bool | Unset = True,
    seed: int | Unset = 0,
    content_type: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(content_type, Unset):
        headers["Content-Type"] = content_type

    params: dict[str, Any] = {}

    json_type_: str | Unset = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    json_provider: None | str | Unset
    if isinstance(provider, Unset):
        json_provider = UNSET
    else:
        json_provider = provider
    params["provider"] = json_provider

    params["max_num_features"] = max_num_features

    params["use_gpu"] = use_gpu

    params["seed"] = seed

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/oneshot/features",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> OneShotFeaturesResponse | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = OneShotFeaturesResponse.from_dict(response.json())

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
) -> Response[OneShotFeaturesResponse | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    type_: OneshotFeaturesV1OneshotFeaturesPostType
    | Unset = OneshotFeaturesV1OneshotFeaturesPostType.SIFT,
    provider: None | str | Unset = UNSET,
    max_num_features: int | Unset = 8192,
    use_gpu: bool | Unset = True,
    seed: int | Unset = 0,
    content_type: None | str | Unset = UNSET,
) -> Response[OneShotFeaturesResponse | ProblemResponse]:
    """Oneshot Features

     Extract local features from a single image. Bytes-in /
    typed-result-out. No persistence.

    Mirrors the parameter set of :class:`FeaturesSpec`. The image
    bytes are read from the request body; the ``Content-Type`` header
    is used to choose a tempfile extension if present, else the
    bytes are sniffed.

    Returns the keypoints + base64-encoded float32 descriptors
    inline. For batch / multi-image / multi-stage flows, use the
    resource API instead.

    Args:
        type_ (OneshotFeaturesV1OneshotFeaturesPostType | Unset): Local feature extractor.
            Default: OneshotFeaturesV1OneshotFeaturesPostType.SIFT.
        provider (None | str | Unset): Optional provider id to execute this call.
        max_num_features (int | Unset):  Default: 8192.
        use_gpu (bool | Unset):  Default: True.
        seed (int | Unset):  Default: 0.
        content_type (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OneShotFeaturesResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        type_=type_,
        provider=provider,
        max_num_features=max_num_features,
        use_gpu=use_gpu,
        seed=seed,
        content_type=content_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    type_: OneshotFeaturesV1OneshotFeaturesPostType
    | Unset = OneshotFeaturesV1OneshotFeaturesPostType.SIFT,
    provider: None | str | Unset = UNSET,
    max_num_features: int | Unset = 8192,
    use_gpu: bool | Unset = True,
    seed: int | Unset = 0,
    content_type: None | str | Unset = UNSET,
) -> OneShotFeaturesResponse | ProblemResponse | None:
    """Oneshot Features

     Extract local features from a single image. Bytes-in /
    typed-result-out. No persistence.

    Mirrors the parameter set of :class:`FeaturesSpec`. The image
    bytes are read from the request body; the ``Content-Type`` header
    is used to choose a tempfile extension if present, else the
    bytes are sniffed.

    Returns the keypoints + base64-encoded float32 descriptors
    inline. For batch / multi-image / multi-stage flows, use the
    resource API instead.

    Args:
        type_ (OneshotFeaturesV1OneshotFeaturesPostType | Unset): Local feature extractor.
            Default: OneshotFeaturesV1OneshotFeaturesPostType.SIFT.
        provider (None | str | Unset): Optional provider id to execute this call.
        max_num_features (int | Unset):  Default: 8192.
        use_gpu (bool | Unset):  Default: True.
        seed (int | Unset):  Default: 0.
        content_type (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OneShotFeaturesResponse | ProblemResponse
    """

    return sync_detailed(
        client=client,
        type_=type_,
        provider=provider,
        max_num_features=max_num_features,
        use_gpu=use_gpu,
        seed=seed,
        content_type=content_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    type_: OneshotFeaturesV1OneshotFeaturesPostType
    | Unset = OneshotFeaturesV1OneshotFeaturesPostType.SIFT,
    provider: None | str | Unset = UNSET,
    max_num_features: int | Unset = 8192,
    use_gpu: bool | Unset = True,
    seed: int | Unset = 0,
    content_type: None | str | Unset = UNSET,
) -> Response[OneShotFeaturesResponse | ProblemResponse]:
    """Oneshot Features

     Extract local features from a single image. Bytes-in /
    typed-result-out. No persistence.

    Mirrors the parameter set of :class:`FeaturesSpec`. The image
    bytes are read from the request body; the ``Content-Type`` header
    is used to choose a tempfile extension if present, else the
    bytes are sniffed.

    Returns the keypoints + base64-encoded float32 descriptors
    inline. For batch / multi-image / multi-stage flows, use the
    resource API instead.

    Args:
        type_ (OneshotFeaturesV1OneshotFeaturesPostType | Unset): Local feature extractor.
            Default: OneshotFeaturesV1OneshotFeaturesPostType.SIFT.
        provider (None | str | Unset): Optional provider id to execute this call.
        max_num_features (int | Unset):  Default: 8192.
        use_gpu (bool | Unset):  Default: True.
        seed (int | Unset):  Default: 0.
        content_type (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OneShotFeaturesResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        type_=type_,
        provider=provider,
        max_num_features=max_num_features,
        use_gpu=use_gpu,
        seed=seed,
        content_type=content_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    type_: OneshotFeaturesV1OneshotFeaturesPostType
    | Unset = OneshotFeaturesV1OneshotFeaturesPostType.SIFT,
    provider: None | str | Unset = UNSET,
    max_num_features: int | Unset = 8192,
    use_gpu: bool | Unset = True,
    seed: int | Unset = 0,
    content_type: None | str | Unset = UNSET,
) -> OneShotFeaturesResponse | ProblemResponse | None:
    """Oneshot Features

     Extract local features from a single image. Bytes-in /
    typed-result-out. No persistence.

    Mirrors the parameter set of :class:`FeaturesSpec`. The image
    bytes are read from the request body; the ``Content-Type`` header
    is used to choose a tempfile extension if present, else the
    bytes are sniffed.

    Returns the keypoints + base64-encoded float32 descriptors
    inline. For batch / multi-image / multi-stage flows, use the
    resource API instead.

    Args:
        type_ (OneshotFeaturesV1OneshotFeaturesPostType | Unset): Local feature extractor.
            Default: OneshotFeaturesV1OneshotFeaturesPostType.SIFT.
        provider (None | str | Unset): Optional provider id to execute this call.
        max_num_features (int | Unset):  Default: 8192.
        use_gpu (bool | Unset):  Default: True.
        seed (int | Unset):  Default: 0.
        content_type (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OneShotFeaturesResponse | ProblemResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            type_=type_,
            provider=provider,
            max_num_features=max_num_features,
            use_gpu=use_gpu,
            seed=seed,
            content_type=content_type,
        )
    ).parsed
