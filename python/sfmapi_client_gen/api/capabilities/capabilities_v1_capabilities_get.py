from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.capabilities_out import CapabilitiesOut
from ...models.problem_response import ProblemResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/capabilities",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CapabilitiesOut | ProblemResponse | None:
    if response.status_code >= 400 and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)

    if response.status_code == 200:
        response_200 = CapabilitiesOut.from_dict(response.json())

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
) -> Response[CapabilitiesOut | ProblemResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[CapabilitiesOut | ProblemResponse]:
    """Capabilities

     Discovery: backend identity + feature flags this deployment exposes.

    Clients MUST hit this once at startup and cache the result for
    the duration of the connection. Use it to gate UI affordances and
    short-circuit against a 501 round-trip on unsupported operations.

    Feature names
    -------------
    The ``features`` map keys are dot-notated, mirroring AIP-style
    capability namespaces:

    - ``features.extract.{type}`` — feature extractor types
      (``sift`` | ``superpoint`` | ``aliked`` | ...).
    - ``matchers.{type}`` — per-pair matcher implementations.
    - ``pairs.{strategy}`` — pair-selection strategies
      (``exhaustive`` | ``vocabtree`` | ``retrieval`` | ...).
    - ``map.{kind}`` — mapping stages (``incremental`` |
      ``global`` | ``hierarchical`` | ``spherical``).
    - ``ba.{mode}`` — bundle-adjustment modes.
    - ``projection.{kind}``, ``georegister.{mode}``, the closed radiance
      keys (``radiance.train``, ``radiance.evaluate``,
      ``radiance.metrics.psnr``, ``radiance.metrics.ssim``,
      ``radiance.metrics.lpips``), and other closed sfmapi namespaces.

    Backend-native or out-of-scope commands such as dense MVS and mesh
    generation are exposed through ``/v1/backend/actions``, not as
    portable capability families.

    Absence rule
    ------------
    A feature key absent from the map means **unsupported** by this
    deployment. Endpoints that require an unsupported feature return
    ``501 capability_unavailable`` with the canonical name in
    ``capability``. Never assume unlisted keys are ``true``; SDK shims
    use :func:`supports(name)` (Python / TS / C++) which checks for
    the exact key + truthy value.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CapabilitiesOut | ProblemResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> CapabilitiesOut | ProblemResponse | None:
    """Capabilities

     Discovery: backend identity + feature flags this deployment exposes.

    Clients MUST hit this once at startup and cache the result for
    the duration of the connection. Use it to gate UI affordances and
    short-circuit against a 501 round-trip on unsupported operations.

    Feature names
    -------------
    The ``features`` map keys are dot-notated, mirroring AIP-style
    capability namespaces:

    - ``features.extract.{type}`` — feature extractor types
      (``sift`` | ``superpoint`` | ``aliked`` | ...).
    - ``matchers.{type}`` — per-pair matcher implementations.
    - ``pairs.{strategy}`` — pair-selection strategies
      (``exhaustive`` | ``vocabtree`` | ``retrieval`` | ...).
    - ``map.{kind}`` — mapping stages (``incremental`` |
      ``global`` | ``hierarchical`` | ``spherical``).
    - ``ba.{mode}`` — bundle-adjustment modes.
    - ``projection.{kind}``, ``georegister.{mode}``, the closed radiance
      keys (``radiance.train``, ``radiance.evaluate``,
      ``radiance.metrics.psnr``, ``radiance.metrics.ssim``,
      ``radiance.metrics.lpips``), and other closed sfmapi namespaces.

    Backend-native or out-of-scope commands such as dense MVS and mesh
    generation are exposed through ``/v1/backend/actions``, not as
    portable capability families.

    Absence rule
    ------------
    A feature key absent from the map means **unsupported** by this
    deployment. Endpoints that require an unsupported feature return
    ``501 capability_unavailable`` with the canonical name in
    ``capability``. Never assume unlisted keys are ``true``; SDK shims
    use :func:`supports(name)` (Python / TS / C++) which checks for
    the exact key + truthy value.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CapabilitiesOut | ProblemResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[CapabilitiesOut | ProblemResponse]:
    """Capabilities

     Discovery: backend identity + feature flags this deployment exposes.

    Clients MUST hit this once at startup and cache the result for
    the duration of the connection. Use it to gate UI affordances and
    short-circuit against a 501 round-trip on unsupported operations.

    Feature names
    -------------
    The ``features`` map keys are dot-notated, mirroring AIP-style
    capability namespaces:

    - ``features.extract.{type}`` — feature extractor types
      (``sift`` | ``superpoint`` | ``aliked`` | ...).
    - ``matchers.{type}`` — per-pair matcher implementations.
    - ``pairs.{strategy}`` — pair-selection strategies
      (``exhaustive`` | ``vocabtree`` | ``retrieval`` | ...).
    - ``map.{kind}`` — mapping stages (``incremental`` |
      ``global`` | ``hierarchical`` | ``spherical``).
    - ``ba.{mode}`` — bundle-adjustment modes.
    - ``projection.{kind}``, ``georegister.{mode}``, the closed radiance
      keys (``radiance.train``, ``radiance.evaluate``,
      ``radiance.metrics.psnr``, ``radiance.metrics.ssim``,
      ``radiance.metrics.lpips``), and other closed sfmapi namespaces.

    Backend-native or out-of-scope commands such as dense MVS and mesh
    generation are exposed through ``/v1/backend/actions``, not as
    portable capability families.

    Absence rule
    ------------
    A feature key absent from the map means **unsupported** by this
    deployment. Endpoints that require an unsupported feature return
    ``501 capability_unavailable`` with the canonical name in
    ``capability``. Never assume unlisted keys are ``true``; SDK shims
    use :func:`supports(name)` (Python / TS / C++) which checks for
    the exact key + truthy value.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CapabilitiesOut | ProblemResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> CapabilitiesOut | ProblemResponse | None:
    """Capabilities

     Discovery: backend identity + feature flags this deployment exposes.

    Clients MUST hit this once at startup and cache the result for
    the duration of the connection. Use it to gate UI affordances and
    short-circuit against a 501 round-trip on unsupported operations.

    Feature names
    -------------
    The ``features`` map keys are dot-notated, mirroring AIP-style
    capability namespaces:

    - ``features.extract.{type}`` — feature extractor types
      (``sift`` | ``superpoint`` | ``aliked`` | ...).
    - ``matchers.{type}`` — per-pair matcher implementations.
    - ``pairs.{strategy}`` — pair-selection strategies
      (``exhaustive`` | ``vocabtree`` | ``retrieval`` | ...).
    - ``map.{kind}`` — mapping stages (``incremental`` |
      ``global`` | ``hierarchical`` | ``spherical``).
    - ``ba.{mode}`` — bundle-adjustment modes.
    - ``projection.{kind}``, ``georegister.{mode}``, the closed radiance
      keys (``radiance.train``, ``radiance.evaluate``,
      ``radiance.metrics.psnr``, ``radiance.metrics.ssim``,
      ``radiance.metrics.lpips``), and other closed sfmapi namespaces.

    Backend-native or out-of-scope commands such as dense MVS and mesh
    generation are exposed through ``/v1/backend/actions``, not as
    portable capability families.

    Absence rule
    ------------
    A feature key absent from the map means **unsupported** by this
    deployment. Endpoints that require an unsupported feature return
    ``501 capability_unavailable`` with the canonical name in
    ``capability``. Never assume unlisted keys are ``true``; SDK shims
    use :func:`supports(name)` (Python / TS / C++) which checks for
    the exact key + truthy value.

    Raises:
        errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CapabilitiesOut | ProblemResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
