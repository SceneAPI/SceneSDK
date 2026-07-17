# sceneapi SDKs

Client SDK repository for sceneapi. The server, wire specification, plugin
hub, backend interfaces, and conformance tests live in
[`SFMAPI/sfmapi`](https://github.com/SFMAPI/sfmapi).

This repository is client-only:

- `python/sceneapi_client_gen/`: **supported** generated Python SDK
  (dist `sceneapi-client`, import `sceneapi_client_gen`; covers the full
  surface including radiance, backend actions, config-schemas, and the
  latest pipeline specs). The deprecated hand-written `sfmapi_client`
  compatibility SDK (and its CLI) was removed at 0.1.0 as scheduled.
- `typescript/`: browser and Node TypeScript SDK (`@sceneapi/client`).
- `cpp/`: header-only C++17 client helpers.
- `openapi.json`: OpenAPI snapshot used to regenerate clients.

## Commands

```bash
cd python
uv run pytest -q

cd ../typescript
npm test
npm run lint
npm run build

cd ../cpp
cmake -S . -B build
cmake --build build
ctest --test-dir build
```

Backend plugins should depend on `sceneapi`, not this SDK package. This repo
is for clients that call an existing sceneapi server.

## Regeneration

The server repo owns the OpenAPI contract. From `sfmapi`, run:

```bash
uv run python scripts/regen_sdk.py
```

That dumps the server OpenAPI document, copies it here as `openapi.json`,
and regenerates the Python and TypeScript clients. If `openapi.json` is
already current in this repo, regenerate locally with:

```bash
python scripts/regen_from_openapi.py
```

## License

The SDK source in this repository is licensed under `Apache-2.0`.
Each published package carries the same license metadata and a local copy
of the license text from this repository.
