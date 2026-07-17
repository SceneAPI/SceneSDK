import type { Capabilities } from "./capabilities.js";
import { raiseForResponse, TransportError } from "./errors.js";
import { asUint8, sha256Hex } from "./hash.js";
import type {
  ApiKey,
  ApiKeyCreated,
  ArtifactConversionPlanOut,
  ArtifactConversionPlanRequest,
  ArtifactConvertRequest,
  ArtifactFormatOut,
  ArtifactImportRequest,
  ArtifactKindOut,
  ArtifactValidationOut,
  AttributesContractOut,
  BatchCreateImagesRequest,
  BatchCreateImagesResponse,
  Dataset,
  DatasetPatch,
  DataTypesContractOut,
  FeaturesSpec,
  HealthResponse,
  Image,
  ImageObservationRow,
  Job,
  JobDetail,
  JobSubmitResponse,
  MatcherSpec,
  OperationsContractOut,
  PairsSpec,
  Page,
  PipelinesContractOut,
  PipelineRunRequest,
  PipelineSpec,
  PipelineValidateRequest,
  PipelineValidateResponse,
  PointObservationRow,
  ProgressEvent,
  ProcessorsContractOut,
  Project,
  ProjectPatch,
  Reconstruction,
  StageArtifact,
  SubModel,
  TilesIndex,
  Upload,
  VerifySpec,
  VersionResponse,
} from "./models.js";
import type {
  CorrespondenceGraphFile,
  DenseManifestFile,
  LocalizationResult,
  MeshFile,
  PosePrior,
  Sim3,
  TwoViewGeometriesFile,
} from "./scene.js";
import { iterSse } from "./sse.js";

export interface SfmApiClientOptions {
  baseUrl: string;
  apiKey?: string;
  fetch?: typeof fetch;
  defaultHeaders?: HeadersInit;
}

export interface RequestOptions {
  signal?: AbortSignal;
  headers?: HeadersInit;
}

export interface PageParams {
  page_size?: number;
  page_token?: string;
}

export interface ArtifactListParams extends PageParams {
  kind?: string;
  task_id?: string;
  name?: string;
}

export interface ArtifactContentOptions extends RequestOptions {
  download?: boolean;
}

const DEFAULT_CHUNK = 1 * 1024 * 1024;
const DENSE_MESH_UNSUPPORTED =
  "Dense MVS and mesh/texture generation are out of scope for sfmapi SDK " +
  "route helpers; invoke backend actions or a downstream mvsapi or meshapi service.";

function unsupportedDenseMesh<T>(): Promise<T> {
  return Promise.reject(new Error(DENSE_MESH_UNSUPPORTED));
}

export class SfmApiClient {
  private readonly baseUrl: string;
  private readonly apiKey?: string;
  private readonly fetchImpl: typeof fetch;
  private readonly defaultHeaders: HeadersInit;

  constructor(opts: SfmApiClientOptions) {
    this.baseUrl = opts.baseUrl.replace(/\/+$/, "");
    if (opts.apiKey !== undefined) this.apiKey = opts.apiKey;
    this.fetchImpl = opts.fetch ?? globalThis.fetch.bind(globalThis);
    this.defaultHeaders = opts.defaultHeaders ?? {};
  }

  // --- low-level ---------------------------------------------------

  private buildHeaders(extra?: HeadersInit): Headers {
    const h = new Headers(this.defaultHeaders);
    if (extra) {
      const e = new Headers(extra);
      e.forEach((v, k) => h.set(k, v));
    }
    if (this.apiKey && !h.has("Authorization")) {
      h.set("Authorization", `Bearer ${this.apiKey}`);
    }
    return h;
  }

  private async req(
    method: string,
    path: string,
    reqInit: Omit<RequestInit, "method"> & { json?: unknown } = {},
    opts?: RequestOptions,
  ): Promise<Response> {
    const { json, ...rest } = reqInit;
    const headers = this.buildHeaders(opts?.headers);
    if (rest.headers) {
      const requestHeaders = new Headers(rest.headers);
      requestHeaders.forEach((value, key) => headers.set(key, value));
    }
    let body: BodyInit | null = (rest.body as BodyInit | null | undefined) ?? null;
    if (json !== undefined) {
      headers.set("Content-Type", "application/json");
      body = JSON.stringify(json);
    }
    const fetchInit: RequestInit = { ...rest, method, headers, body };
    const sig = opts?.signal ?? rest.signal ?? null;
    if (sig) fetchInit.signal = sig;
    let resp: Response;
    try {
      resp = await this.fetchImpl(`${this.baseUrl}${path}`, fetchInit);
    } catch (err: unknown) {
      const cause = err instanceof Error ? err.message : String(err);
      throw new TransportError(`fetch failed: ${cause}`);
    }
    await raiseForResponse(resp);
    return resp;
  }

  private pagedPath(path: string, params: PageParams = {}): string {
    const qs = new URLSearchParams();
    if (params.page_size !== undefined)
      qs.set("page_size", String(params.page_size));
    if (params.page_token) qs.set("page_token", params.page_token);
    const query = qs.toString();
    return query ? `${path}?${query}` : path;
  }

  private artifactListPath(path: string, params: ArtifactListParams = {}): string {
    const qs = new URLSearchParams();
    if (params.page_size !== undefined)
      qs.set("page_size", String(params.page_size));
    if (params.page_token) qs.set("page_token", params.page_token);
    if (params.kind !== undefined) qs.set("kind", params.kind);
    if (params.task_id !== undefined) qs.set("task_id", params.task_id);
    if (params.name !== undefined) qs.set("name", params.name);
    const query = qs.toString();
    return query ? `${path}?${query}` : path;
  }

  private splitPageArgs(
    paramsOrOpts: PageParams | RequestOptions = {},
    opts?: RequestOptions,
  ): [PageParams, RequestOptions | undefined] {
    if (opts !== undefined) {
      return [paramsOrOpts as PageParams, opts];
    }
    if ("page_size" in paramsOrOpts || "page_token" in paramsOrOpts) {
      return [paramsOrOpts as PageParams, opts];
    }
    return [{}, paramsOrOpts as RequestOptions];
  }

  // --- meta --------------------------------------------------------

  healthz(opts?: RequestOptions): Promise<HealthResponse> {
    return this.req("GET", "/healthz", {}, opts).then((r) => r.json());
  }

  version(opts?: RequestOptions): Promise<VersionResponse> {
    return this.req("GET", "/version", {}, opts).then((r) => r.json());
  }

  // --- projects ----------------------------------------------------

  createProject(
    body: { name: string; description?: string | null },
    opts?: RequestOptions,
  ): Promise<Project> {
    return this.req("POST", "/v1/projects", { json: body }, opts).then((r) =>
      r.json(),
    );
  }

  getProject(projectId: string, opts?: RequestOptions): Promise<Project> {
    return this.req("GET", `/v1/projects/${projectId}`, {}, opts).then((r) =>
      r.json(),
    );
  }

  async listProjects(
    params: PageParams = {},
    opts?: RequestOptions,
  ): Promise<Page<Project>> {
    const r = await this.req("GET", this.pagedPath("/v1/projects", params), {}, opts);
    return r.json();
  }

  async deleteProject(projectId: string, opts?: RequestOptions): Promise<void> {
    await this.req("DELETE", `/v1/projects/${projectId}`, {}, opts);
  }

  // --- uploads -----------------------------------------------------

  initUpload(
    body: {
      expected_size: number;
      content_type?: string | null;
      expected_sha?: string | null;
    },
    options: { idempotencyKey?: string } & RequestOptions = {},
  ): Promise<Upload> {
    const headers: Record<string, string> = {};
    if (options.idempotencyKey) headers["Idempotency-Key"] = options.idempotencyKey;
    return this.req(
      "POST",
      "/v1/uploads",
      { json: body, headers },
      options,
    ).then((r) => r.json());
  }

  patchChunk(
    uploadId: string,
    args: { offset: number; data: ArrayBuffer | Uint8Array; total?: number },
    opts?: RequestOptions,
  ): Promise<Upload> {
    const bytes = args.data instanceof Uint8Array
      ? args.data
      : new Uint8Array(args.data);
    // Copy into a fresh ArrayBuffer so the BodyInit overload accepts it
    // across DOM lib versions.
    const buf = new Uint8Array(bytes.byteLength);
    buf.set(bytes);
    const end = args.offset + buf.byteLength - 1;
    const total = args.total ?? args.offset + buf.byteLength;
    return this.req(
      "PATCH",
      `/v1/uploads/${uploadId}`,
      {
        body: buf.buffer,
        headers: {
          "Content-Range": `bytes ${args.offset}-${end}/${total}`,
          "Content-Type": "application/octet-stream",
        },
      },
      opts,
    ).then((r) => r.json());
  }

  finalizeUpload(
    uploadId: string,
    args: { clientSha?: string } = {},
    opts?: RequestOptions,
  ): Promise<Upload> {
    const headers: Record<string, string> = {};
    if (args.clientSha) headers["X-Content-SHA256"] = args.clientSha;
    return this.req(
      "POST",
      `/v1/uploads/${uploadId}:finalize`,
      { json: {}, headers },
      opts,
    ).then((r) => r.json());
  }

  /** High-level helper: init → PATCH (chunked) → finalize → returns blob sha. */
  async uploadBytes(
    data: ArrayBuffer | Uint8Array | Blob,
    options: {
      contentType?: string;
      idempotencyKey?: string;
      chunkSize?: number;
    } & RequestOptions = {},
  ): Promise<string> {
    const bytes = await asUint8(data);
    const sha = await sha256Hex(bytes);
    const initOpts: { idempotencyKey?: string; signal?: AbortSignal } = {};
    if (options.idempotencyKey !== undefined) initOpts.idempotencyKey = options.idempotencyKey;
    if (options.signal !== undefined) initOpts.signal = options.signal;
    const upload = await this.initUpload(
      {
        expected_size: bytes.byteLength,
        expected_sha: sha,
        content_type: options.contentType ?? null,
      },
      initOpts,
    );
    const chunkSize = options.chunkSize ?? DEFAULT_CHUNK;
    let offset = 0;
    while (offset < bytes.byteLength) {
      const end = Math.min(offset + chunkSize, bytes.byteLength);
      const slice = bytes.subarray(offset, end);
      // eslint-disable-next-line no-await-in-loop
      await this.patchChunk(
        upload.upload_id,
        { offset, data: slice, total: bytes.byteLength },
        options,
      );
      offset = end;
    }
    const result = await this.finalizeUpload(upload.upload_id, { clientSha: sha }, options);
    if (result.blob_sha !== sha) {
      throw new Error(`server sha ${result.blob_sha} != local ${sha}`);
    }
    return sha;
  }

  // --- datasets / images -------------------------------------------

  createDataset(
    projectId: string,
    body: {
      name: string;
      source: Record<string, unknown>;
      camera_model?: string;
      intrinsics_mode?: "single_camera" | "per_image" | "per_folder";
      is_spherical?: boolean;
      rig_config?: Record<string, unknown> | null;
      respect_exif_orientation?: boolean;
    },
    opts?: RequestOptions,
  ): Promise<Dataset> {
    return this.req(
      "POST",
      `/v1/projects/${projectId}/datasets`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  getDataset(
    projectId: string,
    datasetId: string,
    opts?: RequestOptions,
  ): Promise<Dataset> {
    return this.req(
      "GET",
      `/v1/projects/${projectId}/datasets/${datasetId}`,
      {},
      opts,
    ).then((r) => r.json());
  }

  listDatasets(projectId: string, opts?: RequestOptions): Promise<Dataset[]>;
  listDatasets(
    projectId: string,
    params?: PageParams,
    opts?: RequestOptions,
  ): Promise<Dataset[]>;
  async listDatasets(
    projectId: string,
    paramsOrOpts: PageParams | RequestOptions = {},
    opts?: RequestOptions,
  ): Promise<Dataset[]> {
    const [params, requestOpts] = this.splitPageArgs(paramsOrOpts, opts);
    const r = await this.req(
      "GET",
      this.pagedPath(`/v1/projects/${projectId}/datasets`, params),
      {},
      requestOpts,
    );
    const page = (await r.json()) as Page<Dataset>;
    return page.items ?? [];
  }

  listDatasetsPage(projectId: string, opts?: RequestOptions): Promise<Page<Dataset>>;
  listDatasetsPage(
    projectId: string,
    params?: PageParams,
    opts?: RequestOptions,
  ): Promise<Page<Dataset>>;
  async listDatasetsPage(
    projectId: string,
    paramsOrOpts: PageParams | RequestOptions = {},
    opts?: RequestOptions,
  ): Promise<Page<Dataset>> {
    const [params, requestOpts] = this.splitPageArgs(paramsOrOpts, opts);
    const r = await this.req(
      "GET",
      this.pagedPath(`/v1/projects/${projectId}/datasets`, params),
      {},
      requestOpts,
    );
    return r.json();
  }

  addImage(
    datasetId: string,
    body: {
      name: string;
      blob_sha?: string;
      rel_path?: string;
      width?: number;
      height?: number;
      exif?: Record<string, unknown>;
    },
    opts?: RequestOptions,
  ): Promise<Image> {
    return this.req(
      "POST",
      `/v1/datasets/${datasetId}/images`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  async listImages(
    datasetId: string,
    params: PageParams = {},
    opts?: RequestOptions,
  ): Promise<Page<Image>> {
    const r = await this.req(
      "GET",
      this.pagedPath(`/v1/datasets/${datasetId}/images`, params),
      {},
      opts,
    );
    return r.json();
  }

  // --- SfM stages --------------------------------------------------

  submitFeatures(
    datasetId: string,
    body: { spec?: FeaturesSpec } = {},
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/datasets/${datasetId}/features`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  submitMatches(
    datasetId: string,
    body: { pairs?: PairsSpec; matcher?: MatcherSpec } = {},
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/datasets/${datasetId}/matches`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  submitVerify(
    datasetId: string,
    body: { spec?: VerifySpec } = {},
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/datasets/${datasetId}/verify`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  runPipeline(
    projectId: string,
    body: {
      dataset_id: string;
      spec: PipelineSpec;
      features?: FeaturesSpec;
      pairs?: PairsSpec;
      matcher?: MatcherSpec;
      verify?: VerifySpec;
    },
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    const kind = body.spec.kind;
    return this.req(
      "POST",
      `/v1/projects/${projectId}/pipelines/${kind}`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  validatePipeline(
    body: PipelineValidateRequest,
    opts?: RequestOptions,
  ): Promise<PipelineValidateResponse> {
    return this.req(
      "POST",
      "/v1/pipelines:validate",
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  runTypedPipeline(
    projectId: string,
    body: PipelineRunRequest,
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/projects/${projectId}/pipelines:run`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  listAttributes(opts?: RequestOptions): Promise<AttributesContractOut> {
    return this.req("GET", "/v1/attributes", {}, opts).then((r) => r.json());
  }

  listDatatypes(opts?: RequestOptions): Promise<DataTypesContractOut> {
    return this.req("GET", "/v1/datatypes", {}, opts).then((r) => r.json());
  }

  listOperations(opts?: RequestOptions): Promise<OperationsContractOut> {
    return this.req("GET", "/v1/operations", {}, opts).then((r) => r.json());
  }

  listProcessors(opts?: RequestOptions): Promise<ProcessorsContractOut> {
    return this.req("GET", "/v1/processors", {}, opts).then((r) => r.json());
  }

  listPipelines(opts?: RequestOptions): Promise<PipelinesContractOut> {
    return this.req("GET", "/v1/pipelines", {}, opts).then((r) => r.json());
  }

  // --- jobs --------------------------------------------------------

  getJob(jobId: string, opts?: RequestOptions): Promise<JobDetail> {
    return this.req("GET", `/v1/jobs/${jobId}`, {}, opts).then((r) => r.json());
  }

  cancelJob(
    jobId: string,
    args: { force?: boolean } = {},
    opts?: RequestOptions,
  ): Promise<Job> {
    const qs = args.force ? "?force=true" : "";
    return this.req("POST", `/v1/jobs/${jobId}:cancel${qs}`, { json: {} }, opts).then(
      (r) => r.json(),
    );
  }

  resumeJob(jobId: string, opts?: RequestOptions): Promise<Job> {
    return this.req("POST", `/v1/jobs/${jobId}:resume`, { json: {} }, opts).then(
      (r) => r.json(),
    );
  }

  async *streamEvents(
    jobId: string,
    options: { lastEventId?: number | string } & RequestOptions = {},
  ): AsyncGenerator<ProgressEvent> {
    const headers: Record<string, string> = { Accept: "text/event-stream" };
    if (options.lastEventId !== undefined) {
      headers["Last-Event-ID"] = String(options.lastEventId);
    }
    const resp = await this.req(
      "GET",
      `/v1/jobs/${jobId}/events`,
      { headers },
      options,
    );
    if (!resp.body) {
      throw new TransportError("no response body for SSE stream");
    }
    for await (const msg of iterSse(resp.body)) {
      try {
        yield JSON.parse(msg.data) as ProgressEvent;
      } catch {
        // Skip malformed payloads rather than killing the stream.
      }
    }
  }

  listArtifactKinds(opts?: RequestOptions): Promise<Page<ArtifactKindOut>> {
    return this.req("GET", "/v1/artifacts/kinds", {}, opts).then((r) =>
      r.json(),
    );
  }

  listArtifactFormats(opts?: RequestOptions): Promise<Page<ArtifactFormatOut>> {
    return this.req("GET", "/v1/artifacts/formats", {}, opts).then((r) =>
      r.json(),
    );
  }

  importArtifact(
    body: ArtifactImportRequest,
    opts?: RequestOptions,
  ): Promise<StageArtifact> {
    return this.req("POST", "/v1/artifacts:import", { json: body }, opts).then(
      (r) => r.json(),
    );
  }

  getArtifact(artifactId: string, opts?: RequestOptions): Promise<StageArtifact> {
    return this.req("GET", `/v1/artifacts/${artifactId}`, {}, opts).then((r) =>
      r.json(),
    );
  }

  planArtifactConversion(
    artifactId: string,
    body: ArtifactConversionPlanRequest,
    opts?: RequestOptions,
  ): Promise<ArtifactConversionPlanOut> {
    return this.req(
      "POST",
      `/v1/artifacts/${artifactId}:conversionPlan`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  convertArtifact(
    artifactId: string,
    body: ArtifactConvertRequest,
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/artifacts/${artifactId}:convert`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  validateArtifact(
    artifactId: string,
    opts?: RequestOptions,
  ): Promise<ArtifactValidationOut> {
    return this.req(
      "POST",
      `/v1/artifacts/${artifactId}:validate`,
      {},
      opts,
    ).then((r) => r.json());
  }

  async listJobArtifacts(
    jobId: string,
    params: ArtifactListParams = {},
    opts?: RequestOptions,
  ): Promise<Page<StageArtifact>> {
    const r = await this.req(
      "GET",
      this.artifactListPath(`/v1/jobs/${jobId}/artifacts`, params),
      {},
      opts,
    );
    return r.json();
  }

  async listReconstructionArtifacts(
    reconId: string,
    params: ArtifactListParams = {},
    opts?: RequestOptions,
  ): Promise<Page<StageArtifact>> {
    const r = await this.req(
      "GET",
      this.artifactListPath(`/v1/reconstructions/${reconId}/artifacts`, params),
      {},
      opts,
    );
    return r.json();
  }

  async readArtifactContent(
    artifactId: string,
    opts?: ArtifactContentOptions,
  ): Promise<ArrayBuffer> {
    const { download, ...requestOpts } = opts ?? {};
    const qs = download ? "?download=true" : "";
    const r = await this.req(
      "GET",
      `/v1/artifacts/${artifactId}/content${qs}`,
      {},
      requestOpts,
    );
    return r.arrayBuffer();
  }

  // --- reconstructions / submodels / snapshots ---------------------

  getReconstruction(
    reconId: string,
    opts?: RequestOptions,
  ): Promise<Reconstruction> {
    return this.req("GET", `/v1/reconstructions/${reconId}`, {}, opts).then(
      (r) => r.json(),
    );
  }

  listSubmodels(reconId: string, opts?: RequestOptions): Promise<SubModel[]>;
  listSubmodels(
    reconId: string,
    params?: PageParams,
    opts?: RequestOptions,
  ): Promise<SubModel[]>;
  async listSubmodels(
    reconId: string,
    paramsOrOpts: PageParams | RequestOptions = {},
    opts?: RequestOptions,
  ): Promise<SubModel[]> {
    const [params, requestOpts] = this.splitPageArgs(paramsOrOpts, opts);
    const r = await this.req(
      "GET",
      this.pagedPath(`/v1/reconstructions/${reconId}/submodels`, params),
      {},
      requestOpts,
    );
    const page = (await r.json()) as Page<SubModel>;
    return page.items ?? [];
  }

  listSubmodelsPage(reconId: string, opts?: RequestOptions): Promise<Page<SubModel>>;
  listSubmodelsPage(
    reconId: string,
    params?: PageParams,
    opts?: RequestOptions,
  ): Promise<Page<SubModel>>;
  async listSubmodelsPage(
    reconId: string,
    paramsOrOpts: PageParams | RequestOptions = {},
    opts?: RequestOptions,
  ): Promise<Page<SubModel>> {
    const [params, requestOpts] = this.splitPageArgs(paramsOrOpts, opts);
    const r = await this.req(
      "GET",
      this.pagedPath(`/v1/reconstructions/${reconId}/submodels`, params),
      {},
      requestOpts,
    );
    return r.json();
  }

  async listSnapshots(reconId: string, opts?: RequestOptions): Promise<number[]> {
    const r = await this.req(
      "GET",
      `/v1/reconstructions/${reconId}/snapshots`,
      {},
      opts,
    );
    const body = (await r.json()) as { seqs: number[] };
    return body.seqs ?? [];
  }

  async readSnapshotFile(
    reconId: string,
    seq: number,
    name: string,
    opts?: RequestOptions,
  ): Promise<ArrayBuffer> {
    const r = await this.req(
      "GET",
      `/v1/reconstructions/${reconId}/snapshots/${seq}/${name}`,
      {},
      opts,
    );
    return r.arrayBuffer();
  }

  // --- capabilities -----------------------------------------------

  capabilities(opts?: RequestOptions): Promise<Capabilities> {
    return this.req("GET", "/v1/capabilities", {}, opts).then((r) => r.json());
  }

  // --- datasets (extended) ----------------------------------------

  async deleteDataset(
    projectId: string,
    datasetId: string,
    opts?: RequestOptions,
  ): Promise<void> {
    await this.req(
      "DELETE",
      `/v1/projects/${projectId}/datasets/${datasetId}`,
      {},
      opts,
    );
  }

  submitMatchesSplit(
    datasetId: string,
    body: { pairs: PairsSpec; matcher: MatcherSpec },
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/datasets/${datasetId}/matches`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  // --- similarity --------------------------------------------------

  similarityNeighbors(
    datasetId: string,
    query: {
      image_id: string;
      k?: number;
      strategy?: "dhash" | "vlad";
      include_self?: boolean;
    },
    opts?: RequestOptions,
  ): Promise<{ query_image_id: string; strategy: string; k: number; neighbors: Array<{ image_id: string; distance: number }> }> {
    const params = new URLSearchParams({
      image_id: query.image_id,
      k: String(query.k ?? 5),
      strategy: query.strategy ?? "dhash",
      include_self: String(query.include_self ?? false),
    });
    return this.req(
      "GET",
      `/v1/datasets/${datasetId}/similarity?${params}`,
      {},
      opts,
    ).then((r) => r.json());
  }

  buildSimilarityIndex(
    datasetId: string,
    options: { strategy?: "dhash" | "vlad"; force?: boolean } = {},
    opts?: RequestOptions,
  ): Promise<unknown> {
    const params = new URLSearchParams({
      strategy: options.strategy ?? "dhash",
      force: String(options.force ?? true),
    });
    return this.req(
      "POST",
      `/v1/datasets/${datasetId}/similarity:build?${params}`,
      {},
      opts,
    ).then((r) => r.json());
  }

  // --- pose priors -------------------------------------------------

  async getPosePrior(imageId: string, opts?: RequestOptions): Promise<PosePrior | null> {
    const r = await this.req("GET", `/v1/images/${imageId}/pose_prior`, {}, opts);
    return (await r.json()) as PosePrior | null;
  }

  putPosePrior(
    imageId: string,
    prior: PosePrior,
    opts?: RequestOptions,
  ): Promise<PosePrior> {
    return this.req(
      "PUT",
      `/v1/images/${imageId}/pose_prior`,
      { json: prior },
      opts,
    ).then((r) => r.json());
  }

  async deletePosePrior(imageId: string, opts?: RequestOptions): Promise<void> {
    await this.req("DELETE", `/v1/images/${imageId}/pose_prior`, {}, opts);
  }

  async listPosePriors(
    datasetId: string,
    opts?: RequestOptions,
  ): Promise<Record<string, PosePrior>> {
    const r = await this.req(
      "GET",
      `/v1/datasets/${datasetId}/pose_priors`,
      {},
      opts,
    );
    const body = (await r.json()) as { pose_priors: Record<string, PosePrior> };
    return body.pose_priors ?? {};
  }

  async bulkSetPosePriors(
    datasetId: string,
    priors: Record<string, PosePrior>,
    opts?: RequestOptions,
  ): Promise<number> {
    const r = await this.req(
      "PUT",
      `/v1/datasets/${datasetId}/pose_priors`,
      { json: priors },
      opts,
    );
    const body = (await r.json()) as { written?: number };
    return body.written ?? 0;
  }

  // --- localize / georegister / cubemap / merge ----

  submitLocalize(
    reconId: string,
    body: { blob_sha: string; sift?: Record<string, unknown> },
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/reconstructions/${reconId}/localize`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  submitGeoregister(
    reconId: string,
    sim3: Sim3,
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/reconstructions/${reconId}/georegister`,
      { json: sim3 },
      opts,
    ).then((r) => r.json());
  }

  submitToCubemap(reconId: string, opts?: RequestOptions): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/reconstructions/${reconId}:to_cubemap`,
      {},
      opts,
    ).then((r) => r.json());
  }

  submitRenderCubemap(
    datasetId: string,
    options: { face_size?: number } = {},
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    const params = options.face_size
      ? `?${new URLSearchParams({ face_size: String(options.face_size) })}`
      : "";
    return this.req(
      "POST",
      `/v1/datasets/${datasetId}:render_cubemap${params}`,
      {},
      opts,
    ).then((r) => r.json());
  }

  submitDense(reconId: string, opts?: RequestOptions): Promise<JobSubmitResponse> {
    void reconId;
    void opts;
    return unsupportedDenseMesh();
  }

  submitMesh(
    reconId: string,
    body: { method?: "poisson" | "delaunay"; options?: Record<string, unknown> } = {},
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    void reconId;
    void body;
    void opts;
    return unsupportedDenseMesh();
  }

  submitMergeRecons(
    body: {
      target_recon_id: string;
      source_recon_ids: string[];
      sim3_aligners?: Sim3[];
    },
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req("POST", "/v1/reconstructions:merge", { json: body }, opts).then(
      (r) => r.json(),
    );
  }

  // --- ingest helpers ----------------------------------------------

  submitVideoFrames(
    projectId: string,
    body: { video_path: string; fps?: number; max_frames?: number },
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/projects/${projectId}/datasets:from_video`,
      { json: { video_path: body.video_path, fps: body.fps ?? 2.0, max_frames: body.max_frames ?? 1000 } },
      opts,
    ).then((r) => r.json());
  }

  submitKaptureImport(
    projectId: string,
    body: { archive_path: string },
    opts?: RequestOptions,
  ): Promise<JobSubmitResponse> {
    return this.req(
      "POST",
      `/v1/projects/${projectId}/datasets:import_kapture`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  // --- reconstruction-level + snapshot reads ----------------------

  readTwoViewGeometries(
    reconId: string,
    opts?: RequestOptions,
  ): Promise<TwoViewGeometriesFile> {
    return this.req(
      "GET",
      `/v1/reconstructions/${reconId}/two_view_geometries.json`,
      {},
      opts,
    ).then((r) => r.json());
  }

  readCorrespondenceGraph(
    reconId: string,
    opts?: RequestOptions,
  ): Promise<CorrespondenceGraphFile> {
    return this.req(
      "GET",
      `/v1/reconstructions/${reconId}/correspondence_graph.json`,
      {},
      opts,
    ).then((r) => r.json());
  }

  readDenseIndex(
    reconId: string,
    seq: number,
    opts?: RequestOptions,
  ): Promise<DenseManifestFile> {
    void reconId;
    void seq;
    void opts;
    return unsupportedDenseMesh();
  }

  readDenseFused(
    reconId: string,
    seq: number,
    opts?: RequestOptions,
  ): Promise<ArrayBuffer> {
    void reconId;
    void seq;
    void opts;
    return unsupportedDenseMesh();
  }

  readDepthMap(
    reconId: string,
    seq: number,
    imageName: string,
    opts?: RequestOptions,
  ): Promise<ArrayBuffer> {
    void reconId;
    void seq;
    void imageName;
    void opts;
    return unsupportedDenseMesh();
  }

  readNormalMap(
    reconId: string,
    seq: number,
    imageName: string,
    opts?: RequestOptions,
  ): Promise<ArrayBuffer> {
    void reconId;
    void seq;
    void imageName;
    void opts;
    return unsupportedDenseMesh();
  }

  readMeshManifest(
    reconId: string,
    seq: number,
    opts?: RequestOptions,
  ): Promise<MeshFile> {
    void reconId;
    void seq;
    void opts;
    return unsupportedDenseMesh();
  }

  readMeshPly(
    reconId: string,
    seq: number,
    opts?: RequestOptions,
  ): Promise<ArrayBuffer> {
    void reconId;
    void seq;
    void opts;
    return unsupportedDenseMesh();
  }

  async getLocalizationResult(
    jobId: string,
    opts?: RequestOptions,
  ): Promise<LocalizationResult> {
    const job = await this.getJob(jobId, opts);
    for (const t of job.tasks) {
      if (t.kind === "localize" && t.outputs_ref) {
        return t.outputs_ref as unknown as LocalizationResult;
      }
    }
    throw new Error(`job ${jobId} has no completed localize task`);
  }

  // --- meta (extended) -------------------------------------------

  readyz(opts?: RequestOptions): Promise<unknown> {
    return this.req("GET", "/readyz", {}, opts).then((r) => r.json());
  }

  spec(opts?: RequestOptions): Promise<unknown> {
    return this.req("GET", "/spec", {}, opts).then((r) => r.json());
  }

  openapi(opts?: RequestOptions): Promise<unknown> {
    return this.req("GET", "/openapi.json", {}, opts).then((r) => r.json());
  }

  metrics(opts?: RequestOptions): Promise<string> {
    return this.req("GET", "/metrics", {}, opts).then((r) => r.text());
  }

  // --- projects (extended) ---------------------------------------

  patchProject(
    projectId: string,
    patch: ProjectPatch,
    opts?: RequestOptions,
  ): Promise<Project> {
    return this.req(
      "PATCH",
      `/v1/projects/${projectId}`,
      { json: patch },
      opts,
    ).then((r) => r.json());
  }

  // --- datasets (extended) ---------------------------------------

  patchDataset(
    projectId: string,
    datasetId: string,
    patch: DatasetPatch,
    opts?: RequestOptions,
  ): Promise<Dataset> {
    return this.req(
      "PATCH",
      `/v1/projects/${projectId}/datasets/${datasetId}`,
      { json: patch },
      opts,
    ).then((r) => r.json());
  }

  // --- images (extended) -----------------------------------------

  batchCreateImages(
    datasetId: string,
    body: BatchCreateImagesRequest,
    opts?: RequestOptions,
  ): Promise<BatchCreateImagesResponse> {
    return this.req(
      "POST",
      `/v1/datasets/${datasetId}/images:batchCreate`,
      { json: body },
      opts,
    ).then((r) => r.json());
  }

  async deleteImage(
    datasetId: string,
    name: string,
    opts?: RequestOptions,
  ): Promise<void> {
    await this.req(
      "DELETE",
      `/v1/datasets/${datasetId}/images/${name}`,
      {},
      opts,
    );
  }

  getImage(imageId: string, opts?: RequestOptions): Promise<Image> {
    return this.req("GET", `/v1/images/${imageId}`, {}, opts).then((r) =>
      r.json(),
    );
  }

  getImageBytes(
    imageId: string,
    options: { download?: boolean } = {},
    opts?: RequestOptions,
  ): Promise<ArrayBuffer> {
    const q = options.download ? "?download=true" : "";
    return this.req("GET", `/v1/images/${imageId}/bytes${q}`, {}, opts).then(
      (r) => r.arrayBuffer(),
    );
  }

  getImageThumbnail(
    imageId: string,
    options: { size?: number } = {},
    opts?: RequestOptions,
  ): Promise<ArrayBuffer> {
    const q = options.size ? `?size=${options.size}` : "";
    return this.req(
      "GET",
      `/v1/images/${imageId}/thumbnail${q}`,
      {},
      opts,
    ).then((r) => r.arrayBuffer());
  }

  getImageExif(
    imageId: string,
    opts?: RequestOptions,
  ): Promise<Record<string, unknown>> {
    return this.req("GET", `/v1/images/${imageId}/exif`, {}, opts).then((r) =>
      r.json(),
    );
  }

  // --- uploads (extended) ----------------------------------------

  getUpload(uploadId: string, opts?: RequestOptions): Promise<Upload> {
    return this.req("GET", `/v1/uploads/${uploadId}`, {}, opts).then((r) =>
      r.json(),
    );
  }

  // --- reconstructions / submodels (extended) --------------------

  getSubmodel(submodelId: string, opts?: RequestOptions): Promise<SubModel> {
    return this.req("GET", `/v1/submodels/${submodelId}`, {}, opts).then(
      (r) => r.json(),
    );
  }

  // --- snapshot inspection (observations / visibility / tiles) ---

  async readImageObservations(
    reconId: string,
    seq: number,
    imageId: string,
    opts?: RequestOptions,
  ): Promise<ImageObservationRow[]> {
    const r = await this.req(
      "GET",
      `/v1/reconstructions/${reconId}/snapshots/${seq}/images/${imageId}/observations`,
      {},
      opts,
    );
    const body = (await r.json()) as { observations?: ImageObservationRow[] };
    return body.observations ?? [];
  }

  async readPointVisibility(
    reconId: string,
    seq: number,
    point3dId: string,
    opts?: RequestOptions,
  ): Promise<PointObservationRow[]> {
    const r = await this.req(
      "GET",
      `/v1/reconstructions/${reconId}/snapshots/${seq}/points/${point3dId}/visibility`,
      {},
      opts,
    );
    const body = (await r.json()) as { observations?: PointObservationRow[] };
    return body.observations ?? [];
  }

  readTilesIndex(
    reconId: string,
    seq: number,
    options: { max_level?: number } = {},
    opts?: RequestOptions,
  ): Promise<TilesIndex> {
    const q = options.max_level ? `?max_level=${options.max_level}` : "";
    return this.req(
      "GET",
      `/v1/reconstructions/${reconId}/snapshots/${seq}/tiles/index.json${q}`,
      {},
      opts,
    ).then((r) => r.json());
  }

  readTile(
    reconId: string,
    seq: number,
    level: number,
    x: number,
    y: number,
    z: number,
    opts?: RequestOptions,
  ): Promise<ArrayBuffer> {
    return this.req(
      "GET",
      `/v1/reconstructions/${reconId}/snapshots/${seq}/tiles/${level}/${x}/${y}/${z}.bin`,
      {},
      opts,
    ).then((r) => r.arrayBuffer());
  }

  // --- admin: api keys -------------------------------------------

  listApiKeys(opts?: RequestOptions): Promise<ApiKey[]> {
    return this.req("GET", "/v1/admin/api-keys", {}, opts)
      .then((r) => r.json())
      .then((items: ApiKey[]) => items.map((item) => this.normalizeApiKey(item)));
  }

  createApiKey(
    body: { tenant_id?: string; name?: string | null; label?: string | null },
    opts?: RequestOptions,
  ): Promise<ApiKeyCreated>;
  createApiKey(name?: string | null, opts?: RequestOptions): Promise<ApiKeyCreated>;
  createApiKey(
    bodyOrName?: { tenant_id?: string; name?: string | null; label?: string | null } | string | null,
    opts?: RequestOptions,
  ): Promise<ApiKeyCreated> {
    const body = this.normalizeApiKeyCreateBody(bodyOrName);
    return this.req(
      "POST",
      "/v1/admin/api-keys",
      { json: body },
      opts,
    ).then((r) => r.json()).then((item: ApiKeyCreated) => this.normalizeApiKey(item));
  }

  createApiKeyForTenant(
    tenantId: string,
    name?: string | null,
    opts?: RequestOptions,
  ): Promise<ApiKeyCreated> {
    const body: { tenant_id: string; name?: string | null } = { tenant_id: tenantId };
    if (name !== undefined) body.name = name;
    return this.createApiKey(body, opts);
  }

  async deleteApiKey(apiKeyId: string, opts?: RequestOptions): Promise<void> {
    await this.req("DELETE", `/v1/admin/api-keys/${apiKeyId}`, {}, opts);
  }

  private normalizeApiKeyCreateBody(
    bodyOrName?: { tenant_id?: string; name?: string | null; label?: string | null } | string | null,
  ): { tenant_id: string; name?: string | null } {
    if (typeof bodyOrName === "object" && bodyOrName !== null) {
      const name = bodyOrName.name ?? bodyOrName.label;
      return {
        tenant_id: bodyOrName.tenant_id ?? "default",
        ...(name == null ? {} : { name }),
      };
    }
    return {
      tenant_id: "default",
      ...(bodyOrName == null ? {} : { name: bodyOrName }),
    };
  }

  private normalizeApiKey<T extends ApiKey>(item: T): T {
    if (item.label === undefined && item.name !== undefined) {
      return { ...item, label: item.name };
    }
    return item;
  }
}
