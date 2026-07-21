# @scenesdk/client

Typed TypeScript SDK for [sceneapi](https://github.com/SFMAPI/sfmapi).

Works in browsers (modern fetch + ReadableStream) and Node >= 20.

```bash
cd typescript
npm install
npm run build
```

## Usage

```ts
import { createSfmApiClient } from "@scenesdk/client/generated";

const c = createSfmApiClient({
  baseUrl: "http://localhost:8080",
  apiKey: process.env.SFMAPI_KEY,
});

const { data: proj, error } = await c.raw.POST("/v1/projects", {
  body: { name: "my-proj" },
});
if (error) throw error;

const sha = await c.uploadBytes(new Uint8Array(await file.arrayBuffer()), {
  contentType: "image/jpeg",
});

const { data: ds, error: dsError } = await c.raw.POST(
  "/v1/projects/{project_id}/datasets",
  {
    params: { path: { project_id: proj.project_id } },
    body: {
      name: "ds",
      source: {
        kind: "upload",
        entries: [{ name: "a.jpg", blob_sha: sha }],
      },
    },
  },
);
if (dsError) throw dsError;

const { data: job, error: jobError } = await c.raw.POST(
  "/v1/projects/{project_id}/pipelines/incremental",
  {
    params: { path: { project_id: proj.project_id } },
    body: {
      dataset_id: ds.dataset_id,
      image_root: "/data",
      image_list: ["a.jpg"],
      spec: { kind: "incremental", version: 1 },
    },
  },
);
if (jobError) throw jobError;

for await (const event of c.streamEvents(job.job_id)) {
  console.log(event.kind, "phase=", event.phase);
}
```

## Compatibility Client

The package also exports the older handwritten `SfmApiClient` wrapper
from `@scenesdk/client`. It remains available for compatibility and
migration, but new code should prefer the generated client above because
its raw endpoint surface is derived directly from the OpenAPI contract.

```ts
import { SfmApiClient } from "@scenesdk/client";

const c = new SfmApiClient({
  baseUrl: "http://localhost:8080",
  apiKey: process.env.SFMAPI_KEY,
});
```

## Errors

Generated helper methods and the compatibility wrapper throw typed
subclasses of `SfmApiError` for non-2xx HTTP responses. Raw OpenAPI calls
through `c.raw` return `{ data, error }`; check `error` explicitly there.

| HTTP | Class |
|---|---|
| 400 / 422 | `ValidationError` |
| 401 / 403 | `AuthError` |
| 404 | `NotFoundError` |
| 409 | `ConflictError` |
| 413 / 429 | `QuotaExceededError` |
| 501 | `CapabilityUnavailableError` (`PycolmapUnavailableError` when `capability="pycolmap"`) |
| 503 | `BackendUnavailableError` |
| 507 | `StorageError` |
| Other non-2xx | `SfmApiError` |

Each error carries `.statusCode`, `.problem` (parsed
`application/problem+json`), and `.response` (the raw `Response`).

## Browser Usage Notes

- `streamEvents()` uses `fetch`'s `ReadableStream`. All evergreen
  browsers support this.
- `uploadBytes()` accepts `Uint8Array`; convert browser `Blob` or `File`
  values with `new Uint8Array(await file.arrayBuffer())`.
- Pass `globalThis.AbortSignal` via `{ signal }` in any method options
  to cancel.

## Versioning

The SDK pins to the major version of the server's REST API (`/v1`).
Minor server bumps are non-breaking by contract.

## License

The TypeScript SDK source and npm package are licensed under
`Apache-2.0`; see `LICENSE`.
