// Type-only mirror of `app/core/capabilities.py`. Keep this file in
// lock-step with the server's registry — the canonical capability
// names are part of the wire standard.

export interface BackendInfo {
  name: string;
  version: string;
  vendor?: string;
}

/** Wire schema version of the Capabilities envelope. Bump when the
 * *shape* changes (new top-level fields, type changes); independent
 * of the feature flags themselves. */
export const CAPABILITIES_SCHEMA_VERSION = 1;

export interface Capabilities {
  /** Wire schema version. See {@link CAPABILITIES_SCHEMA_VERSION}. */
  schema_version: number;
  backend: BackendInfo;
  /** Flat dict from canonical capability name to bool. Absence means
   * "unsupported"; clients MUST treat unknown keys as opaque. */
  features: Record<string, boolean>;
}

/** CORE capabilities — every conforming server advertises these as
 * `true`. */
export const CORE_CAPABILITIES = [
  "projects.crud",
  "datasets.crud",
  "images.crud",
  "uploads.chunked",
  "jobs.read",
  "events.sse",
  "spec.read",
] as const;

/** OPTIONAL capabilities — backends report any subset. */
export const OPTIONAL_CAPABILITIES = [
  "features.extract.sift",
  "features.extract.superpoint",
  "features.extract.aliked",
  "features.extract.disk",
  "features.extract.r2d2",
  "features.extract.d2net",
  "features.extract.sosnet",
  "pairs.exhaustive",
  "pairs.sequential",
  "pairs.spatial",
  "pairs.vocabtree",
  "pairs.retrieval",
  "pairs.from_poses",
  "pairs.explicit",
  "matchers.nn-mutual",
  "matchers.nn-ratio",
  "matchers.superglue",
  "matchers.lightglue",
  "matchers.loftr",
  "matchers.mast3r",
  "matches.verify",
  "geometry.two_view",
  "map.incremental",
  "map.global",
  "map.hierarchical",
  "map.spherical",
  "ba.standard",
  "ba.two_stage",
  "ba.featuremetric",
  "ba.rig",
  "triangulate.retri",
  "relocalize.images",
  "pgo.optimize",
  "recon.merge",
  "localize.batch",
  "localize.sequence",
  "export.ply",
  "export.nvm",
  "export.colmap_text",
  "export.colmap_bin",
  "export.nerfstudio",
  "export.gaussian_splatting",
  "export.instant_ngp",
  "export.kapture",
  "similarity.dhash",
  "similarity.vlad",
  "index.vocab_tree",
  "images.thumbnail",
  "localize.from_memory",
  "georegister.sim3",
  "georegister.gps",
  "image.undistort",
  "projection.equirectangular_to_cubemap",
  "projection.cubemap_to_equirectangular",
  "projection.equirectangular_to_perspective",
  "projection.cubemap_rig",
  "spherical.to_cubemap",
  "spherical.render_cubemap",
  "rigs.configure",
  "pose_priors.read_write",
  "pose_priors.mapping",
  "inputs.imu",
  "inputs.timestamps",
  "video.frame_extract",
  "import.kapture",
  "import.archive",
  "observations.by_image",
  "observations.by_point",
  "radiance.train",
  "radiance.evaluate",
  "radiance.metrics.psnr",
  "radiance.metrics.ssim",
  "radiance.metrics.lpips",
  "backend.actions",
  "backend.action_schema",
  "backend.action_validate",
  "backend.action_jobs",
  "backend.config_schemas",
  "backend.artifact_contracts",
  "pipelines.custom_execution",
  "compute.in_memory",
  "segment.sam",
] as const;

export type CoreCapability = (typeof CORE_CAPABILITIES)[number];
export type OptionalCapability = (typeof OPTIONAL_CAPABILITIES)[number];
export type CanonicalCapability = CoreCapability | OptionalCapability;

/** Returns true iff the capabilities snapshot advertises `name`. */
export function supports(caps: Capabilities, name: string): boolean {
  return Boolean(caps.features?.[name]);
}
