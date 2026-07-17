import { describe, expect, it, beforeAll, afterAll, afterEach } from "vitest";
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

import {
  SfmApiClient,
  NotFoundError,
  ValidationError,
  AuthError,
  BackendUnavailableError,
  QuotaExceededError,
  StorageError,
  CapabilityUnavailableError,
  PycolmapUnavailableError,
} from "../src/index.js";
import type { BundleAdjustmentSpec } from "../src/index.js";
import { iterSse } from "../src/sse.js";

const BASE = "http://api.test";

const server = setupServer();

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function makeClient(opts: { apiKey?: string } = {}) {
  return new SfmApiClient({
    baseUrl: BASE,
    ...(opts.apiKey !== undefined ? { apiKey: opts.apiKey } : {}),
  });
}

function artifactPayload(artifactId = "art-1") {
  return {
    artifact_id: artifactId,
    job_id: "job-1",
    task_id: "task-1",
    recon_id: "recon-1",
    dataset_id: null,
    kind: "features.local.v1",
    name: "features.json",
    uri: "https://artifacts.example/features.json",
    media_type: "application/json",
    artifact_format: "sfmapi.features.local.v1",
    datatype: "feature_set",
    schema_version: 1,
    files: [],
    sha256: null,
    byte_size: null,
    coordinate_frame: null,
    producer: null,
    summary: null,
    metadata: {},
    created_at: "2026-05-02T00:00:00Z",
    _links: { self: { href: `/v1/artifacts/${artifactId}` } },
  };
}

describe("SfmApiClient", () => {
  it("createProject sends Authorization header and parses Project", async () => {
    let captured: Headers | null = null;
    server.use(
      http.post(`${BASE}/v1/projects`, ({ request }) => {
        captured = request.headers;
        return HttpResponse.json(
          {
            project_id: "P".repeat(26),
            tenant_id: "default",
            name: "alpha",
            description: null,
            created_at: "2026-05-02T00:00:00Z",
          },
          { status: 201 },
        );
      }),
    );
    const c = makeClient({ apiKey: "sfm_test" });
    const p = await c.createProject({ name: "alpha" });
    expect(p.name).toBe("alpha");
    expect(captured!.get("Authorization")).toBe("Bearer sfm_test");
  });

  it("createApiKey sends tenant/name and parses current response shape", async () => {
    let captured: unknown = null;
    server.use(
      http.post(`${BASE}/v1/admin/api-keys`, async ({ request }) => {
        captured = await request.json();
        return HttpResponse.json(
          {
            raw_key: "sfm_secret",
            api_key_id: "key-1",
            tenant_id: "tenant-1",
            name: "ci",
          },
          { status: 201 },
        );
      }),
    );
    const c = makeClient();
    const key = await c.createApiKeyForTenant("tenant-1", "ci");
    expect(captured).toEqual({ tenant_id: "tenant-1", name: "ci" });
    expect(key.raw_key).toBe("sfm_secret");
    expect(key.name).toBe("ci");
  });

  it("createApiKey keeps legacy name helper with default tenant", async () => {
    let captured: unknown = null;
    server.use(
      http.post(`${BASE}/v1/admin/api-keys`, async ({ request }) => {
        captured = await request.json();
        return HttpResponse.json(
          {
            raw_key: "sfm_secret",
            api_key_id: "key-1",
            tenant_id: "default",
            name: "ci",
          },
          { status: 201 },
        );
      }),
    );
    const c = makeClient();
    const key = await c.createApiKey("ci");
    expect(captured).toEqual({ tenant_id: "default", name: "ci" });
    expect(key.tenant_id).toBe("default");
  });

  it("createApiKey keeps legacy label object helper", async () => {
    let captured: unknown = null;
    server.use(
      http.post(`${BASE}/v1/admin/api-keys`, async ({ request }) => {
        captured = await request.json();
        return HttpResponse.json(
          {
            raw_key: "sfm_secret",
            api_key_id: "key-1",
            tenant_id: "default",
            name: "ci",
          },
          { status: 201 },
        );
      }),
    );
    const c = makeClient();
    const key = await c.createApiKey({ label: "ci" });
    expect(captured).toEqual({ tenant_id: "default", name: "ci" });
    expect(key.label).toBe("ci");
  });

  it("dense and mesh helpers reject locally without fetch", async () => {
    const calls: string[] = [];
    const fetchImpl: typeof fetch = ((input: RequestInfo | URL) => {
      calls.push(String(input));
      return Promise.resolve(new Response("{}"));
    }) as typeof fetch;
    const c = new SfmApiClient({ baseUrl: BASE, fetch: fetchImpl });
    await expect(c.submitDense("R".repeat(26))).rejects.toThrow(/out of scope/);
    await expect(c.submitMesh("R".repeat(26))).rejects.toThrow(/out of scope/);
    await expect(c.readDenseIndex("R".repeat(26), 1)).rejects.toThrow(/out of scope/);
    await expect(c.readMeshPly("R".repeat(26), 1)).rejects.toThrow(/out of scope/);
    expect(calls).toEqual([]);
  });

  it("404 raises NotFoundError with parsed problem body", async () => {
    server.use(
      http.get(`${BASE}/v1/projects/missing`, () =>
        HttpResponse.json(
          {
            type: "https://sfmapi/errors/not_found",
            title: "Resource not found",
            status: 404,
            detail: "Project missing not found",
          },
          { status: 404, headers: { "Content-Type": "application/problem+json" } },
        ),
      ),
    );
    const c = makeClient();
    await expect(c.getProject("missing")).rejects.toMatchObject({
      name: "NotFoundError",
      statusCode: 404,
      message: expect.stringContaining("missing"),
    });
    expect(NotFoundError).toBeDefined();
  });

  it("422 maps to ValidationError", async () => {
    server.use(
      http.post(`${BASE}/v1/datasets/DS/matches`, () =>
        HttpResponse.json(
          { title: "Validation error", status: 422, detail: "vocab missing" },
          { status: 422, headers: { "Content-Type": "application/problem+json" } },
        ),
      ),
    );
    const c = makeClient();
    await expect(
      c.submitMatches("DS", { pairs: { strategy: "vocabtree" } }),
    ).rejects.toBeInstanceOf(ValidationError);
  });

  it("403 maps to AuthError", async () => {
    server.use(
      http.get(`${BASE}/v1/projects/X`, () =>
        HttpResponse.json(
          { title: "Tenant boundary violation", status: 403 },
          { status: 403 },
        ),
      ),
    );
    const c = makeClient();
    await expect(c.getProject("X")).rejects.toBeInstanceOf(AuthError);
  });

  it("generic 501 maps to CapabilityUnavailableError", async () => {
    server.use(
      http.get(`${BASE}/v1/projects/X`, () =>
        HttpResponse.json(
          {
            title: "Capability not available in this deployment",
            status: 501,
            detail: "custom typed processor pipeline execution is not available",
            capability: "pipelines.custom_execution",
          },
          { status: 501, headers: { "Content-Type": "application/problem+json" } },
        ),
      ),
    );
    const c = makeClient();
    await expect(c.getProject("X")).rejects.toBeInstanceOf(CapabilityUnavailableError);
    await expect(c.getProject("X")).rejects.not.toBeInstanceOf(PycolmapUnavailableError);
  });

  it("pycolmap 501 keeps the specialized error", async () => {
    server.use(
      http.get(`${BASE}/v1/projects/X`, () =>
        HttpResponse.json(
          {
            title: "Capability not available in this deployment",
            status: 501,
            detail: "pycolmap unavailable",
            capability: "pycolmap",
          },
          { status: 501, headers: { "Content-Type": "application/problem+json" } },
        ),
      ),
    );
    const c = makeClient();
    await expect(c.getProject("X")).rejects.toBeInstanceOf(PycolmapUnavailableError);
    await expect(c.getProject("X")).rejects.toBeInstanceOf(CapabilityUnavailableError);
  });

  it("maps remaining standard problem statuses", async () => {
    const cases = [
      [400, ValidationError],
      [401, AuthError],
      [413, QuotaExceededError],
      [503, BackendUnavailableError],
      [507, StorageError],
    ] as const;
    for (const [status, Cls] of cases) {
      server.resetHandlers();
      server.use(
        http.get(`${BASE}/v1/projects/X`, () =>
          HttpResponse.json(
            { title: "Problem", status, detail: `status ${status}` },
            { status, headers: { "Content-Type": "application/problem+json" } },
          ),
        ),
      );
      const c = makeClient();
      await expect(c.getProject("X")).rejects.toBeInstanceOf(Cls);
    }
  });

  it("readArtifactContent returns raw bytes", async () => {
    const payload = new Uint8Array([0, 255, 65, 10]);
    let contentUrl = "";
    server.use(
      http.get(`${BASE}/v1/artifacts/art-1/content`, ({ request }) => {
        contentUrl = request.url;
        return new HttpResponse(payload, {
          status: 200,
          headers: { "Content-Type": "application/octet-stream" },
        });
      }),
    );

    const c = makeClient();
    const body = await c.readArtifactContent("art-1", { download: true });

    expect(Array.from(new Uint8Array(body))).toEqual(Array.from(payload));
    expect(contentUrl).toBe(`${BASE}/v1/artifacts/art-1/content?download=true`);
  });

  it("artifact helpers route and parse typed responses", async () => {
    const artifact = artifactPayload();
    let importBody: unknown = null;
    let planBody: unknown = null;
    let convertBody: unknown = null;
    let jobArtifactsUrl = "";
    let reconArtifactsUrl = "";

    server.use(
      http.get(`${BASE}/v1/artifacts/kinds`, () =>
        HttpResponse.json({
          items: [
            {
              kind: "features.local.v1",
              datatype: "feature_set",
              title: "Features",
              description: "Local features",
              durable: true,
              artifact_format: "sfmapi.features.local.v1",
              schema_version: 1,
            },
          ],
          next_page_token: null,
        }),
      ),
      http.get(`${BASE}/v1/artifacts/formats`, () =>
        HttpResponse.json({
          items: [
            {
              format_id: "sfmapi.features.local.v1",
              datatype: "feature_set",
              title: "Features",
              description: "Local features",
              schema_version: 1,
              media_types: ["application/json"],
            },
          ],
          next_page_token: null,
        }),
      ),
      http.post(/^http:\/\/api\.test\/v1\/artifacts:import$/, async ({ request }) => {
        importBody = await request.json();
        return HttpResponse.json(artifact, { status: 201 });
      }),
      http.get(`${BASE}/v1/artifacts/art-1`, () => HttpResponse.json(artifact)),
      http.post(
        /^http:\/\/api\.test\/v1\/artifacts\/art-1:conversionPlan$/,
        async ({ request }) => {
          planBody = await request.json();
          return HttpResponse.json({
            artifact_id: "art-1",
            source_format: "provider.native",
            target_format: "sfmapi.features.local.v1",
            conversion_required: true,
            executable: true,
            steps: [
              {
                from_format: "provider.native",
                to_format: "sfmapi.features.local.v1",
                lossless: true,
              },
            ],
          });
        },
      ),
      http.post(/^http:\/\/api\.test\/v1\/artifacts\/art-1:convert$/, async ({ request }) => {
        convertBody = await request.json();
        return HttpResponse.json(
          {
            job_id: "job-1",
            task_ids: ["task-1"],
            artifact_id: "art-1",
            target_format: "sfmapi.features.local.v1",
          },
          { status: 202 },
        );
      }),
      http.post(/^http:\/\/api\.test\/v1\/artifacts\/art-1:validate$/, () =>
        HttpResponse.json({
          artifact_id: "art-1",
          valid: true,
          artifact_format: "sfmapi.features.local.v1",
          datatype: "feature_set",
          checked_content: false,
          issues: [],
        }),
      ),
      http.get(`${BASE}/v1/jobs/job-1/artifacts`, ({ request }) => {
        jobArtifactsUrl = request.url;
        return HttpResponse.json({ items: [artifact], next_page_token: null });
      }),
      http.get(`${BASE}/v1/reconstructions/recon-1/artifacts`, ({ request }) => {
        reconArtifactsUrl = request.url;
        return HttpResponse.json({ items: [artifact], next_page_token: null });
      }),
    );

    const c = makeClient();
    expect((await c.listArtifactKinds()).items[0]?.kind).toBe("features.local.v1");
    expect((await c.listArtifactFormats()).items[0]?.format_id).toBe(
      "sfmapi.features.local.v1",
    );
    expect(
      (
        await c.importArtifact({
          project_id: "project-1",
          kind: "features.local.v1",
          artifact_format: "sfmapi.features.local.v1",
          uri: "https://artifacts.example/features.json",
        })
      ).artifact_id,
    ).toBe("art-1");
    expect((await c.getArtifact("art-1"))._links?.self?.href).toBe(
      "/v1/artifacts/art-1",
    );
    expect(
      (await c.planArtifactConversion("art-1", {
        to_format: "sfmapi.features.local.v1",
      })).executable,
    ).toBe(true);
    expect(
      (await c.convertArtifact("art-1", {
        to_format: "sfmapi.features.local.v1",
      })).artifact_id,
    ).toBe("art-1");
    expect((await c.validateArtifact("art-1")).valid).toBe(true);
    expect(
      (
        await c.listJobArtifacts("job-1", {
          page_size: 1,
          kind: "features.local.v1",
          task_id: "task-1",
          name: "features",
        })
      ).items[0]?.artifact_id,
    ).toBe("art-1");
    expect(
      (
        await c.listReconstructionArtifacts("recon-1", {
          page_size: 1,
          kind: "features.local.v1",
          name: "features",
        })
      ).items[0]?.artifact_id,
    ).toBe("art-1");

    expect(importBody).toMatchObject({ artifact_format: "sfmapi.features.local.v1" });
    expect(planBody).toEqual({ to_format: "sfmapi.features.local.v1" });
    expect(convertBody).toEqual({ to_format: "sfmapi.features.local.v1" });
    expect(jobArtifactsUrl).toBe(
      `${BASE}/v1/jobs/job-1/artifacts?page_size=1&kind=features.local.v1&task_id=task-1&name=features`,
    );
    expect(reconArtifactsUrl).toBe(
      `${BASE}/v1/reconstructions/recon-1/artifacts?page_size=1&kind=features.local.v1&name=features`,
    );
  });

  it("handwritten BundleAdjustmentSpec type allows rig mode", () => {
    const spec: BundleAdjustmentSpec = { mode: "rig" };

    expect(spec.mode).toBe("rig");
  });

  it("uploadBytes performs init → PATCH → finalize and verifies sha", async () => {
    const payload = new Uint8Array([0xff, 0xd8, 0xff, 0xe0, 1, 2, 3, 4, 5]);
    // sha256 of payload (precomputed)
    const expectedSha = await crypto.subtle
      .digest("SHA-256", payload)
      .then((d) =>
        Array.from(new Uint8Array(d))
          .map((b) => b.toString(16).padStart(2, "0"))
          .join(""),
      );

    let initBody: any = null;
    const ranges: string[] = [];

    server.use(
      http.post(`${BASE}/v1/uploads`, async ({ request }) => {
        initBody = await request.json();
        return HttpResponse.json(
          {
            upload_id: "U".repeat(26),
            state: "open",
            expected_size: payload.byteLength,
            received_bytes: 0,
            blob_sha: null,
            expires_at: "2026-05-03T00:00:00Z",
          },
          { status: 201 },
        );
      }),
      http.patch(`${BASE}/v1/uploads/${"U".repeat(26)}`, async ({ request }) => {
        ranges.push(request.headers.get("Content-Range") ?? "");
        return HttpResponse.json({
          upload_id: "U".repeat(26),
          state: "received",
          expected_size: payload.byteLength,
          received_bytes: payload.byteLength,
          blob_sha: null,
          expires_at: "2026-05-03T00:00:00Z",
        });
      }),
      http.post(`${BASE}/v1/uploads/${"U".repeat(26)}:finalize`, () =>
        HttpResponse.json({
          upload_id: "U".repeat(26),
          state: "finalized",
          expected_size: payload.byteLength,
          received_bytes: payload.byteLength,
          blob_sha: expectedSha,
          expires_at: "2026-05-03T00:00:00Z",
        }),
      ),
    );

    const c = makeClient();
    const sha = await c.uploadBytes(payload, { chunkSize: 4 });
    expect(sha).toBe(expectedSha);
    expect(initBody.expected_sha).toBe(expectedSha);
    expect(initBody.expected_size).toBe(payload.byteLength);
    expect(ranges).toEqual(["bytes 0-3/9", "bytes 4-7/9", "bytes 8-8/9"]);
  });

  it("runPipeline routes to /pipelines/{kind}", async () => {
    let hitPath: string | null = null;
    server.use(
      http.post(`${BASE}/v1/projects/PR/pipelines/incremental`, ({ request }) => {
        hitPath = new URL(request.url).pathname;
        return HttpResponse.json(
          {
            job_id: "J".repeat(26),
            task_ids: ["T".repeat(26)],
            recon_id: "R".repeat(26),
          },
          { status: 202 },
        );
      }),
    );
    const c = makeClient();
    const result = await c.runPipeline("PR", {
      dataset_id: "DS",
      spec: { kind: "incremental" },
    });
    expect(hitPath).toBe("/v1/projects/PR/pipelines/incremental");
    expect(result.recon_id).toBe("R".repeat(26));
  });

  it("validatePipeline routes to /pipelines:validate", async () => {
    let captured: unknown = null;
    server.use(
      http.post(`${BASE}/v1/pipelines:validate`, async ({ request }) => {
        captured = await request.json();
        return HttpResponse.json({ valid: true, errors: [] });
      }),
    );
    const c = makeClient();
    const result = await c.validatePipeline({
      steps: [{ processor: "features" }],
    });
    expect(result.valid).toBe(true);
    expect(captured).toEqual({ steps: [{ processor: "features" }] });
  });

  it("runTypedPipeline routes to /pipelines:run", async () => {
    let capturedPath: string | null = null;
    let capturedBody: unknown = null;
    server.use(
      http.post(`${BASE}/v1/projects/PR/pipelines:run`, async ({ request }) => {
        capturedPath = new URL(request.url).pathname;
        capturedBody = await request.json();
        return HttpResponse.json(
          {
            job_id: "Y".repeat(26),
            task_ids: ["T".repeat(26)],
            recon_id: null,
          },
          { status: 202 },
        );
      }),
    );
    const c = makeClient();
    const result = await c.runTypedPipeline("PR", {
      dataset_id: "DS",
      steps: ["features", "pairs"],
    });
    expect(capturedPath).toBe("/v1/projects/PR/pipelines:run");
    expect(capturedBody).toEqual({
      dataset_id: "DS",
      steps: ["features", "pairs"],
    });
    expect(result.job_id).toBe("Y".repeat(26));
  });

  it("typed dataflow discovery helpers route to contract endpoints", async () => {
    const paths: string[] = [];
    server.use(
      http.get(`${BASE}/v1/attributes`, ({ request }) => {
        paths.push(new URL(request.url).pathname);
        return HttpResponse.json({
          contract: "attributes",
          contract_schema_version: 1,
          attribute_types: ["str"],
          rules: {},
        });
      }),
      http.get(`${BASE}/v1/datatypes`, ({ request }) => {
        paths.push(new URL(request.url).pathname);
        return HttpResponse.json({
          contract: "datatypes",
          contract_schema_version: 1,
          kinds: ["logical"],
          types: [],
        });
      }),
      http.get(`${BASE}/v1/operations`, ({ request }) => {
        paths.push(new URL(request.url).pathname);
        return HttpResponse.json({
          contract: "operations",
          contract_schema_version: 1,
          operations: [],
          compatibility: {},
        });
      }),
      http.get(`${BASE}/v1/processors`, ({ request }) => {
        paths.push(new URL(request.url).pathname);
        return HttpResponse.json({
          contract: "processors",
          contract_schema_version: 1,
          processors: [],
          rules: {},
        });
      }),
      http.get(`${BASE}/v1/pipelines`, ({ request }) => {
        paths.push(new URL(request.url).pathname);
        return HttpResponse.json({
          contract: "pipelines",
          contract_schema_version: 1,
          composition_rule: "supplier.datatype == consumer.datatype",
          initial_inputs: [],
          canonical_pipelines: {},
          plugin_pipelines: [],
          step_schema: {},
          validation_reasons: [],
        });
      }),
    );

    const c = makeClient();
    expect((await c.listAttributes()).contract).toBe("attributes");
    expect((await c.listDatatypes()).contract).toBe("datatypes");
    expect((await c.listOperations()).contract).toBe("operations");
    expect((await c.listProcessors()).contract).toBe("processors");
    expect((await c.listPipelines()).contract).toBe("pipelines");
    expect(paths).toEqual([
      "/v1/attributes",
      "/v1/datatypes",
      "/v1/operations",
      "/v1/processors",
      "/v1/pipelines",
    ]);
  });

  it("listDatasets returns items and listDatasetsPage returns the page envelope", async () => {
    let captured: URL | null = null;
    server.use(
      http.get(`${BASE}/v1/projects/PR/datasets`, ({ request }) => {
        captured = new URL(request.url);
        return HttpResponse.json({
          items: [
            {
              dataset_id: "D".repeat(26),
              project_id: "PR",
              tenant_id: "default",
              name: "dataset",
              camera_model: "SIMPLE_RADIAL",
              intrinsics_mode: "single_camera",
              is_spherical: false,
              respect_exif_orientation: false,
              active_maskset_id: null,
              manifest_hash: "",
              created_at: "2026-05-02T00:00:00Z",
              updated_at: "2026-05-02T00:00:00Z",
            },
          ],
          next_page_token: "next",
        });
      }),
    );

    const c = makeClient();
    const page = await c.listDatasetsPage("PR", { page_size: 7, page_token: "tok" });
    const items = await c.listDatasets("PR", { page_size: 7, page_token: "tok" });

    expect(captured!.searchParams.get("page_size")).toBe("7");
    expect(captured!.searchParams.get("page_token")).toBe("tok");
    expect(page.next_page_token).toBe("next");
    expect(page.items[0]?.name).toBe("dataset");
    expect(items[0]?.name).toBe("dataset");
  });

  it("listSubmodels returns items and listSubmodelsPage returns the page envelope", async () => {
    let captured: URL | null = null;
    server.use(
      http.get(`${BASE}/v1/reconstructions/REC/submodels`, ({ request }) => {
        captured = new URL(request.url);
        return HttpResponse.json({
          items: [
            {
              submodel_id: "S".repeat(26),
              recon_id: "REC",
              idx: 0,
              image_count: 2,
              registered_images: ["a.jpg", "b.jpg"],
              snapshot_seq: 1,
              created_at: "2026-05-02T00:00:00Z",
            },
          ],
          next_page_token: "2",
        });
      }),
    );

    const c = makeClient();
    const page = await c.listSubmodelsPage("REC", { page_size: 2, page_token: "1" });
    const items = await c.listSubmodels("REC", { page_size: 2, page_token: "1" });

    expect(captured!.searchParams.get("page_size")).toBe("2");
    expect(captured!.searchParams.get("page_token")).toBe("1");
    expect(page.next_page_token).toBe("2");
    expect(page.items[0]?.submodel_id).toBe("S".repeat(26));
    expect(items[0]?.submodel_id).toBe("S".repeat(26));
  });

  it("streamEvents parses SSE lines into ProgressEvent objects", async () => {
    server.use(
      http.get(`${BASE}/v1/jobs/JOB/events`, () => {
        const body = [
          "id: 1",
          'data: {"schema_version":1,"ts":"t","job_id":"JOB","seq":1,"kind":"phase_started","phase":"feature_extraction"}',
          "",
          "id: 2",
          'data: {"schema_version":1,"ts":"t","job_id":"JOB","seq":2,"kind":"phase_progress","phase":"feature_extraction","current":3,"total":4}',
          "",
        ].join("\n");
        return new HttpResponse(body, {
          status: 200,
          headers: { "Content-Type": "text/event-stream" },
        });
      }),
    );
    const c = makeClient();
    const events = [];
    for await (const e of c.streamEvents("JOB")) {
      events.push(e);
      if (events.length === 2) break;
    }
    expect(events).toHaveLength(2);
    expect(events[0]!.kind).toBe("phase_started");
    expect(events[1]!.kind).toBe("phase_progress");
    expect(events[1]!.current).toBe(3);
  });
});

describe("iterSse", () => {
  it("yields multi-line data fields concatenated with newlines", async () => {
    const body = ["data: line1", "data: line2", "", ""].join("\n");
    const stream = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(new TextEncoder().encode(body));
        controller.close();
      },
    });
    const out: string[] = [];
    for await (const msg of iterSse(stream)) out.push(msg.data);
    expect(out).toEqual(["line1\nline2"]);
  });
});
