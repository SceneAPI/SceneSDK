# sfmapi-client-gen

Auto-generated typed Python SDK for [sfmapi](https://github.com/SFMAPI/sfmapi).

> **Generated** - do not hand-edit generated endpoint or model files.
> Update `openapi.json` from the server repo, then regenerate the SDK.

## Install

```bash
pip install sfmapi-client-gen
```

## Usage

```python
from sfmapi_client_gen.client import Client
from sfmapi_client_gen.api.capabilities import capabilities_v1_capabilities_get

client = Client(base_url="http://localhost:8080")
caps_resp = capabilities_v1_capabilities_get.sync_detailed(client=client)
print(caps_resp.parsed)  # CapabilitiesOut with schema_version, backend, features
```

## Versus the hand-rolled `sfmapi-client`

This package is regenerated from the OpenAPI spec on every release. The
hand-rolled `sfmapi-client` package adds ergonomic helpers such as typed
errors, binary parsers, SSE event iterators, and sync/async parity. Use
the generated client for raw typed access; use the hand-rolled client
when you want the ergonomic surface.

Both decode identical wire formats. The contract test suite in the
server repo replays recorded server responses through both.

## License

The generated Python SDK package is licensed under `Apache-2.0`; see
`LICENSE`.
