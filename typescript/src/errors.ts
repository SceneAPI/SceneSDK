// Client-side error hierarchy for sfmapi problem+json responses.

export interface ProblemJson {
  type?: string;
  title?: string;
  status?: number;
  detail?: string;
  instance?: string;
  [extra: string]: unknown;
}

export class SfmApiError extends Error {
  statusCode: number;
  detail: string;
  body: Record<string, unknown>;
  problem: ProblemJson;
  response: Response | undefined;

  constructor(
    messageOrStatus: string | number,
    detailOrOpts:
      | string
      | { statusCode?: number; problem?: ProblemJson; response?: Response }
      = {},
    body: Record<string, unknown> = {},
  ) {
    const generatedStyle = typeof messageOrStatus === "number";
    const opts: { statusCode?: number; problem?: ProblemJson; response?: Response } =
      generatedStyle || typeof detailOrOpts === "string" ? {} : detailOrOpts;
    const detail: string = generatedStyle
      ? typeof detailOrOpts === "string"
        ? detailOrOpts
        : ""
      : String(messageOrStatus);
    const problem: ProblemJson = generatedStyle ? (body as ProblemJson) : (opts.problem ?? {});
    const statusCode: number = generatedStyle
      ? messageOrStatus
      : (opts.statusCode ?? problem.status ?? 0);
    const message = generatedStyle ? detail || `sfmapi error: ${statusCode}` : String(messageOrStatus);
    super(message);
    this.name = new.target.name;
    this.statusCode = statusCode;
    this.detail = detail;
    this.body = problem as Record<string, unknown>;
    this.problem = problem;
    this.response = opts.response;
    // Preserve prototype chain across transpilation targets.
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

export class NotFoundError extends SfmApiError {}
export class ConflictError extends SfmApiError {}
export class ValidationError extends SfmApiError {}
export class AuthError extends SfmApiError {}
export class QuotaExceededError extends SfmApiError {}
export class StorageError extends SfmApiError {}
export class CapabilityUnavailableError extends SfmApiError {}
export class PycolmapUnavailableError extends CapabilityUnavailableError {}
export class BackendUnavailableError extends SfmApiError {}
export class TransportError extends SfmApiError {}

const STATUS_MAP: Record<number, new (...args: ConstructorParameters<typeof SfmApiError>) => SfmApiError> = {
  400: ValidationError,
  401: AuthError,
  403: AuthError,
  404: NotFoundError,
  409: ConflictError,
  413: QuotaExceededError,
  422: ValidationError,
  429: QuotaExceededError,
  501: CapabilityUnavailableError,
  503: BackendUnavailableError,
  507: StorageError,
};

export function buildSfmApiError(statusCode: number, body: unknown): SfmApiError {
  let detail = "";
  let problem: ProblemJson = {};
  if (body && typeof body === "object" && !Array.isArray(body)) {
    problem = body as ProblemJson;
    const d = problem.detail ?? problem.title;
    if (typeof d === "string") detail = d;
  } else if (typeof body === "string") {
    detail = body;
  }
  let Cls = STATUS_MAP[statusCode] ?? SfmApiError;
  if (Cls === CapabilityUnavailableError && problem.capability === "pycolmap") {
    Cls = PycolmapUnavailableError;
  }
  return new Cls(statusCode, detail, problem as Record<string, unknown>);
}

export async function raiseForResponse(resp: Response): Promise<void> {
  if (resp.ok) return;
  let problem: ProblemJson = {};
  const contentType = resp.headers.get("content-type") ?? "";
  if (contentType.includes("json")) {
    try {
      problem = (await resp.clone().json()) as ProblemJson;
    } catch {
      problem = { title: resp.statusText, status: resp.status };
    }
  }
  let body: unknown = problem;
  if (!Object.keys(problem).length) {
    body = (await resp.clone().text()) || resp.statusText;
  }
  const err = buildSfmApiError(resp.status, body);
  err.response = resp;
  throw err;
}
