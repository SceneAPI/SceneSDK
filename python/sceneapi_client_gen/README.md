# sceneapi-client

Auto-generated typed Python SDK for [sceneapi](https://github.com/SFMAPI/sfmapi)
(import package `sceneapi_client_gen`).

> **Generated** - do not hand-edit generated endpoint or model files.
> Update `openapi.json` from the server repo, then regenerate the SDK.

## Install

```bash
pip install sceneapi-client
```

## Usage

```python
from sceneapi_client_gen.client import Client
from sceneapi_client_gen.api.capabilities import capabilities_v1_capabilities_get

client = Client(base_url="http://localhost:8080")
caps_resp = capabilities_v1_capabilities_get.sync_detailed(client=client)
print(caps_resp.parsed)  # CapabilitiesOut with schema_version, backend, features
```

## The canonical SDK surface

This package is regenerated from the OpenAPI spec on every release. The
generated package is the canonical SDK surface; its
`sceneapi_client_gen._ergonomics` module adds helpers for common workflows
on top of the generated endpoint and model types.

The deprecated hand-rolled `sfmapi-client` package was removed at 0.1.0
as scheduled; its ergonomics surface (typed exceptions, `supports()`,
chunked upload, SSE streaming, points parsing, job combinators) is
reproduced in `sceneapi_client_gen._ergonomics`. The contract test
suite in the server repo replays recorded server responses through the
generated models so wire drift fails CI immediately.

## License

The generated Python SDK package is licensed under `Apache-2.0`; see
`LICENSE`.
