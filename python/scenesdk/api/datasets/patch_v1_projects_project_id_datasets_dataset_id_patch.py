from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dataset_out import DatasetOut
from ...models.dataset_patch import DatasetPatch
from ...models.problem_response import ProblemResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    dataset_id: str,
    *,
    body: DatasetPatch,
    update_mask: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_update_mask: None | str | Unset
    if isinstance(update_mask, Unset):
        json_update_mask = UNSET
    else:
        json_update_mask = update_mask
    params["update_mask"] = json_update_mask

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/projects/{project_id}/datasets/{dataset_id}".format(
            project_id=quote(str(project_id), safe=""),
            dataset_id=quote(str(dataset_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: DatasetPatch,
    update_mask: None | str | Unset = UNSET,
) -> Response[DatasetOut | ProblemResponse]:
    """Patch

     Partially update a dataset.

    Without ``update_mask``, only fields present in the request body
    are written. With ``update_mask``, only the named field paths are
    applied and they must also be present in the body.

    The dataset's ``source_id`` is immutable; to change image inputs,
    create a new dataset. 422 if the row exists but belongs to another project.

    Args:
        project_id (str):
        dataset_id (str):
        update_mask (None | str | Unset): Optional AIP-161 comma-separated field mask. Allowed
            paths: name, camera_model, intrinsics_mode, is_spherical, rig_config,
            respect_exif_orientation, active_maskset_id.
        body (DatasetPatch): Partial update. Unset fields are left untouched. The dataset's
            `source_id` is immutable — to change images, create a new dataset.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
        body=body,
        update_mask=update_mask,
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
    body: DatasetPatch,
    update_mask: None | str | Unset = UNSET,
) -> DatasetOut | ProblemResponse | None:
    """Patch

     Partially update a dataset.

    Without ``update_mask``, only fields present in the request body
    are written. With ``update_mask``, only the named field paths are
    applied and they must also be present in the body.

    The dataset's ``source_id`` is immutable; to change image inputs,
    create a new dataset. 422 if the row exists but belongs to another project.

    Args:
        project_id (str):
        dataset_id (str):
        update_mask (None | str | Unset): Optional AIP-161 comma-separated field mask. Allowed
            paths: name, camera_model, intrinsics_mode, is_spherical, rig_config,
            respect_exif_orientation, active_maskset_id.
        body (DatasetPatch): Partial update. Unset fields are left untouched. The dataset's
            `source_id` is immutable — to change images, create a new dataset.

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
        body=body,
        update_mask=update_mask,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DatasetPatch,
    update_mask: None | str | Unset = UNSET,
) -> Response[DatasetOut | ProblemResponse]:
    """Patch

     Partially update a dataset.

    Without ``update_mask``, only fields present in the request body
    are written. With ``update_mask``, only the named field paths are
    applied and they must also be present in the body.

    The dataset's ``source_id`` is immutable; to change image inputs,
    create a new dataset. 422 if the row exists but belongs to another project.

    Args:
        project_id (str):
        dataset_id (str):
        update_mask (None | str | Unset): Optional AIP-161 comma-separated field mask. Allowed
            paths: name, camera_model, intrinsics_mode, is_spherical, rig_config,
            respect_exif_orientation, active_maskset_id.
        body (DatasetPatch): Partial update. Unset fields are left untouched. The dataset's
            `source_id` is immutable — to change images, create a new dataset.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetOut | ProblemResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
        body=body,
        update_mask=update_mask,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DatasetPatch,
    update_mask: None | str | Unset = UNSET,
) -> DatasetOut | ProblemResponse | None:
    """Patch

     Partially update a dataset.

    Without ``update_mask``, only fields present in the request body
    are written. With ``update_mask``, only the named field paths are
    applied and they must also be present in the body.

    The dataset's ``source_id`` is immutable; to change image inputs,
    create a new dataset. 422 if the row exists but belongs to another project.

    Args:
        project_id (str):
        dataset_id (str):
        update_mask (None | str | Unset): Optional AIP-161 comma-separated field mask. Allowed
            paths: name, camera_model, intrinsics_mode, is_spherical, rig_config,
            respect_exif_orientation, active_maskset_id.
        body (DatasetPatch): Partial update. Unset fields are left untouched. The dataset's
            `source_id` is immutable — to change images, create a new dataset.

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
            body=body,
            update_mask=update_mask,
        )
    ).parsed
