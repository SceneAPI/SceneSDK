# scenesdk

Typed Python SDK for [sceneapi](https://github.com/SFMAPI/sfmapi): the
auto-generated `scenesdk` package, regenerated from the live
OpenAPI spec on every release. Package documentation, usage examples,
and the ergonomics-helper surface are described in
[`scenesdk/README.md`](scenesdk/README.md).

```bash
pip install scenesdk
```

```python
from scenesdk.client import Client
from scenesdk.api.capabilities import capabilities_v1_capabilities_get

client = Client(base_url="http://localhost:8080")
caps = capabilities_v1_capabilities_get.sync_detailed(client=client)
print(caps.parsed)  # CapabilitiesOut with schema_version, backend, features
```

`scenesdk._ergonomics` adds the helper surface on top of the
generated endpoint and model types: the typed `SfmApiError` exception
hierarchy, `supports()`, chunked upload (`upload_bytes` /
`upload_file`), the SSE event iterator (`stream_events`), the
`application/x-sfm-points-v1` parser, and the `wait_for_job` /
`submit_and_wait` / `submit_and_stream` job combinators.

## Layout

- `scenesdk/` — the distribution's self-contained build root
  (generated code + repo-owned metadata and `_ergonomics.py`). Release
  builds and publishes run from there.
- `pyproject.toml` (this directory) — dev-install root for the same
  `scenesdk` distribution: `pip install -e ".[dev]"` gives the
  generated package plus the test toolchain for `tests/`.

## History

The hand-rolled `sfmapi-client` package (sync + async clients plus the
`sfmapi-client` CLI) that used to live here was deprecated at 0.0.2 and
**removed at 0.1.0 as scheduled**, together with the sceneapi package
rename. Its full ergonomics surface lives on in
`scenesdk._ergonomics`.

## License

The Python SDK source and package are licensed under `Apache-2.0`; see
`LICENSE`.
