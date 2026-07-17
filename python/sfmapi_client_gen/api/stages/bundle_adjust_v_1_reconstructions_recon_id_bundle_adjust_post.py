from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bundle_adjustment_spec import BundleAdjustmentSpec
from ...models.job_accepted_response import JobAcceptedResponse
from ...models.problem_response import ProblemResponse
from ...types import Response


def _get_kwargs(
    recon_id: str,
    *,
    body: BundleAdjustmentSpec,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/reconstructions/{recon_id}:bundleAdjust".format(
            recon_id=quote(str(recon_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

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
    recon_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BundleAdjustmentSpec,
) -> Response[JobAcceptedResponse | ProblemResponse]:
    """Bundle Adjust

     Run standalone bundle adjustment over the reconstruction.

    ``mode`` selects the algorithm + gating capability (``ba.standard``
    / ``ba.two_stage`` / ``ba.featuremetric`` / ``ba.rig``).

    Args:
        recon_id (str):
        body (BundleAdjustmentSpec): Standalone bundle-adjustment spec.

            ``mode`` selects the algorithm:
              - ``standard``: a single ceres / baxx solve over all
                registered cameras + 3D points (capability ``ba.standard``).
              - ``two_stage``: a two-pass refinement (capability ``ba.two_stage``).
              - ``featuremetric``: Pixel-Perfect SfM-style refinement that
                minimizes a CNN-feature error, not raw reprojection
                (capability ``ba.featuremetric``). Requires a backend with
                learned-feature support.
              - ``rig``: rig-aware refinement that shares intrinsics + relative
                extrinsics across a multi-camera rig (capability ``ba.rig``).

            ``loss_kernel`` chooses the robust loss applied to per-residual
            cost: ``squared`` (no robustification), ``huber``, ``cauchy``,
            ``soft_l1``, ``tukey``. ``loss_threshold`` is the kernel scale
            (in pixels for reprojection loss).

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobAcceptedResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        recon_id=recon_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    recon_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BundleAdjustmentSpec,
) -> JobAcceptedResponse | ProblemResponse | None:
    """Bundle Adjust

     Run standalone bundle adjustment over the reconstruction.

    ``mode`` selects the algorithm + gating capability (``ba.standard``
    / ``ba.two_stage`` / ``ba.featuremetric`` / ``ba.rig``).

    Args:
        recon_id (str):
        body (BundleAdjustmentSpec): Standalone bundle-adjustment spec.

            ``mode`` selects the algorithm:
              - ``standard``: a single ceres / baxx solve over all
                registered cameras + 3D points (capability ``ba.standard``).
              - ``two_stage``: a two-pass refinement (capability ``ba.two_stage``).
              - ``featuremetric``: Pixel-Perfect SfM-style refinement that
                minimizes a CNN-feature error, not raw reprojection
                (capability ``ba.featuremetric``). Requires a backend with
                learned-feature support.
              - ``rig``: rig-aware refinement that shares intrinsics + relative
                extrinsics across a multi-camera rig (capability ``ba.rig``).

            ``loss_kernel`` chooses the robust loss applied to per-residual
            cost: ``squared`` (no robustification), ``huber``, ``cauchy``,
            ``soft_l1``, ``tukey``. ``loss_threshold`` is the kernel scale
            (in pixels for reprojection loss).

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobAcceptedResponse | ProblemResponse
    """

    return sync_detailed(
        recon_id=recon_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    recon_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BundleAdjustmentSpec,
) -> Response[JobAcceptedResponse | ProblemResponse]:
    """Bundle Adjust

     Run standalone bundle adjustment over the reconstruction.

    ``mode`` selects the algorithm + gating capability (``ba.standard``
    / ``ba.two_stage`` / ``ba.featuremetric`` / ``ba.rig``).

    Args:
        recon_id (str):
        body (BundleAdjustmentSpec): Standalone bundle-adjustment spec.

            ``mode`` selects the algorithm:
              - ``standard``: a single ceres / baxx solve over all
                registered cameras + 3D points (capability ``ba.standard``).
              - ``two_stage``: a two-pass refinement (capability ``ba.two_stage``).
              - ``featuremetric``: Pixel-Perfect SfM-style refinement that
                minimizes a CNN-feature error, not raw reprojection
                (capability ``ba.featuremetric``). Requires a backend with
                learned-feature support.
              - ``rig``: rig-aware refinement that shares intrinsics + relative
                extrinsics across a multi-camera rig (capability ``ba.rig``).

            ``loss_kernel`` chooses the robust loss applied to per-residual
            cost: ``squared`` (no robustification), ``huber``, ``cauchy``,
            ``soft_l1``, ``tukey``. ``loss_threshold`` is the kernel scale
            (in pixels for reprojection loss).

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobAcceptedResponse | ProblemResponse]
    """

    kwargs = _get_kwargs(
        recon_id=recon_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    recon_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BundleAdjustmentSpec,
) -> JobAcceptedResponse | ProblemResponse | None:
    """Bundle Adjust

     Run standalone bundle adjustment over the reconstruction.

    ``mode`` selects the algorithm + gating capability (``ba.standard``
    / ``ba.two_stage`` / ``ba.featuremetric`` / ``ba.rig``).

    Args:
        recon_id (str):
        body (BundleAdjustmentSpec): Standalone bundle-adjustment spec.

            ``mode`` selects the algorithm:
              - ``standard``: a single ceres / baxx solve over all
                registered cameras + 3D points (capability ``ba.standard``).
              - ``two_stage``: a two-pass refinement (capability ``ba.two_stage``).
              - ``featuremetric``: Pixel-Perfect SfM-style refinement that
                minimizes a CNN-feature error, not raw reprojection
                (capability ``ba.featuremetric``). Requires a backend with
                learned-feature support.
              - ``rig``: rig-aware refinement that shares intrinsics + relative
                extrinsics across a multi-camera rig (capability ``ba.rig``).

            ``loss_kernel`` chooses the robust loss applied to per-residual
            cost: ``squared`` (no robustification), ``huber``, ``cauchy``,
            ``soft_l1``, ``tukey``. ``loss_threshold`` is the kernel scale
            (in pixels for reprojection loss).

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobAcceptedResponse | ProblemResponse
    """

    return (
        await asyncio_detailed(
            recon_id=recon_id,
            client=client,
            body=body,
        )
    ).parsed
