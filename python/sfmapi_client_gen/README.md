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
generated package is the canonical SDK surface; its
`sfmapi_client_gen._ergonomics` module adds helpers for common workflows
on top of the generated endpoint and model types.

The hand-rolled `sfmapi-client` package remains for compatibility and
migration support. Prefer the generated client for new code.

Both decode identical wire formats. The contract test suite in the
server repo replays recorded server responses through both.

## License

The generated Python SDK package is licensed under `Apache-2.0`; see
`LICENSE`.
