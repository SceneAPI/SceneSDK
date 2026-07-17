// Type-only mirror of the server schemas. Kept here so the SDK ships
// without depending on any runtime validator.

import type { components } from "./_generated/openapi.js";
import type { Sim3 } from "./scene.js";

type Schema<K extends keyof components["schemas"]> = components["schemas"][K];

export interface Page<T> {
  items: T[];
  next_page_token?: string | null;
  total?: number | null;
}

export interface ProjectCreate {
  name: string;
  description?: string | null;
}

export interface ProjectPatch {
  /** Partial update — unset fields are left untouched. */
  name?: string | null;
  description?: string | null;
}

export interface Project {
  project_id: string;
  tenant_id: string;
  name: string;
  description?: string | null;
  created_at: string;
  updated_at?: string | null;
  _links?: Record<string, { href?: string | null } | null> | null;
}

export interface UploadSourceSpec {
  kind: "upload";
  entries: Array<{ name: string; blob_sha: string }>;
}

export interface LocalSourceSpec {
  kind: "local";
  root: string;
  recursive?: boolean;
}

export interface S3SourceSpec {
  kind: "s3";
  bucket: string;
  prefix: string;
}

export type SourceSpec = UploadSourceSpec | LocalSourceSpec | S3SourceSpec;

export interface DatasetCreate {
  name: string;
  source: SourceSpec;
  camera_model?: string;
  intrinsics_mode?: "single_camera" | "per_image" | "per_folder";
  is_spherical?: boolean;
  rig_config?: Record<string, unknown> | null;
  respect_exif_orientation?: boolean;
}

export interface DatasetPatch {
  name?: string;
  camera_model?: string;
  intrinsics_mode?: "single_camera" | "per_image" | "per_folder";
  is_spherical?: boolean;
  rig_config?: Record<string, unknown> | null;
  respect_exif_orientation?: boolean;
  active_maskset_id?: string | null;
}

export interface ImageCreate {
  name: string;
  blob_sha?: string | null;
  rel_path?: string | null;
  width?: number | null;
  height?: number | null;
  exif?: Record<string, unknown> | null;
}

export interface BatchCreateImagesRequest {
  requests: ImageCreate[];
}

export interface BatchCreateImagesResponse {
  images: Image[];
}

export interface ImageObservationRow {
  point3d_id: number;
  x: number;
  y: number;
  kp_idx?: number;
  error?: number | null;
}

export interface PointObservationRow {
  image_id: number;
  x: number;
  y: number;
  kp_idx?: number;
}

export interface TilesIndex {
  bbox_min: number[];
  bbox_max: number[];
  levels: Array<Record<string, unknown>>;
}

export interface ApiKey {
  api_key_id: string;
  tenant_id: string;
  name?: string | null;
  /** Deprecated alias for name. */
  label?: string | null;
  created_at?: string | null;
  revoked?: boolean;
}

export interface ApiKeyCreated extends ApiKey {
  /** Bearer token — returned only at creation time. */
  raw_key: string;
}

export interface Dataset {
  dataset_id: string;
  tenant_id: string;
  project_id: string;
  source_id: string;
  name: string;
  camera_model: string;
  intrinsics_mode: string;
  is_spherical: boolean;
  respect_exif_orientation: boolean;
  /**
   * Server emits the column name (`rig_config_json`) directly. We mirror
   * the wire shape so JSON round-trips don't require renaming.
   */
  rig_config_json?: Record<string, unknown> | null;
  active_maskset_id?: string | null;
  manifest_hash: string;
  created_at: string;
  updated_at?: string | null;
  _links?: Record<string, { href?: string | null } | null> | null;
}

export interface Image {
  image_id: string;
  dataset_id: string;
  name: string;
  content_sha: string;
  source_kind: string;
  rel_path?: string | null;
  byte_size?: number | null;
  width?: number | null;
  height?: number | null;
  created_at: string;
  _links?: Record<string, { href?: string | null } | null> | null;
}

export interface Upload {
  upload_id: string;
  state: "open" | "received" | "finalized" | "expired";
  expected_size: number;
  received_bytes: number;
  blob_sha?: string | null;
  expires_at: string;
}

export type JobStatus =
  | "pending"
  | "running"
  | "succeeded"
  | "failed"
  | "cancelled"
  | "cancelled_dirty";

export type TaskStatus = JobStatus | "skipped";

export interface Task {
  task_id: string;
  job_id: string;
  kind: string;
  status: TaskStatus;
  cache_key: string;
  inputs_hash: string;
  params_hash: string;
  provider?: string | null;
  outputs_ref?: Record<string, unknown> | null;
}

export interface Job {
  job_id: string;
  tenant_id: string;
  project_id: string;
  recipe: string;
  status: JobStatus;
  cancel_requested: boolean;
  cancel_force: boolean;
  created_at: string;
  started_at?: string | null;
  finished_at?: string | null;
  error_class?: string | null;
  error_message?: string | null;
  _links?: Record<string, { href?: string | null } | null> | null;
}

export interface JobDetail extends Job {
  tasks: Task[];
}

export interface Reconstruction {
  recon_id: string;
  project_id: string;
  dataset_id: string;
  dataset_snapshot_hash: string;
  spec:
    | Schema<"IncrementalSpec">
    | Schema<"GlobalSpec">
    | Schema<"HierarchicalSpec">
    | Schema<"SphericalSpec">;
  rv_id: string;
  status: "running" | "succeeded" | "failed" | "cancelled" | "cancelled_dirty";
  created_at: string;
  _links?: Record<string, { href?: string | null } | null> | null;
}

export interface SubModel {
  submodel_id: string;
  recon_id: string;
  idx: number;
  parent_submodel_id?: string | null;
  summary?: Record<string, unknown> | null;
  rigidity?: Record<string, unknown> | null;
  snapshot_seq?: number | null;
  sealed_path?: string | null;
  created_at: string;
  _links?: Record<string, { href?: string | null } | null> | null;
}

export interface JobSubmitResponse {
  job_id: string;
  task_ids: string[];
  recon_id?: string | null;
  dataset_id?: string | null;
  project_id?: string | null;
  method?: string | null;
  applied_sim3?: Sim3 | null;
  target_recon_id?: string | null;
  source_recon_ids?: string[] | null;
  strategy?: string | null;
  action_id?: string | null;
  backend?: string | null;
  provider?: string | null;
  artifact_id?: string | null;
  target_format?: string | null;
  radiance_field_id?: string | null;
  radiance_evaluation_id?: string | null;
}

export interface HealthResponse {
  status: string;
}

export interface BackendVersion {
  name: string;
  version: string;
  vendor?: string | null;
  runtime_versions?: Record<string, string>;
}

export interface VersionResponse {
  sfmapi: string;
  backend?: BackendVersion | null;
}

// ----- Pipeline + stage specs ------------------------------------------------

export interface ArtifactInputRef {
  artifact_id: string;
  kind?: string | null;
}

export type ArtifactInputMap = Record<string, ArtifactInputRef>;

export interface ArtifactKindOut {
  kind: string;
  datatype: string;
  title: string;
  description: string;
  durable: boolean;
  artifact_format: string;
  schema_version: number;
}

export interface ArtifactFormatOut {
  format_id: string;
  datatype: string;
  title: string;
  description: string;
  schema_version: number;
  media_types: string[];
  json_schema?: Record<string, unknown> | null;
  examples?: Array<Record<string, unknown>>;
  portable: boolean;
}

export interface ArtifactConversionStepOut {
  contract_id?: string | null;
  backend?: string | null;
  provider?: string | null;
  from_format: string;
  to_format: string;
  lossless: boolean;
  description?: string | null;
}

export interface ArtifactConversionPlanOut {
  artifact_id: string;
  source_format?: string | null;
  target_format: string;
  conversion_required: boolean;
  executable: boolean;
  reason?: string | null;
  steps?: ArtifactConversionStepOut[];
}

interface ArtifactConversionPlanRequestBase {
  provider?: string | null;
  to_format?: string | null;
  accepted_formats?: [string, ...string[]];
  require_lossless?: boolean;
}

export type ArtifactConversionPlanRequest = ArtifactConversionPlanRequestBase &
  ({ to_format: string } | { accepted_formats: [string, ...string[]] });

export type ArtifactConvertRequest = ArtifactConversionPlanRequestBase &
  ({ to_format: string } | { accepted_formats: [string, ...string[]] }) & {
  name?: string | null;
  to_kind?: string | null;
  options?: Record<string, unknown>;
};

export interface ArtifactFileRef {
  name: string;
  uri: string;
  media_type?: string | null;
  sha256?: string | null;
  byte_size?: number | null;
}

export interface ArtifactImportRequest {
  project_id: string;
  recon_id?: string | null;
  dataset_id?: string | null;
  kind: string;
  name?: string | null;
  uri?: string | null;
  media_type?: string | null;
  artifact_format?: string | null;
  datatype?: string | null;
  schema_version?: number | null;
  files?: ArtifactFileRef[];
  sha256?: string | null;
  byte_size?: number | null;
  coordinate_frame?: string | null;
  producer?: Record<string, unknown> | null;
  summary?: Record<string, unknown> | null;
  metadata?: Record<string, unknown>;
}

export interface ArtifactValidationIssueOut {
  level: string;
  field?: string | null;
  message: string;
}

export interface ArtifactValidationOut {
  artifact_id: string;
  valid: boolean;
  artifact_format?: string | null;
  datatype?: string | null;
  checked_content: boolean;
  issues?: ArtifactValidationIssueOut[];
}

export interface StageArtifact {
  artifact_id: string;
  job_id: string;
  task_id: string;
  recon_id?: string | null;
  dataset_id?: string | null;
  kind: string;
  name?: string | null;
  uri?: string | null;
  media_type?: string | null;
  artifact_format?: string | null;
  datatype?: string | null;
  schema_version?: number | null;
  files?: ArtifactFileRef[];
  sha256?: string | null;
  byte_size?: number | null;
  coordinate_frame?: string | null;
  producer?: Record<string, unknown> | null;
  summary?: Record<string, unknown> | null;
  metadata?: Record<string, unknown> | null;
  created_at: string;
  _links?: Record<string, { href?: string | null } | null> | null;
}

/** Canonical local-feature extractors. Capability flag is
 * `features.extract.{type}`. Backends advertise the subset they
 * implement. */
export type FeatureType =
  | "sift"
  | "superpoint"
  | "aliked"
  | "disk"
  | "r2d2"
  | "d2net"
  | "sosnet";

export interface FeaturesSpec {
  version?: 1;
  type?: FeatureType;
  provider?: string | null;
  max_num_features?: number;
  use_gpu?: boolean;
  seed?: number;
  /** Backend-specific options discovered from `/v1/backend/config-schemas`. */
  backend_options?: Record<string, unknown>;
  input_artifacts?: ArtifactInputMap;
}

/** Pair-selection strategy. Capability flag is `pairs.{strategy}`. */
export type PairStrategy =
  | "exhaustive"
  | "sequential"
  | "spatial"
  | "vocabtree"
  | "retrieval"
  | "from_poses"
  | "explicit";

export interface ImagePairRef {
  image_name1: string;
  image_name2: string;
}

export interface PairsSpec {
  version?: 1;
  strategy?: PairStrategy;
  provider?: string | null;
  overlap?: number;
  vocab_tree_path?: string | null;
  retrieval_strategy?: "dhash" | "vlad" | "netvlad";
  retrieval_k?: number;
  overlap_distance_m?: number | null;
  max_angle_deg?: number | null;
  image_pairs?: ImagePairRef[] | null;
  pairs_blob_sha?: string | null;
  pairs_blob_format?: "image_name_pairs_txt";
  /** Backend-specific options discovered from `/v1/backend/config-schemas`. */
  backend_options?: Record<string, unknown>;
  input_artifacts?: ArtifactInputMap;
}

/** Per-pair matcher. Capability flag is `matchers.{type}`. */
export type MatcherType =
  | "nn-mutual"
  | "nn-ratio"
  | "superglue"
  | "lightglue"
  | "loftr"
  | "mast3r";

export interface MatcherSpec {
  version?: 1;
  type?: MatcherType;
  provider?: string | null;
  use_gpu?: boolean;
  cross_check?: boolean;
  max_ratio?: number;
  max_distance?: number;
  /** Backend-specific options discovered from `/v1/backend/config-schemas`. */
  backend_options?: Record<string, unknown>;
  input_artifacts?: ArtifactInputMap;
}

export interface VerifySpec {
  version?: 1;
  provider?: string | null;
  use_gpu?: boolean;
  min_inlier_ratio?: number;
  /** Backend-specific options discovered from `/v1/backend/config-schemas`. */
  backend_options?: Record<string, unknown>;
  input_artifacts?: ArtifactInputMap;
}

export interface BundleAdjustmentSpec {
  version?: 1;
  /** `featuremetric` requires capability `ba.featuremetric`. */
  mode?: "standard" | "two_stage" | "featuremetric" | "rig";
  provider?: string | null;
  refine_focal_length?: boolean;
  refine_principal_point?: boolean;
  refine_extra_params?: boolean;
  max_num_iterations?: number;
  loss_kernel?: "squared" | "huber" | "cauchy" | "soft_l1" | "tukey";
  loss_threshold?: number;
  /** Backend-specific options discovered from `/v1/backend/config-schemas`. */
  backend_options?: Record<string, unknown>;
}

interface _PipelineSpecBase {
  version?: 1;
  provider?: string | null;
  seed?: number;
  max_runtime_seconds?: number | null;
  snapshot_frames_freq?: number | null;
  /** Backend-specific options discovered from `/v1/backend/config-schemas`. */
  backend_options?: Record<string, unknown>;
  input_artifacts?: ArtifactInputMap;
}

export interface IncrementalSpec extends _PipelineSpecBase {
  kind: "incremental";
  init_image_pair?: [string, string] | null;
  multiple_models?: boolean;
  max_num_models?: number;
  min_num_matches?: number;
  ba_global_use_pba?: boolean;
  extract_colors?: boolean;
}

export interface GlobalSpec extends _PipelineSpecBase {
  kind: "global";
  backend?: "AUTO" | "BAXX" | "CERES";
  formulation?: "AUTO" | "EXPLICIT_SCALE" | "ELIMINATED_SCALE";
  use_incremental_quality_fallback?: boolean;
}

export interface HierarchicalSpec extends _PipelineSpecBase {
  kind: "hierarchical";
  cluster_max_size?: number;
  cluster_overlap?: number;
}

export interface SphericalSpec extends _PipelineSpecBase {
  kind: "spherical";
  panorama?: boolean;
}

export type PipelineSpec =
  | IncrementalSpec
  | GlobalSpec
  | HierarchicalSpec
  | SphericalSpec;

export interface ChainError {
  where: string;
  message: string;
  reason?: string | null;
  path?: string | null;
}

export interface AttributeOut {
  name: string;
  type: string;
  required: boolean;
  description: string;
  default?: unknown | null;
  enum?: string[] | null;
  min?: number | null;
  max?: number | null;
}

export interface DataTypeOut {
  type_id: string;
  title: string;
  kind: string;
  aliases: string[];
  description: string;
}

export interface PortSpecOut {
  datatype: string;
  required: boolean;
  multiple: boolean;
  description: string;
}

export interface ProcessorOut {
  processor_id: string;
  title: string;
  consumer: Record<string, PortSpecOut>;
  supplier: Record<string, PortSpecOut>;
  attributes: AttributeOut[];
  special_inputs: Record<string, PortSpecOut>;
  special_attributes: AttributeOut[];
  capabilities: string[];
  config_stage: string | null;
  aliases: string[];
  description: string;
}

export interface OperationOut {
  op_id: string;
  title: string;
  consumes: string[];
  produces: string[];
  capabilities: string[];
  config_stage: string | null;
  description: string;
}

export interface PipelineStep {
  op: string;
  provider?: string | null;
  params?: Record<string, unknown>;
}

export interface ProcessorPipelineStep {
  processor: string;
  ref?: string | null;
  provider?: string | null;
  attributes?: Record<string, unknown>;
  params?: Record<string, unknown>;
  wires?: Record<string, string | string[]>;
}

export interface PipelineDefinitionStepOut {
  ref: string;
  processor: string;
  attributes: Record<string, unknown>;
  wires: Record<string, string | string[]>;
}

export interface PipelineDefinitionOut {
  pipeline_id: string;
  title: string;
  aliases: string[];
  initial_inputs: string[];
  steps: PipelineDefinitionStepOut[];
  description: string;
}

export interface AttributesContractOut {
  contract: string;
  contract_schema_version: number;
  attribute_types: string[];
  rules: Record<string, string>;
}

export interface DataTypesContractOut {
  contract: string;
  contract_schema_version: number;
  kinds: string[];
  types: DataTypeOut[];
}

export interface OperationsContractOut {
  contract: string;
  contract_schema_version: number;
  operations: OperationOut[];
  compatibility: Record<string, string>;
}

export interface ProcessorsContractOut {
  contract: string;
  contract_schema_version: number;
  processors: ProcessorOut[];
  rules: Record<string, string>;
}

export interface PipelinesContractOut {
  contract: string;
  contract_schema_version: number;
  composition_rule: string;
  initial_inputs: string[];
  canonical_pipelines: Record<string, string[]>;
  plugin_pipelines: PipelineDefinitionOut[];
  step_schema: Record<string, unknown>;
  validation_reasons: string[];
}

export type PipelineStepLike = string | ProcessorPipelineStep | PipelineStep;

export interface PipelineValidateRequest {
  initial_inputs?: string[];
  steps: PipelineStepLike[];
}

export interface PipelineRunRequest extends PipelineValidateRequest {
  dataset_id: string;
}

export interface PipelineValidateResponse {
  valid: boolean;
  errors: ChainError[];
}

// ----- ProgressEvent (loose union) ------------------------------------------

export type ProgressEventKind =
  | "phase_started"
  | "phase_progress"
  | "phase_completed"
  | "metric"
  | "snapshot_available"
  | "log_line"
  | "warning"
  | "error";

export interface ProgressEvent {
  schema_version: 1;
  ts: string;
  job_id: string;
  task_id?: string | null;
  seq: number;
  kind: ProgressEventKind;
  phase?: string;
  current?: number;
  total?: number | null;
  rate?: number | null;
  key?: string;
  value?: number;
  snapshot_seq?: number;
  summary?: Record<string, unknown>;
  level?: "DEBUG" | "INFO" | "WARNING" | "ERROR";
  message?: string;
  error_class?: string;
  detail?: Record<string, unknown> | null;
}
