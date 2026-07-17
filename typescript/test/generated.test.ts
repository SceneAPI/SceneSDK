// Replays the same Python-recorded fixtures through the generated
// TypeScript types. The hand-rolled contract test (contract.test.ts)
// asserts the hand-rolled interfaces; this one asserts the generated
// `components["schemas"]["X"]` shapes — if the two diverge, the
// codegen flip exposes the gap.

import { describe, expect, it } from "vitest";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";

import type { components } from "../src/_generated/openapi.js";
import type { JobSubmitResponse } from "../src/models.js";

const FIXTURE_DIR = resolve(__dirname, "../../cpp/test/contract/fixtures");
if (
  !existsSync(FIXTURE_DIR) ||
  !readdirSync(FIXTURE_DIR).some((f) => f.endsWith(".json"))
) {
  throw new Error(`Missing SDK contract fixtures: ${FIXTURE_DIR}`);
}

function load<T>(name: string): T {
  return JSON.parse(readFileSync(join(FIXTURE_DIR, `${name}.json`), "utf-8")) as T;
}

type CapabilitiesOut = components["schemas"]["CapabilitiesOut"];
type HealthResponse = components["schemas"]["HealthResponse"];
type VersionResponse = components["schemas"]["VersionResponse"];
type SpecResponse = components["schemas"]["SpecResponse"];
type ProjectOut = components["schemas"]["ProjectOut"];
type DatasetOut = components["schemas"]["DatasetOut"];
type UploadOut = components["schemas"]["UploadOut"];
type JobAcceptedResponse = components["schemas"]["JobAcceptedResponse"];
type SnapshotListResponse = components["schemas"]["SnapshotListResponse"];
type ArtifactConversionPlanRequest = components["schemas"]["ArtifactConversionPlanRequest"];
type ArtifactConvertRequest = components["schemas"]["ArtifactConvertRequest"];

describe("contract: generated TS types decode fixtures", () => {
  it("CapabilitiesOut carries schema_version + backend + features", () => {
    const c = load<CapabilitiesOut>("capabilities");
    expect(c.schema_version).toBe(1);
    expect(c.backend.name).toBeTruthy();
    expect(typeof c.features).toBe("object");
  });

  it("HealthResponse decodes", () => {
    const h = load<HealthResponse>("healthz");
    expect(h.status).toBeTruthy();
  });

  it("VersionResponse decodes", () => {
    const v = load<VersionResponse>("version");
    expect(v.sfmapi).toBeTruthy();
    if (v.backend) {
      expect(typeof v.backend.name).toBe("string");
      expect(typeof v.backend.version).toBe("string");
    }
  });

  it("SpecResponse decodes", () => {
    const s = load<SpecResponse>("spec");
    expect(s.spec).toBe("sfmapi");
    expect(s.spec_version).toBeTruthy();
    expect(s.openapi_url).toBeTruthy();
    expect(s.server.name).toBeTruthy();
  });

  it("ProjectOut decodes for both create + get", () => {
    for (const name of ["project_get", "project_create"] as const) {
      const p = load<ProjectOut>(name);
      expect(p.project_id).toMatch(/^[0-9A-Z]{26}$/);
      expect(p.tenant_id).toBeTruthy();
      expect(p.name).toBeTruthy();
    }
  });

  it("DatasetOut decodes", () => {
    const d = load<DatasetOut>("dataset_create");
    expect(d.dataset_id).toMatch(/^[0-9A-Z]{26}$/);
    expect(d.project_id).toMatch(/^[0-9A-Z]{26}$/);
    expect(d.camera_model).toBeTruthy();
  });

  it("UploadOut decodes", () => {
    const u = load<UploadOut>("upload_init");
    expect(u.upload_id).toMatch(/^[0-9A-Z]{26}$/);
    expect(u.state).toBe("open");
    expect(u.received_bytes).toBe(0);
  });

  it("hand-rolled and generated JobAcceptedResponse types align", () => {
    // Real recorded fixture from the features stage submission.
    const j = load<JobAcceptedResponse>("job_accepted_features");
    const handRolled: JobSubmitResponse = {
      job_id: j.job_id,
      task_ids: j.task_ids ?? [],
      recon_id: j.recon_id ?? null,
      dataset_id: j.dataset_id ?? null,
      project_id: j.project_id ?? null,
      method: j.method ?? null,
      applied_sim3: j.applied_sim3 ?? null,
      target_recon_id: j.target_recon_id ?? null,
      source_recon_ids: j.source_recon_ids ?? null,
      strategy: j.strategy ?? null,
      action_id: j.action_id ?? null,
      backend: j.backend ?? null,
      provider: j.provider ?? null,
      artifact_id: j.artifact_id ?? null,
      target_format: j.target_format ?? null,
      radiance_field_id: j.radiance_field_id ?? null,
      radiance_evaluation_id: j.radiance_evaluation_id ?? null,
    };
    expect(j.job_id).toMatch(/^[0-9A-Z]{26}$/);
    expect(Array.isArray(j.task_ids)).toBe(true);
    expect((j.task_ids ?? []).length).toBeGreaterThanOrEqual(1);
    expect(Object.keys(j).sort()).toEqual([
      "action_id",
      "applied_sim3",
      "artifact_id",
      "backend",
      "dataset_id",
      "job_id",
      "method",
      "project_id",
      "provider",
      "radiance_evaluation_id",
      "radiance_field_id",
      "recon_id",
      "source_recon_ids",
      "strategy",
      "target_format",
      "target_recon_id",
      "task_ids",
    ]);
    expect(handRolled.provider).toBeNull();
    expect(handRolled.artifact_id).toBeNull();
    expect(handRolled.radiance_field_id).toBeNull();
  });

  it("SnapshotListResponse decodes empty list", () => {
    const s = load<SnapshotListResponse>("snapshot_list_empty");
    expect(s.seqs).toEqual([]);
  });

  it("conversion request types allow defaulted lossless flag omission", () => {
    const plan: ArtifactConversionPlanRequest = {
      to_format: "sfmapi.features.local.v1",
    };
    const planByAcceptedFormats: ArtifactConversionPlanRequest = {
      accepted_formats: ["sfmapi.features.local.v1"],
      require_lossless: true,
    };
    const convert: ArtifactConvertRequest = {
      to_format: "sfmapi.features.local.v1",
      options: { preserve_metadata: true },
    };
    const convertByAcceptedFormats: ArtifactConvertRequest = {
      accepted_formats: ["sfmapi.features.local.v1"],
      name: "converted",
    };
    expect(plan.to_format).toBe(convert.to_format);
    expect(planByAcceptedFormats.accepted_formats[0]).toBe(
      convertByAcceptedFormats.accepted_formats[0],
    );

    // @ts-expect-error either to_format or non-empty accepted_formats is required
    const missingPlanTarget: ArtifactConversionPlanRequest = {};
    // @ts-expect-error accepted_formats must be statically non-empty when used as target
    const emptyPlanTargets: ArtifactConversionPlanRequest = { accepted_formats: [] };
    // @ts-expect-error accepted_formats must be statically non-empty when present
    const emptyPlanTargetsWithFormat: ArtifactConversionPlanRequest = { to_format: "sfmapi.features.local.v1", accepted_formats: [] };
    // @ts-expect-error either to_format or non-empty accepted_formats is required
    const missingConvertTarget: ArtifactConvertRequest = { options: {} };
    // @ts-expect-error accepted_formats must be statically non-empty when used as target
    const emptyConvertTargets: ArtifactConvertRequest = { accepted_formats: [] };
    // @ts-expect-error accepted_formats must be statically non-empty when present
    const emptyConvertTargetsWithFormat: ArtifactConvertRequest = { to_format: "sfmapi.features.local.v1", accepted_formats: [] };
    expect([
      missingPlanTarget,
      emptyPlanTargets,
      emptyPlanTargetsWithFormat,
      missingConvertTarget,
      emptyConvertTargets,
      emptyConvertTargetsWithFormat,
    ]).toHaveLength(6);
  });
});
