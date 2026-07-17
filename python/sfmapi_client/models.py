"""Pydantic models — mirror the server schemas.

We deliberately keep these in the SDK rather than importing from `app.*`
so the SDK can be released independently and consumers don't have to
install the server-side deps (sqlalchemy, alembic, arq, ...).
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

T = TypeVar("T")


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class _ResponseBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


# -- Pagination --------------------------------------------------------------


class Page(_ResponseBase, Generic[T]):
    items: list[T]
    next_page_token: str | None = None
    total: int | None = None


# -- Projects / datasets / images / uploads ---------------------------------


class Link(_ResponseBase):
    href: str | None = None


class ProjectCreate(_Base):
    name: str
    description: str | None = None


class ProjectPatch(_Base):
    """Partial update; unset fields are left untouched."""

    name: str | None = None
    description: str | None = None


class Project(_ResponseBase):
    project_id: str
    tenant_id: str
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    links: dict[str, Link | None] | None = Field(default=None, alias="_links")


class UploadSourceSpec(_Base):
    kind: Literal["upload"] = "upload"
    entries: list[dict[str, str]] = Field(default_factory=list)


class LocalSourceSpec(_Base):
    kind: Literal["local"] = "local"
    root: str
    recursive: bool = True


class S3SourceSpec(_Base):
    kind: Literal["s3"] = "s3"
    bucket: str
    prefix: str


SourceSpec = Annotated[
    UploadSourceSpec | LocalSourceSpec | S3SourceSpec,
    Field(discriminator="kind"),
]


class DatasetCreate(_Base):
    name: str
    source: dict[str, Any]
    camera_model: str = "SIMPLE_RADIAL"
    intrinsics_mode: Literal["single_camera", "per_image", "per_folder"] = "single_camera"
    is_spherical: bool = False
    rig_config: dict[str, Any] | None = None
    respect_exif_orientation: bool = False


class DatasetPatch(_Base):
    name: str | None = None
    camera_model: str | None = None
    intrinsics_mode: Literal["single_camera", "per_image", "per_folder"] | None = None
    is_spherical: bool | None = None
    rig_config: dict[str, Any] | None = None
    respect_exif_orientation: bool | None = None
    active_maskset_id: str | None = None


class ImageCreate(_Base):
    name: str
    blob_sha: str | None = None
    rel_path: str | None = None
    width: int | None = None
    height: int | None = None
    exif: dict[str, Any] | None = None


class BatchCreateImagesRequest(_Base):
    """AIP-231 batch-create request body."""

    requests: list[ImageCreate] = Field(default_factory=list)


class BatchCreateImagesResponse(_ResponseBase):
    """AIP-231 batch-create response — created resources in
    request-order."""

    images: list[Image] = Field(default_factory=list)


class Image(_ResponseBase):
    image_id: str
    dataset_id: str
    name: str
    content_sha: str
    source_kind: str
    rel_path: str | None = None
    byte_size: int | None = None
    width: int | None = None
    height: int | None = None
    created_at: datetime
    links: dict[str, Link | None] | None = Field(default=None, alias="_links")


class Dataset(_ResponseBase):
    dataset_id: str
    tenant_id: str
    project_id: str
    source_id: str
    name: str
    camera_model: str
    intrinsics_mode: str
    is_spherical: bool
    respect_exif_orientation: bool
    rig_config: dict[str, Any] | None = Field(None, alias="rig_config_json")
    active_maskset_id: str | None = None
    manifest_hash: str
    created_at: datetime
    updated_at: datetime | None = None
    links: dict[str, Link | None] | None = Field(default=None, alias="_links")


class Upload(_ResponseBase):
    upload_id: str
    state: str
    expected_size: int
    received_bytes: int
    blob_sha: str | None = None
    expires_at: datetime


class ImageObservation(_ResponseBase):
    """Per-image observation row from the visibility sidecar."""

    point3d_id: int
    x: float
    y: float
    kp_idx: int = -1
    error: float | None = None


class PointObservation(_ResponseBase):
    """Per-point visibility row — which images observed a 3D point."""

    image_id: int
    x: float
    y: float
    kp_idx: int = -1


class TilesIndex(_ResponseBase):
    """Manifest of an octree-tiled point cloud snapshot."""

    bbox_min: list[float]
    bbox_max: list[float]
    levels: list[dict[str, Any]] = Field(default_factory=list)


class ApiKey(_ResponseBase):
    api_key_id: str
    tenant_id: str
    name: str | None = None
    label: str | None = None
    created_at: datetime | None = None
    revoked: bool = False

    @model_validator(mode="after")
    def _sync_legacy_label(self):
        if self.name is None and self.label is not None:
            self.name = self.label
        elif self.label is None and self.name is not None:
            self.label = self.name
        return self


class ApiKeyCreated(ApiKey):
    """Returned only at creation time. ``raw_key`` is the bearer
    token; the server never reveals it again."""

    raw_key: str


# -- Progress events (mirror of app/schemas/progress_event.py) -------------


ProgressEventKind = Literal[
    "phase_started",
    "phase_progress",
    "phase_completed",
    "metric",
    "snapshot_available",
    "log_line",
    "warning",
    "error",
]


class ProgressEvent(_ResponseBase):
    """Loose ProgressEvent shape — every backend kind decoded into a
    single Pydantic model with all kind-specific fields optional. The
    discriminator is ``kind``; readers switch on it and consume the
    relevant fields."""

    schema_version: Literal[1] = 1
    ts: datetime
    job_id: str
    task_id: str | None = None
    seq: int
    kind: ProgressEventKind
    # phase_*
    phase: str | None = None
    current: int | None = None
    total: int | None = None
    rate: float | None = None
    # metric
    key: str | None = None
    value: float | None = None
    # snapshot_available
    snapshot_seq: int | None = None
    summary: dict[str, Any] | None = None
    # log_line / warning / error
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] | None = None
    message: str | None = None
    error_class: str | None = None
    detail: dict[str, Any] | None = None


# -- Jobs / Tasks ------------------------------------------------------------


class Task(_ResponseBase):
    task_id: str
    job_id: str
    kind: str
    status: str
    provider: str | None = None
    cache_key: str
    inputs_hash: str
    params_hash: str
    outputs_ref: dict[str, Any] | None = None


class Job(_ResponseBase):
    job_id: str
    tenant_id: str
    project_id: str
    recipe: str
    status: str
    cancel_requested: bool = False
    cancel_force: bool = False
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_class: str | None = None
    error_message: str | None = None
    links: dict[str, Link | None] | None = Field(default=None, alias="_links")


class JobDetail(Job):
    tasks: list[Task] = Field(default_factory=list)


# -- Reconstructions / submodels --------------------------------------------


class Reconstruction(_ResponseBase):
    recon_id: str
    project_id: str
    dataset_id: str
    dataset_snapshot_hash: str
    spec: dict[str, Any]
    rv_id: str
    status: str
    created_at: datetime
    links: dict[str, Link | None] | None = Field(default=None, alias="_links")


class SubModel(_ResponseBase):
    submodel_id: str
    recon_id: str
    idx: int
    parent_submodel_id: str | None = None
    summary: dict[str, Any] | None = None
    rigidity: dict[str, Any] | None = None
    snapshot_seq: int | None = None
    sealed_path: str | None = None
    created_at: datetime
    links: dict[str, Link | None] | None = Field(default=None, alias="_links")


# -- Pipeline + stage specs (input shapes for job submission) ---------------


FeatureType = Literal["sift", "superpoint", "aliked", "disk", "r2d2", "d2net", "sosnet"]
PairStrategy = Literal[
    "exhaustive",
    "sequential",
    "spatial",
    "vocabtree",
    "retrieval",
    "from_poses",
    "explicit",
]
MatcherType = Literal["nn-mutual", "nn-ratio", "superglue", "lightglue", "loftr", "mast3r"]


class ArtifactInputRef(_Base):
    artifact_id: str
    kind: str | None = None


ArtifactInputMap = dict[str, ArtifactInputRef | dict[str, Any]]


class ArtifactKindOut(_ResponseBase):
    kind: str
    datatype: str
    title: str
    description: str
    durable: bool
    artifact_format: str
    schema_version: int


class ArtifactFormatOut(_ResponseBase):
    format_id: str
    datatype: str
    title: str
    description: str
    schema_version: int
    media_types: list[str]
    json_schema: dict[str, Any] | None = None
    examples: list[dict[str, Any]] = Field(default_factory=list)
    portable: bool = True


class ArtifactConversionStepOut(_ResponseBase):
    contract_id: str | None = None
    backend: str | None = None
    provider: str | None = None
    from_format: str
    to_format: str
    lossless: bool = False
    description: str | None = None


class ArtifactConversionPlanOut(_ResponseBase):
    artifact_id: str
    source_format: str | None = None
    target_format: str
    conversion_required: bool
    executable: bool
    reason: str | None = None
    steps: list[ArtifactConversionStepOut] = Field(default_factory=list)


class ArtifactConversionPlanRequest(_Base):
    provider: str | None = None
    to_format: str | None = None
    accepted_formats: list[str] = Field(default_factory=list)
    require_lossless: bool = False

    @model_validator(mode="after")
    def _target_is_present(self) -> ArtifactConversionPlanRequest:
        if "accepted_formats" in self.model_fields_set and not self.accepted_formats:
            raise ValueError("to_format or non-empty accepted_formats is required")
        if not self.to_format and not self.accepted_formats:
            raise ValueError("to_format or non-empty accepted_formats is required")
        return self


class ArtifactConvertRequest(ArtifactConversionPlanRequest):
    name: str | None = None
    to_kind: str | None = None
    options: dict[str, Any] = Field(default_factory=dict)


class ArtifactFileRef(_ResponseBase):
    name: str
    uri: str
    media_type: str | None = None
    sha256: str | None = None
    byte_size: int | None = None


class ArtifactImportRequest(_Base):
    project_id: str
    recon_id: str | None = None
    dataset_id: str | None = None
    kind: str
    name: str | None = None
    uri: str | None = None
    media_type: str | None = None
    artifact_format: str | None = None
    datatype: str | None = None
    schema_version: int | None = None
    files: list[ArtifactFileRef] = Field(default_factory=list)
    sha256: str | None = None
    byte_size: int | None = None
    coordinate_frame: str | None = None
    producer: dict[str, Any] | None = None
    summary: dict[str, Any] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("files", mode="before")
    @classmethod
    def _files_are_typed_refs(cls, value: Any) -> Any:
        if value is None:
            return []
        if isinstance(value, list) and any(isinstance(item, dict) for item in value):
            raise ValueError("files must contain ArtifactFileRef instances")
        return value


class ArtifactValidationIssueOut(_ResponseBase):
    level: str
    field: str | None = None
    message: str


class ArtifactValidationOut(_ResponseBase):
    artifact_id: str
    valid: bool
    artifact_format: str | None = None
    datatype: str | None = None
    checked_content: bool = False
    issues: list[ArtifactValidationIssueOut] = Field(default_factory=list)


class StageArtifact(_ResponseBase):
    artifact_id: str
    job_id: str
    task_id: str
    recon_id: str | None = None
    dataset_id: str | None = None
    kind: str
    name: str | None = None
    uri: str | None = None
    media_type: str | None = None
    artifact_format: str | None = None
    datatype: str | None = None
    schema_version: int | None = None
    files: list[ArtifactFileRef] = Field(default_factory=list)
    sha256: str | None = None
    byte_size: int | None = None
    coordinate_frame: str | None = None
    producer: dict[str, Any] | None = None
    summary: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime
    links: dict[str, Link | None] | None = Field(default=None, alias="_links")


class FeaturesSpec(_Base):
    version: Literal[1] = 1
    type: FeatureType = "sift"
    provider: str | None = None
    max_num_features: int = 8192
    use_gpu: bool = True
    seed: int = 0
    backend_options: dict[str, Any] = Field(default_factory=dict)
    input_artifacts: ArtifactInputMap = Field(default_factory=dict)


class ImagePairRef(_Base):
    image_name1: str
    image_name2: str


class PairsSpec(_Base):
    """New-style pair-selection spec; pair with :class:`MatcherSpec`."""

    version: Literal[1] = 1
    strategy: PairStrategy = "exhaustive"
    provider: str | None = None
    overlap: int = 10
    vocab_tree_path: str | None = None
    retrieval_strategy: Literal["dhash", "vlad", "netvlad"] = "vlad"
    retrieval_k: int = 20
    overlap_distance_m: float | None = None
    max_angle_deg: float | None = None
    image_pairs: list[ImagePairRef] | None = None
    pairs_blob_sha: str | None = None
    pairs_blob_format: Literal["image_name_pairs_txt"] = "image_name_pairs_txt"
    backend_options: dict[str, Any] = Field(default_factory=dict)
    input_artifacts: ArtifactInputMap = Field(default_factory=dict)


class MatcherSpec(_Base):
    """Per-pair matcher; pair with :class:`PairsSpec`."""

    version: Literal[1] = 1
    type: MatcherType = "nn-mutual"
    provider: str | None = None
    use_gpu: bool = True
    cross_check: bool = True
    max_ratio: float = 0.8
    max_distance: float = 0.7
    backend_options: dict[str, Any] = Field(default_factory=dict)
    input_artifacts: ArtifactInputMap = Field(default_factory=dict)


class VerifySpec(_Base):
    version: Literal[1] = 1
    provider: str | None = None
    use_gpu: bool = True
    min_inlier_ratio: float = 0.25
    backend_options: dict[str, Any] = Field(default_factory=dict)
    input_artifacts: ArtifactInputMap = Field(default_factory=dict)


class BundleAdjustmentSpec(_Base):
    version: Literal[1] = 1
    mode: Literal["standard", "two_stage", "featuremetric", "rig"] = "standard"
    provider: str | None = None
    refine_focal_length: bool = True
    refine_principal_point: bool = False
    refine_extra_params: bool = True
    max_num_iterations: int = 100
    loss_kernel: Literal["squared", "huber", "cauchy", "soft_l1", "tukey"] = "squared"
    loss_threshold: float = 1.0
    backend_options: dict[str, Any] = Field(default_factory=dict)


class _PipelineSpecBase(_Base):
    version: Literal[1] = 1
    provider: str | None = None
    seed: int = 0
    max_runtime_seconds: int | None = None
    snapshot_frames_freq: int | None = 50
    backend_options: dict[str, Any] = Field(default_factory=dict)
    input_artifacts: ArtifactInputMap = Field(default_factory=dict)


class IncrementalSpec(_PipelineSpecBase):
    kind: Literal["incremental"] = "incremental"
    init_image_pair: tuple[str, str] | None = None
    multiple_models: bool = True
    max_num_models: int = 50
    min_num_matches: int = 15
    ba_global_use_pba: bool = True
    extract_colors: bool = True


class GlobalSpec(_PipelineSpecBase):
    kind: Literal["global"] = "global"
    backend: Literal["AUTO", "BAXX", "CERES"] = "AUTO"
    formulation: Literal["AUTO", "EXPLICIT_SCALE", "ELIMINATED_SCALE"] = "AUTO"
    use_incremental_quality_fallback: bool = True


class HierarchicalSpec(_PipelineSpecBase):
    kind: Literal["hierarchical"] = "hierarchical"
    cluster_max_size: int = 100
    cluster_overlap: int = 25


class SphericalSpec(_PipelineSpecBase):
    kind: Literal["spherical"] = "spherical"
    panorama: bool = True


PipelineSpec = Annotated[
    IncrementalSpec | GlobalSpec | HierarchicalSpec | SphericalSpec,
    Field(discriminator="kind"),
]


class AttributeOut(_ResponseBase):
    name: str
    type: str
    required: bool
    description: str
    default: Any | None = None
    enum: list[str] | None = None
    min: float | None = None
    max: float | None = None


class DataTypeOut(_ResponseBase):
    type_id: str
    title: str
    kind: str
    aliases: list[str]
    description: str


class PortSpecOut(_ResponseBase):
    datatype: str
    required: bool
    multiple: bool
    description: str


class ProcessorOut(_ResponseBase):
    processor_id: str
    title: str
    consumer: dict[str, PortSpecOut]
    supplier: dict[str, PortSpecOut]
    attributes: list[AttributeOut]
    special_inputs: dict[str, PortSpecOut]
    special_attributes: list[AttributeOut]
    capabilities: list[str]
    config_stage: str | None
    aliases: list[str]
    description: str


class OperationOut(_ResponseBase):
    op_id: str
    title: str
    consumes: list[str]
    produces: list[str]
    capabilities: list[str]
    config_stage: str | None
    description: str


class PipelineStep(_Base):
    op: str
    provider: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)


class ProcessorPipelineStep(_Base):
    processor: str
    ref: str | None = None
    provider: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    params: dict[str, Any] = Field(default_factory=dict)
    wires: dict[str, str | list[str]] = Field(default_factory=dict)


class PipelineDefinitionStepOut(_ResponseBase):
    ref: str
    processor: str
    attributes: dict[str, Any]
    wires: dict[str, str | list[str]]


class PipelineDefinitionOut(_ResponseBase):
    pipeline_id: str
    title: str
    aliases: list[str]
    initial_inputs: list[str]
    steps: list[PipelineDefinitionStepOut]
    description: str


class AttributesContractOut(_ResponseBase):
    contract: str
    contract_schema_version: int
    attribute_types: list[str]
    rules: dict[str, str]


class DataTypesContractOut(_ResponseBase):
    contract: str
    contract_schema_version: int
    kinds: list[str]
    types: list[DataTypeOut]


class OperationsContractOut(_ResponseBase):
    contract: str
    contract_schema_version: int
    operations: list[OperationOut]
    compatibility: dict[str, str]


class ProcessorsContractOut(_ResponseBase):
    contract: str
    contract_schema_version: int
    processors: list[ProcessorOut]
    rules: dict[str, str]


class PipelinesContractOut(_ResponseBase):
    contract: str
    contract_schema_version: int
    composition_rule: str
    initial_inputs: list[str]
    canonical_pipelines: dict[str, list[str]]
    plugin_pipelines: list[PipelineDefinitionOut]
    step_schema: dict[str, Any]
    validation_reasons: list[str]


PipelineStepLike = str | ProcessorPipelineStep | PipelineStep


class PipelineValidateRequest(_Base):
    initial_inputs: list[str] = Field(default_factory=lambda: ["image_sequence"])
    steps: list[PipelineStepLike]


class PipelineRunRequest(PipelineValidateRequest):
    dataset_id: str


class ChainError(_ResponseBase):
    where: str
    message: str
    reason: str | None = None
    path: str | None = None


class PipelineValidateResponse(_ResponseBase):
    valid: bool
    errors: list[ChainError] = Field(default_factory=list)


# -- Async-context responses for high-level helpers --------------------------


class JobSubmitResponse(_ResponseBase):
    job_id: str
    task_ids: list[str]
    recon_id: str | None = None
    dataset_id: str | None = None
    project_id: str | None = None
    method: str | None = None
    applied_sim3: Sim3 | None = None
    target_recon_id: str | None = None
    source_recon_ids: list[str] | None = None
    strategy: str | None = None
    action_id: str | None = None
    backend: str | None = None
    provider: str | None = None
    artifact_id: str | None = None
    target_format: str | None = None
    radiance_field_id: str | None = None
    radiance_evaluation_id: str | None = None


class HealthResponse(_ResponseBase):
    status: str = "ok"


class BackendVersion(_ResponseBase):
    name: str
    version: str
    vendor: str | None = None
    runtime_versions: dict[str, str] = Field(default_factory=dict)


class VersionResponse(_ResponseBase):
    sfmapi: str
    backend: BackendVersion | None = None


# -- Capabilities (mirror of app/core/capabilities.py) ---------------------


class BackendInfo(_ResponseBase):
    name: str
    version: str
    vendor: str = ""


CAPABILITIES_SCHEMA_VERSION = 1


class Capabilities(_ResponseBase):
    """Wire shape of the ``GET /v1/capabilities`` response.

    ``schema_version`` tracks the envelope shape (top-level keys, field
    types) — independent of the feature flags themselves, which are
    negotiated via the ``features`` dict.
    """

    schema_version: int = CAPABILITIES_SCHEMA_VERSION
    backend: BackendInfo
    features: dict[str, bool] = Field(default_factory=dict)

    def supports(self, capability: str) -> bool:
        return bool(self.features.get(capability, False))


# -- Scene wire types (mirror of app/schemas/api/scene.py) -----------------


class Rotation(_Base):
    """Hamilton quaternion stored ``(w, x, y, z)``."""

    w: float
    x: float
    y: float
    z: float


class Rigid3(_Base):
    rotation: Rotation
    translation: tuple[float, float, float]


class Sim3(_Base):
    rotation: Rotation
    translation: tuple[float, float, float]
    scale: float


class GpsCoord(_Base):
    lat: float
    lng: float
    alt: float | None = None
    horiz_accuracy_m: float | None = None
    vert_accuracy_m: float | None = None


class ImuMeasurement(_Base):
    timestamp_ns: int
    gyro: tuple[float, float, float]
    accel: tuple[float, float, float]


class PosePrior(_Base):
    cam_from_world: Rigid3
    covariance: list[float] | None = Field(default=None, min_length=36, max_length=36)
    gps: GpsCoord | None = None
    timestamp_ns: int | None = None
    imu: ImuMeasurement | None = None


SPHERICAL_CAMERA_MODEL = "SPHERICAL"


class Camera(_Base):
    camera_id: int
    model: str
    width: int
    height: int
    params: list[float]
    has_prior_focal_length: bool = False

    def is_spherical(self) -> bool:
        return self.model == SPHERICAL_CAMERA_MODEL


class Point2D(_Base):
    xy: tuple[float, float]
    point3d_id: int | None = None


class ImagePose(_Base):
    image_id: int
    name: str
    camera_id: int
    cam_from_world: Rigid3
    points2D: list[Point2D] = Field(default_factory=list)


class TrackElement(_Base):
    image_id: int
    point2d_idx: int


class Track(_Base):
    point3d_id: int
    elements: list[TrackElement] = Field(default_factory=list)


class Rig(_Base):
    rig_id: int
    ref_sensor_id: int
    sensor_from_rig: dict[str, Rigid3]


class Frame(_Base):
    frame_id: int
    rig_id: int
    rig_from_world: Rigid3
    data_ids: dict[str, int] = Field(default_factory=dict)


TwoViewGeometryType = Literal[
    "undefined",
    "degenerate",
    "calibrated",
    "uncalibrated",
    "planar",
    "panoramic",
    "planar_or_panoramic",
    "watermark",
    "multiple",
]


class TwoViewGeometry(_Base):
    image_id1: int
    image_id2: int
    type: TwoViewGeometryType
    num_inliers: int
    F: list[float] | None = Field(default=None, min_length=9, max_length=9)
    E: list[float] | None = Field(default=None, min_length=9, max_length=9)
    H: list[float] | None = Field(default=None, min_length=9, max_length=9)
    inlier_matches: list[tuple[int, int]] = Field(default_factory=list)


class CorrespondencePair(_Base):
    image_id1: int
    image_id2: int
    num_matches: int
    matches: list[tuple[int, int]] = Field(default_factory=list)


class PoseGraphEdge(_Base):
    image_id1: int
    image_id2: int
    cam2_from_cam1: Rigid3
    weight: float = 1.0


class PoseGraph(_Base):
    nodes: list[ImagePose] = Field(default_factory=list)
    edges: list[PoseGraphEdge] = Field(default_factory=list)


class CamerasFile(_Base):
    cameras: list[Camera] = Field(default_factory=list)


class ImagesFile(_Base):
    images: list[ImagePose] = Field(default_factory=list)


class RigsFile(_Base):
    rigs: list[Rig] = Field(default_factory=list)


class FramesFile(_Base):
    frames: list[Frame] = Field(default_factory=list)


class TwoViewGeometriesFile(_Base):
    pairs: list[TwoViewGeometry] = Field(default_factory=list)


class CorrespondenceGraphFile(_Base):
    pairs: list[CorrespondencePair] = Field(default_factory=list)


class PoseGraphFile(_Base):
    pose_graph: PoseGraph


class LocalizationResult(_ResponseBase):
    success: bool
    cam_from_world: Rigid3 | None = None
    num_inliers: int = 0
    inlier_matches: list[tuple[int, int]] = Field(default_factory=list)
    diagnostics: dict[str, Any] = Field(default_factory=dict)


class DepthMapInfo(_ResponseBase):
    image_id: int
    image_name: str
    width: int
    height: int
    depth_min: float
    depth_max: float
    has_normal_map: bool = False


class DenseSummary(_ResponseBase):
    num_images: int
    num_depth_maps: int
    num_normal_maps: int
    fused_points: int
    bbox_min: tuple[float, float, float] | None = None
    bbox_max: tuple[float, float, float] | None = None


class DenseManifestFile(_ResponseBase):
    summary: DenseSummary
    depth_maps: list[DepthMapInfo] = Field(default_factory=list)


MeshMethod = Literal["poisson", "delaunay"]


class MeshSummary(_ResponseBase):
    method: MeshMethod
    num_vertices: int
    num_faces: int
    has_vertex_colors: bool = False
    has_vertex_normals: bool = False
    bbox_min: tuple[float, float, float] | None = None
    bbox_max: tuple[float, float, float] | None = None


class MeshFile(_ResponseBase):
    summary: MeshSummary
    mesh_url: str | None = None
