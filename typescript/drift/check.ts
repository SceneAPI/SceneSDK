/**
 * Structural drift check between the hand-rolled SDK models in
 * `src/models.ts` and the auto-generated OpenAPI types in
 * `src/_generated/openapi.d.ts`.
 *
 * Strategy: declare a series of `const _: GeneratedShape = {} as
 * SdkShape` assignments under `as` casts that force structural
 * compatibility in BOTH directions. If a server schema field is added
 * or renamed and the SDK model isn't updated to match, this file
 * stops type-checking — `npm run check:openapi-drift` fails, which
 * the CI gates on.
 *
 * The asymmetry table below documents intentional divergences:
 *
 *   - The SDK model fields use `string` for ULIDs; the OpenAPI schema
 *     also uses `string`. No mismatch.
 *   - The SDK uses `string` for `created_at`; the OpenAPI schema does
 *     too (FastAPI emits `datetime` as ISO strings).
 *   - `Page<T>` in the SDK is a generic; the generated schema
 *     produces one type per instantiation (`Page_ImageOut_`,
 *     `Page_ProjectOut_`). We check each instantiation explicitly.
 *   - The dataflow/processor preview surface (`AttributeOut`,
 *     `DataTypesContractOut`, `OperationsContractOut`,
 *     `ProcessorsContractOut`, `PipelinesContractOut`,
 *     `PipelineDefinition*`, `PipelineValidate*`, `ChainErrorOut`,
 *     `PortSpecOut`) is preview-fenced OUT of the published OpenAPI
 *     contract. The hand-rolled models keep those types, but there is
 *     no generated counterpart to pin them against — instead the
 *     `_FencedOut` block below asserts those schema names stay ABSENT
 *     from the generated contract, so a fence regression (preview
 *     schemas leaking into the public document) fails this check and
 *     re-adding the structural rows becomes a conscious step.
 *
 * This file never executes — it only exists for `tsc --noEmit`.
 */

import type { components } from "../src/_generated/openapi.js";
import type {
  ApiKey,
  ApiKeyCreated,
  ArtifactConversionPlanOut,
  ArtifactConversionPlanRequest,
  ArtifactConversionStepOut,
  ArtifactConvertRequest,
  ArtifactFileRef,
  ArtifactFormatOut,
  ArtifactImportRequest,
  ArtifactKindOut,
  ArtifactValidationIssueOut,
  ArtifactValidationOut,
  BundleAdjustmentSpec,
  Dataset,
  Image,
  Job,
  JobDetail,
  JobSubmitResponse,
  PipelineRunRequest,
  PipelineStep,
  ProcessorPipelineStep,
  Project,
  Reconstruction,
  StageArtifact,
  SubModel,
  Task,
  Upload,
  Page,
} from "../src/models.js";

type Schema<K extends keyof components["schemas"]> = components["schemas"][K];

// Helper: compile-time "A and B have the same field names". Runs both
// directions so neither side can grow a field without the other.
type SameKeys<A, B> = keyof A extends keyof B
  ? keyof B extends keyof A
    ? true
    : ["DRIFT: B has extra keys", Exclude<keyof B, keyof A>]
  : ["DRIFT: A has extra keys", Exclude<keyof A, keyof B>];

// Helper: deep "A is assignable to B AND B is assignable to A." This catches
// value-domain drift such as a new enum literal, not just missing fields.
type _Same<A, B> = SameKeys<A, B> extends true
  ? [A] extends [B]
    ? [B] extends [A]
      ? true
      : ["DRIFT: SDK not assignable to generated", B, A]
    : ["DRIFT: generated not assignable to SDK", A, B]
  : SameKeys<A, B>;

type WithRequiredDefaults<T, K extends keyof T> = Omit<T, K> & {
  [P in K]-?: Exclude<T[P], undefined>;
};

// --- Per-resource invariants ------------------------------------------------

const _project: _Same<Schema<"ProjectOut">, Project> = true;
const _dataset: _Same<Schema<"DatasetOut">, Dataset> = true;
const _image: _Same<Schema<"ImageOut">, Image> = true;
const _upload: _Same<Schema<"UploadOut">, Upload> = true;
const _job: _Same<Schema<"JobOut">, Job> = true;
const _jobDetail: _Same<Schema<"JobDetail">, JobDetail> = true;
const _jobAccepted: _Same<
  WithRequiredDefaults<Schema<"JobAcceptedResponse">, "task_ids">,
  JobSubmitResponse
> = true;
const _task: _Same<Schema<"TaskOut">, Task> = true;
const _recon: _Same<Schema<"ReconstructionOut">, Reconstruction> = true;
const _submodel: _Same<Schema<"SubModelOut">, SubModel> = true;
const _apiKey: _Same<
  Schema<"ApiKeyOut">,
  WithRequiredDefaults<
    Pick<ApiKey, "api_key_id" | "tenant_id" | "name" | "revoked">,
    "name" | "revoked"
  >
> = true;
const _apiKeyCreated: _Same<
  Schema<"IssueKeyResponse">,
  WithRequiredDefaults<
    Pick<ApiKeyCreated, "api_key_id" | "tenant_id" | "name" | "raw_key">,
    "name"
  >
> = true;
const _bundleAdjustmentSpec: _Same<
  Schema<"BundleAdjustmentSpec">,
  WithRequiredDefaults<
    BundleAdjustmentSpec,
    | "version"
    | "mode"
    | "refine_focal_length"
    | "refine_principal_point"
    | "refine_extra_params"
    | "max_num_iterations"
    | "loss_kernel"
    | "loss_threshold"
  >
> = true;
const _artifactKind: _Same<Schema<"ArtifactKindOut">, ArtifactKindOut> = true;
const _artifactFormat: _Same<
  Schema<"ArtifactFormatOut">,
  ArtifactFormatOut
> = true;
const _artifactConversionStep: _Same<
  Schema<"ArtifactConversionStepOut">,
  ArtifactConversionStepOut
> = true;
const _artifactConversionPlan: _Same<
  Schema<"ArtifactConversionPlanOut">,
  ArtifactConversionPlanOut
> = true;
const _artifactConversionPlanRequest: _Same<
  Schema<"ArtifactConversionPlanRequest">,
  ArtifactConversionPlanRequest
> = true;
const _artifactConvertRequest: _Same<
  Schema<"ArtifactConvertRequest">,
  ArtifactConvertRequest
> = true;
const _artifactFileRef: _Same<Schema<"ArtifactFileRef">, ArtifactFileRef> =
  true;
const _artifactImportRequest: _Same<
  Schema<"ArtifactImportRequest">,
  ArtifactImportRequest
> = true;
const _artifactValidationIssue: _Same<
  Schema<"ArtifactValidationIssueOut">,
  ArtifactValidationIssueOut
> = true;
const _artifactValidation: _Same<
  Schema<"ArtifactValidationOut">,
  ArtifactValidationOut
> = true;
const _stageArtifact: _Same<Schema<"StageArtifactOut">, StageArtifact> = true;
const _pipelineStep: _Same<Schema<"PipelineStep">, PipelineStep> = true;
const _processorPipelineStep: _Same<
  Schema<"ProcessorPipelineStep">,
  ProcessorPipelineStep
> = true;
const _pipelineRunRequest: _Same<
  Schema<"PipelineRunRequest">,
  PipelineRunRequest
> = true;

// --- Preview fence ----------------------------------------------------------
//
// The dataflow/processor preview surface is intentionally excluded from
// the published OpenAPI document (preview fence). These names must stay
// ABSENT from the generated schema map: if one shows up, the fence
// regressed (a preview route/schema leaked into the public contract) and
// the corresponding structural `_Same` row above must be reinstated.
type _FencedOut<K extends string> = K extends keyof components["schemas"]
  ? ["DRIFT: preview schema leaked into the fenced contract", K]
  : true;

const _fencedAttributeOut: _FencedOut<"AttributeOut"> = true;
const _fencedAttributesContract: _FencedOut<"AttributesContractOut"> = true;
const _fencedDataTypeOut: _FencedOut<"DataTypeOut"> = true;
const _fencedDataTypesContract: _FencedOut<"DataTypesContractOut"> = true;
const _fencedOperationOut: _FencedOut<"OperationOut"> = true;
const _fencedOperationsContract: _FencedOut<"OperationsContractOut"> = true;
const _fencedPortSpecOut: _FencedOut<"PortSpecOut"> = true;
const _fencedProcessorOut: _FencedOut<"ProcessorOut"> = true;
const _fencedProcessorsContract: _FencedOut<"ProcessorsContractOut"> = true;
const _fencedPipelineDefinitionStep: _FencedOut<"PipelineDefinitionStepOut"> =
  true;
const _fencedPipelineDefinition: _FencedOut<"PipelineDefinitionOut"> = true;
const _fencedPipelinesContract: _FencedOut<"PipelinesContractOut"> = true;
const _fencedChainError: _FencedOut<"ChainErrorOut"> = true;
const _fencedPipelineValidateRequest: _FencedOut<"PipelineValidateRequest"> =
  true;
const _fencedPipelineValidateResponse: _FencedOut<"PipelineValidateResponse"> =
  true;

// Generic Page<T> instantiations:
const _pageProj: _Same<Schema<"Page_ProjectOut_">, Page<Project>> = true;
const _pageDataset: _Same<Schema<"Page_DatasetOut_">, Page<Dataset>> = true;
const _pageImg: _Same<Schema<"Page_ImageOut_">, Page<Image>> = true;
const _pageSubmodel: _Same<Schema<"Page_SubModelOut_">, Page<SubModel>> = true;
const _pageArtifactKind: _Same<
  Schema<"Page_ArtifactKindOut_">,
  Page<ArtifactKindOut>
> = true;
const _pageArtifactFormat: _Same<
  Schema<"Page_ArtifactFormatOut_">,
  Page<ArtifactFormatOut>
> = true;
const _pageStageArtifact: _Same<
  Schema<"Page_StageArtifactOut_">,
  Page<StageArtifact>
> = true;

// Touch the bindings so the compiler doesn't report them as unused.
export const _drift = [
  _project,
  _dataset,
  _image,
  _upload,
  _job,
  _recon,
  _submodel,
  _apiKey,
  _apiKeyCreated,
  _bundleAdjustmentSpec,
  _artifactKind,
  _artifactFormat,
  _artifactConversionStep,
  _artifactConversionPlan,
  _artifactConversionPlanRequest,
  _artifactConvertRequest,
  _artifactFileRef,
  _artifactImportRequest,
  _artifactValidationIssue,
  _artifactValidation,
  _stageArtifact,
  _pipelineStep,
  _processorPipelineStep,
  _pipelineRunRequest,
  _fencedAttributeOut,
  _fencedAttributesContract,
  _fencedDataTypeOut,
  _fencedDataTypesContract,
  _fencedOperationOut,
  _fencedOperationsContract,
  _fencedPortSpecOut,
  _fencedProcessorOut,
  _fencedProcessorsContract,
  _fencedPipelineDefinitionStep,
  _fencedPipelineDefinition,
  _fencedPipelinesContract,
  _fencedChainError,
  _fencedPipelineValidateRequest,
  _fencedPipelineValidateResponse,
  _pageProj,
  _pageDataset,
  _pageImg,
  _pageSubmodel,
  _pageArtifactKind,
  _pageArtifactFormat,
  _pageStageArtifact,
];
