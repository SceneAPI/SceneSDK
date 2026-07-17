"""Contains all the data models used in inputs/outputs"""

from .api_key_out import ApiKeyOut
from .archive_import_request import ArchiveImportRequest
from .artifact_conversion_out import ArtifactConversionOut
from .artifact_conversion_plan_out import ArtifactConversionPlanOut
from .artifact_conversion_plan_request import ArtifactConversionPlanRequest
from .artifact_conversion_step_out import ArtifactConversionStepOut
from .artifact_convert_request import ArtifactConvertRequest
from .artifact_convert_request_options import ArtifactConvertRequestOptions
from .artifact_file_ref import ArtifactFileRef
from .artifact_format_out import ArtifactFormatOut
from .artifact_format_out_examples_item import ArtifactFormatOutExamplesItem
from .artifact_format_out_json_schema_type_0 import ArtifactFormatOutJsonSchemaType0
from .artifact_import_request import ArtifactImportRequest
from .artifact_import_request_metadata import ArtifactImportRequestMetadata
from .artifact_import_request_producer_type_0 import ArtifactImportRequestProducerType0
from .artifact_import_request_summary_type_0 import ArtifactImportRequestSummaryType0
from .artifact_kind_out import ArtifactKindOut
from .artifact_ref import ArtifactRef
from .artifact_validation_issue_out import ArtifactValidationIssueOut
from .artifact_validation_out import ArtifactValidationOut
from .backend_action_out import BackendActionOut
from .backend_action_out_input_schema_type_0 import BackendActionOutInputSchemaType0
from .backend_action_out_links_type_0 import BackendActionOutLinksType0
from .backend_action_out_metadata import BackendActionOutMetadata
from .backend_action_out_output_schema_type_0 import BackendActionOutOutputSchemaType0
from .backend_action_out_side_effects import BackendActionOutSideEffects
from .backend_action_out_stability import BackendActionOutStability
from .backend_action_run_request import BackendActionRunRequest
from .backend_action_run_request_inputs import BackendActionRunRequestInputs
from .backend_action_validate_request import BackendActionValidateRequest
from .backend_action_validate_request_inputs import BackendActionValidateRequestInputs
from .backend_action_validate_response import BackendActionValidateResponse
from .backend_action_validate_response_normalized_inputs import (
    BackendActionValidateResponseNormalizedInputs,
)
from .backend_action_validation_error_out import BackendActionValidationErrorOut
from .backend_artifact_contract_out import BackendArtifactContractOut
from .backend_artifact_contract_out_links_type_0 import (
    BackendArtifactContractOutLinksType0,
)
from .backend_artifact_contract_out_metadata import BackendArtifactContractOutMetadata
from .backend_config_schema_out import BackendConfigSchemaOut
from .backend_config_schema_out_defaults import BackendConfigSchemaOutDefaults
from .backend_config_schema_out_links_type_0 import BackendConfigSchemaOutLinksType0
from .backend_config_schema_out_metadata import BackendConfigSchemaOutMetadata
from .backend_config_schema_out_option_schema_type_0 import (
    BackendConfigSchemaOutOptionSchemaType0,
)
from .backend_info_out import BackendInfoOut
from .backend_out import BackendOut
from .backend_out_links_type_0 import BackendOutLinksType0
from .backend_out_runtime_versions import BackendOutRuntimeVersions
from .backend_version import BackendVersion
from .backend_version_runtime_versions import BackendVersionRuntimeVersions
from .batch_create_images_request import BatchCreateImagesRequest
from .batch_create_images_response import BatchCreateImagesResponse
from .bulk_set_pose_priors_v1_datasets_dataset_id_pose_priors_put_body import (
    BulkSetPosePriorsV1DatasetsDatasetIdPosePriorsPutBody,
)
from .bundle_adjustment_spec import BundleAdjustmentSpec
from .bundle_adjustment_spec_backend_options import BundleAdjustmentSpecBackendOptions
from .bundle_adjustment_spec_loss_kernel import BundleAdjustmentSpecLossKernel
from .bundle_adjustment_spec_mode import BundleAdjustmentSpecMode
from .camera_model_out import CameraModelOut
from .camera_model_out_distortion import CameraModelOutDistortion
from .camera_model_out_projection import CameraModelOutProjection
from .capabilities_out import CapabilitiesOut
from .capabilities_out_features import CapabilitiesOutFeatures
from .compatibility import Compatibility
from .compatibility_tool_versions import CompatibilityToolVersions
from .conformance import Conformance
from .conformance_status import ConformanceStatus
from .container_service_build import ContainerServiceBuild
from .container_service_build_args import ContainerServiceBuildArgs
from .container_service_build_source import ContainerServiceBuildSource
from .container_service_cache import ContainerServiceCache
from .container_service_cache_policy import ContainerServiceCachePolicy
from .container_service_cache_scope import ContainerServiceCacheScope
from .container_service_endpoint import ContainerServiceEndpoint
from .container_service_execution import ContainerServiceExecution
from .container_service_execution_gpu import ContainerServiceExecutionGpu
from .container_service_execution_log_collection import (
    ContainerServiceExecutionLogCollection,
)
from .container_service_healthcheck import ContainerServiceHealthcheck
from .container_service_image import ContainerServiceImage
from .container_service_mounts import ContainerServiceMounts
from .container_service_object_store import ContainerServiceObjectStore
from .container_service_provenance import ContainerServiceProvenance
from .container_service_retry import ContainerServiceRetry
from .container_service_runtime import ContainerServiceRuntime
from .cubemap_projection_request import CubemapProjectionRequest
from .cubemap_projection_spec import CubemapProjectionSpec
from .cubemap_projection_spec_face_order_item import CubemapProjectionSpecFaceOrderItem
from .dataset_create import DatasetCreate
from .dataset_create_intrinsics_mode import DatasetCreateIntrinsicsMode
from .dataset_create_rig_config_type_0 import DatasetCreateRigConfigType0
from .dataset_out import DatasetOut
from .dataset_out_links_type_0 import DatasetOutLinksType0
from .dataset_out_rig_config_json_type_0 import DatasetOutRigConfigJsonType0
from .dataset_patch import DatasetPatch
from .dataset_patch_intrinsics_mode_type_0 import DatasetPatchIntrinsicsModeType0
from .dataset_patch_rig_config_type_0 import DatasetPatchRigConfigType0
from .docker_runtime import DockerRuntime
from .doctor_check import DoctorCheck
from .doctor_check_metadata import DoctorCheckMetadata
from .doctor_check_status import DoctorCheckStatus
from .equirectangular_projection_request import EquirectangularProjectionRequest
from .equirectangular_projection_spec import EquirectangularProjectionSpec
from .export_spec import ExportSpec
from .export_spec_backend_options import ExportSpecBackendOptions
from .export_spec_format import ExportSpecFormat
from .external_tool_runtime import ExternalToolRuntime
from .features_request import FeaturesRequest
from .features_spec import FeaturesSpec
from .features_spec_backend_options import FeaturesSpecBackendOptions
from .features_spec_input_artifacts import FeaturesSpecInputArtifacts
from .features_spec_type import FeaturesSpecType
from .georegister_request import GeoregisterRequest
from .georegister_request_backend_options import GeoregisterRequestBackendOptions
from .georegister_request_mode import GeoregisterRequestMode
from .global_spec import GlobalSpec
from .global_spec_backend import GlobalSpecBackend
from .global_spec_backend_options import GlobalSpecBackendOptions
from .global_spec_formulation import GlobalSpecFormulation
from .global_spec_input_artifacts import GlobalSpecInputArtifacts
from .gps_coord import GpsCoord
from .health_response import HealthResponse
from .hierarchical_spec import HierarchicalSpec
from .hierarchical_spec_backend_options import HierarchicalSpecBackendOptions
from .hierarchical_spec_input_artifacts import HierarchicalSpecInputArtifacts
from .http_validation_error import HTTPValidationError
from .image_create import ImageCreate
from .image_create_exif_type_0 import ImageCreateExifType0
from .image_exif_response import ImageExifResponse
from .image_exif_response_exif import ImageExifResponseExif
from .image_observation_row import ImageObservationRow
from .image_observations_response import ImageObservationsResponse
from .image_out import ImageOut
from .image_out_links_type_0 import ImageOutLinksType0
from .image_pair_ref import ImagePairRef
from .imu_measurement import ImuMeasurement
from .incremental_spec import IncrementalSpec
from .incremental_spec_backend_options import IncrementalSpecBackendOptions
from .incremental_spec_input_artifacts import IncrementalSpecInputArtifacts
from .issue_key_body import IssueKeyBody
from .issue_key_response import IssueKeyResponse
from .job_accepted_response import JobAcceptedResponse
from .job_detail import JobDetail
from .job_detail_links_type_0 import JobDetailLinksType0
from .job_detail_status import JobDetailStatus
from .job_out import JobOut
from .job_out_links_type_0 import JobOutLinksType0
from .job_out_status import JobOutStatus
from .job_progress_out import JobProgressOut
from .job_progress_out_latest_event_type_0 import JobProgressOutLatestEventType0
from .job_progress_out_status import JobProgressOutStatus
from .job_progress_out_task_counts import JobProgressOutTaskCounts
from .kapture_import_request import KaptureImportRequest
from .license_info import LicenseInfo
from .link import Link
from .list_v1_jobs_get_status_type_0 import ListV1JobsGetStatusType0
from .local_source_spec import LocalSourceSpec
from .localization_request import LocalizationRequest
from .localization_request_sift_type_0 import LocalizationRequestSiftType0
from .matcher_spec import MatcherSpec
from .matcher_spec_backend_options import MatcherSpecBackendOptions
from .matcher_spec_input_artifacts import MatcherSpecInputArtifacts
from .matcher_spec_type import MatcherSpecType
from .matches_request import MatchesRequest
from .matches_request_input_artifacts import MatchesRequestInputArtifacts
from .merge_request import MergeRequest
from .merge_request_sim_3_aligners_type_0_item import MergeRequestSim3AlignersType0Item
from .one_shot_features_payload import OneShotFeaturesPayload
from .one_shot_features_response import OneShotFeaturesResponse
from .one_shot_features_response_spec import OneShotFeaturesResponseSpec
from .one_shot_image_info import OneShotImageInfo
from .one_shot_localize_response import OneShotLocalizeResponse
from .one_shot_localize_response_result import OneShotLocalizeResponseResult
from .one_shot_localize_response_spec import OneShotLocalizeResponseSpec
from .one_shot_runtime_info import OneShotRuntimeInfo
from .oneshot_features_v1_oneshot_features_post_type import (
    OneshotFeaturesV1OneshotFeaturesPostType,
)
from .oneshot_localize_v1_oneshot_localize_post_type import (
    OneshotLocalizeV1OneshotLocalizePostType,
)
from .page_artifact_format_out import PageArtifactFormatOut
from .page_artifact_kind_out import PageArtifactKindOut
from .page_backend_action_out import PageBackendActionOut
from .page_backend_artifact_contract_out import PageBackendArtifactContractOut
from .page_backend_config_schema_out import PageBackendConfigSchemaOut
from .page_camera_model_out import PageCameraModelOut
from .page_dataset_out import PageDatasetOut
from .page_image_out import PageImageOut
from .page_job_out import PageJobOut
from .page_plugin_entry_point_out import PagePluginEntryPointOut
from .page_plugin_registry_item_out import PagePluginRegistryItemOut
from .page_project_out import PageProjectOut
from .page_provider_out import PageProviderOut
from .page_radiance_evaluation_out import PageRadianceEvaluationOut
from .page_radiance_field_out import PageRadianceFieldOut
from .page_stage_artifact_out import PageStageArtifactOut
from .page_sub_model_out import PageSubModelOut
from .pairs_spec import PairsSpec
from .pairs_spec_backend_options import PairsSpecBackendOptions
from .pairs_spec_input_artifacts import PairsSpecInputArtifacts
from .pairs_spec_retrieval_strategy import PairsSpecRetrievalStrategy
from .pairs_spec_strategy import PairsSpecStrategy
from .perspective_projection_request import PerspectiveProjectionRequest
from .perspective_projection_spec import PerspectiveProjectionSpec
from .perspective_view_spec import PerspectiveViewSpec
from .pipeline_request import PipelineRequest
from .pipeline_request_input_artifacts import PipelineRequestInputArtifacts
from .pipeline_run_request import PipelineRunRequest
from .pipeline_step import PipelineStep
from .pipeline_step_params import PipelineStepParams
from .legacy_operation_step import LegacyOperationStep
from .legacy_operation_step_params import LegacyOperationStepParams
from .plugin_attribute_manifest import PluginAttributeManifest
from .plugin_attribute_manifest_type import PluginAttributeManifestType
from .plugin_data_type_manifest import PluginDataTypeManifest
from .plugin_data_type_manifest_kind import PluginDataTypeManifestKind
from .plugin_dependency_manifest import PluginDependencyManifest
from .plugin_detail_out import PluginDetailOut
from .plugin_detail_out_links_type_0 import PluginDetailOutLinksType0
from .plugin_doctor_out import PluginDoctorOut
from .plugin_doctor_out_status import PluginDoctorOutStatus
from .plugin_entry_point_out import PluginEntryPointOut
from .plugin_install_request import PluginInstallRequest
from .plugin_install_request_method import PluginInstallRequestMethod
from .plugin_install_response import PluginInstallResponse
from .plugin_install_response_method import PluginInstallResponseMethod
from .plugin_manifest import PluginManifest
from .plugin_manifest_trust_tier import PluginManifestTrustTier
from .plugin_pipeline_manifest import PluginPipelineManifest
from .plugin_pipeline_step_manifest import PluginPipelineStepManifest
from .plugin_pipeline_step_manifest_attributes import (
    PluginPipelineStepManifestAttributes,
)
from .plugin_pipeline_step_manifest_wires import PluginPipelineStepManifestWires
from .plugin_port_spec_manifest import PluginPortSpecManifest
from .plugin_processor_extension_manifest import PluginProcessorExtensionManifest
from .plugin_processor_extension_manifest_special_inputs import (
    PluginProcessorExtensionManifestSpecialInputs,
)
from .plugin_processor_manifest import PluginProcessorManifest
from .plugin_processor_manifest_consumer import PluginProcessorManifestConsumer
from .plugin_processor_manifest_supplier import PluginProcessorManifestSupplier
from .plugin_provision_step_out import PluginProvisionStepOut
from .plugin_provisioning_out import PluginProvisioningOut
from .plugin_provisioning_out_metadata import PluginProvisioningOutMetadata
from .plugin_provisioning_out_outputs import PluginProvisioningOutOutputs
from .plugin_provisioning_out_redacted_env import PluginProvisioningOutRedactedEnv
from .plugin_registry_item_out import PluginRegistryItemOut
from .plugin_registry_item_out_links_type_0 import PluginRegistryItemOutLinksType0
from .plugin_special_attribute_manifest import PluginSpecialAttributeManifest
from .plugin_special_attribute_manifest_type import PluginSpecialAttributeManifestType
from .plugin_special_input_port_spec_manifest import PluginSpecialInputPortSpecManifest
from .point_observation_row import PointObservationRow
from .point_visibility_response import PointVisibilityResponse
from .pose_graph_spec import PoseGraphSpec
from .pose_graph_spec_backend_options import PoseGraphSpecBackendOptions
from .pose_prior import PosePrior
from .pose_priors_bulk_response import PosePriorsBulkResponse
from .pose_priors_bulk_response_pose_priors import PosePriorsBulkResponsePosePriors
from .pose_priors_bulk_write_response import PosePriorsBulkWriteResponse
from .problem_error import ProblemError
from .problem_error_ctx_type_0 import ProblemErrorCtxType0
from .problem_response import ProblemResponse
from .processor_pipeline_step import ProcessorPipelineStep
from .processor_pipeline_step_attributes import ProcessorPipelineStepAttributes
from .processor_pipeline_step_params import ProcessorPipelineStepParams
from .processor_pipeline_step_wires import ProcessorPipelineStepWires
from .project_create import ProjectCreate
from .project_out import ProjectOut
from .project_out_links_type_0 import ProjectOutLinksType0
from .project_patch import ProjectPatch
from .projection_job_request import ProjectionJobRequest
from .projection_job_request_operation import ProjectionJobRequestOperation
from .projection_output_options import ProjectionOutputOptions
from .projection_output_options_format import ProjectionOutputOptionsFormat
from .projection_sampling import ProjectionSampling
from .projection_sampling_interpolation import ProjectionSamplingInterpolation
from .provider_manifest import ProviderManifest
from .provider_out import ProviderOut
from .provider_out_links_type_0 import ProviderOutLinksType0
from .radiance_eval_config import RadianceEvalConfig
from .radiance_eval_config_background import RadianceEvalConfigBackground
from .radiance_eval_config_lpips_net import RadianceEvalConfigLpipsNet
from .radiance_eval_config_metrics_item import RadianceEvalConfigMetricsItem
from .radiance_eval_config_split import RadianceEvalConfigSplit
from .radiance_evaluate_request import RadianceEvaluateRequest
from .radiance_evaluate_request_backend_options import (
    RadianceEvaluateRequestBackendOptions,
)
from .radiance_evaluation_out import RadianceEvaluationOut
from .radiance_evaluation_out_artifacts_type_0_item import (
    RadianceEvaluationOutArtifactsType0Item,
)
from .radiance_evaluation_out_config import RadianceEvaluationOutConfig
from .radiance_evaluation_out_error_type_0 import RadianceEvaluationOutErrorType0
from .radiance_evaluation_out_links_type_0 import RadianceEvaluationOutLinksType0
from .radiance_evaluation_out_status import RadianceEvaluationOutStatus
from .radiance_field_out import RadianceFieldOut
from .radiance_field_out_links_type_0 import RadianceFieldOutLinksType0
from .radiance_field_out_spec import RadianceFieldOutSpec
from .radiance_field_out_status import RadianceFieldOutStatus
from .radiance_field_out_summary_type_0 import RadianceFieldOutSummaryType0
from .radiance_metrics import RadianceMetrics
from .radiance_snapshot_list_response import RadianceSnapshotListResponse
from .radiance_snapshot_list_response_links_type_0 import (
    RadianceSnapshotListResponseLinksType0,
)
from .radiance_snapshot_out import RadianceSnapshotOut
from .radiance_snapshot_out_links_type_0 import RadianceSnapshotOutLinksType0
from .radiance_snapshot_out_summary_type_0 import RadianceSnapshotOutSummaryType0
from .radiance_train_request import RadianceTrainRequest
from .radiance_train_request_backend_options import RadianceTrainRequestBackendOptions
from .read_correspondence_graph_v1_reconstructions_recon_id_correspondence_graph_json_get_response_200 import (
    ReadCorrespondenceGraphV1ReconstructionsReconIdCorrespondenceGraphJsonGetResponse200,
)
from .read_two_view_geometries_v1_reconstructions_recon_id_two_view_geometries_json_get_response_200 import (
    ReadTwoViewGeometriesV1ReconstructionsReconIdTwoViewGeometriesJsonGetResponse200,
)
from .readyz_response import ReadyzResponse
from .readyz_response_checks import ReadyzResponseChecks
from .reconstruction_out import ReconstructionOut
from .reconstruction_out_links_type_0 import ReconstructionOutLinksType0
from .reconstruction_out_status import ReconstructionOutStatus
from .relocalize_spec import RelocalizeSpec
from .relocalize_spec_backend_options import RelocalizeSpecBackendOptions
from .rig_config_spec import RigConfigSpec
from .rig_config_spec_backend_options import RigConfigSpecBackendOptions
from .rig_config_spec_rig_config import RigConfigSpecRigConfig
from .rigid_3 import Rigid3
from .rotation import Rotation
from .routing_out import RoutingOut
from .routing_out_profiles import RoutingOutProfiles
from .routing_out_project_profiles import RoutingOutProjectProfiles
from .routing_out_workspace_profiles import RoutingOutWorkspaceProfiles
from .routing_profile import RoutingProfile
from .routing_profile_routes import RoutingProfileRoutes
from .run_recipe_v1_projects_project_id_pipelines_recipe_post_recipe import (
    RunRecipeV1ProjectsProjectIdPipelinesRecipePostRecipe,
)
from .runtime_modes import RuntimeModes
from .s3_source_spec import S3SourceSpec
from .sim_3 import Sim3
from .snapshot_list_response import SnapshotListResponse
from .snapshot_list_response_links_type_0 import SnapshotListResponseLinksType0
from .spec_response import SpecResponse
from .spec_server_info import SpecServerInfo
from .spherical_spec import SphericalSpec
from .spherical_spec_backend_options import SphericalSpecBackendOptions
from .spherical_spec_input_artifacts import SphericalSpecInputArtifacts
from .stage_artifact_out import StageArtifactOut
from .stage_artifact_out_links_type_0 import StageArtifactOutLinksType0
from .stage_artifact_out_metadata_type_0 import StageArtifactOutMetadataType0
from .stage_artifact_out_producer_type_0 import StageArtifactOutProducerType0
from .stage_artifact_out_summary_type_0 import StageArtifactOutSummaryType0
from .sub_model_out import SubModelOut
from .sub_model_out_links_type_0 import SubModelOutLinksType0
from .sub_model_out_rigidity_type_0 import SubModelOutRigidityType0
from .sub_model_out_summary_type_0 import SubModelOutSummaryType0
from .task_out import TaskOut
from .task_out_outputs_ref_type_0 import TaskOutOutputsRefType0
from .task_out_status import TaskOutStatus
from .task_progress_out import TaskProgressOut
from .task_progress_out_status import TaskProgressOutStatus
from .tiles_index_v1_reconstructions_recon_id_snapshots_seq_tiles_index_json_get_response_200 import (
    TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200,
)
from .tool_detection import ToolDetection
from .tool_detection_out import ToolDetectionOut
from .tool_detection_out_tools import ToolDetectionOutTools
from .tool_detection_source import ToolDetectionSource
from .torch_runtime import TorchRuntime
from .torch_runtime_device import TorchRuntimeDevice
from .torch_runtime_install_env import TorchRuntimeInstallEnv
from .torch_runtime_policy import TorchRuntimePolicy
from .triangulate_spec import TriangulateSpec
from .triangulate_spec_backend_options import TriangulateSpecBackendOptions
from .two_view_spec import TwoViewSpec
from .two_view_spec_backend_options import TwoViewSpecBackendOptions
from .undistort_spec import UndistortSpec
from .undistort_spec_backend_options import UndistortSpecBackendOptions
from .upload_entry_spec import UploadEntrySpec
from .upload_finalize_request import UploadFinalizeRequest
from .upload_init import UploadInit
from .upload_out import UploadOut
from .upload_out_state import UploadOutState
from .upload_source_spec import UploadSourceSpec
from .upstream_project import UpstreamProject
from .uv_runtime import UvRuntime
from .validation_error import ValidationError
from .validation_error_context import ValidationErrorContext
from .verify_request import VerifyRequest
from .verify_request_input_artifacts import VerifyRequestInputArtifacts
from .verify_spec import VerifySpec
from .verify_spec_backend_options import VerifySpecBackendOptions
from .verify_spec_input_artifacts import VerifySpecInputArtifacts
from .version_response import VersionResponse
from .video_frames_request import VideoFramesRequest
from .vocab_tree_spec import VocabTreeSpec
from .vocab_tree_spec_backend_options import VocabTreeSpecBackendOptions

__all__ = (
    "ApiKeyOut",
    "ArchiveImportRequest",
    "ArtifactConversionOut",
    "ArtifactConversionPlanOut",
    "ArtifactConversionPlanRequest",
    "ArtifactConversionStepOut",
    "ArtifactConvertRequest",
    "ArtifactConvertRequestOptions",
    "ArtifactFileRef",
    "ArtifactFormatOut",
    "ArtifactFormatOutExamplesItem",
    "ArtifactFormatOutJsonSchemaType0",
    "ArtifactImportRequest",
    "ArtifactImportRequestMetadata",
    "ArtifactImportRequestProducerType0",
    "ArtifactImportRequestSummaryType0",
    "ArtifactKindOut",
    "ArtifactRef",
    "ArtifactValidationIssueOut",
    "ArtifactValidationOut",
    "BackendActionOut",
    "BackendActionOutInputSchemaType0",
    "BackendActionOutLinksType0",
    "BackendActionOutMetadata",
    "BackendActionOutOutputSchemaType0",
    "BackendActionOutSideEffects",
    "BackendActionOutStability",
    "BackendActionRunRequest",
    "BackendActionRunRequestInputs",
    "BackendActionValidateRequest",
    "BackendActionValidateRequestInputs",
    "BackendActionValidateResponse",
    "BackendActionValidateResponseNormalizedInputs",
    "BackendActionValidationErrorOut",
    "BackendArtifactContractOut",
    "BackendArtifactContractOutLinksType0",
    "BackendArtifactContractOutMetadata",
    "BackendConfigSchemaOut",
    "BackendConfigSchemaOutDefaults",
    "BackendConfigSchemaOutLinksType0",
    "BackendConfigSchemaOutMetadata",
    "BackendConfigSchemaOutOptionSchemaType0",
    "BackendInfoOut",
    "BackendOut",
    "BackendOutLinksType0",
    "BackendOutRuntimeVersions",
    "BackendVersion",
    "BackendVersionRuntimeVersions",
    "BatchCreateImagesRequest",
    "BatchCreateImagesResponse",
    "BulkSetPosePriorsV1DatasetsDatasetIdPosePriorsPutBody",
    "BundleAdjustmentSpec",
    "BundleAdjustmentSpecBackendOptions",
    "BundleAdjustmentSpecLossKernel",
    "BundleAdjustmentSpecMode",
    "CameraModelOut",
    "CameraModelOutDistortion",
    "CameraModelOutProjection",
    "CapabilitiesOut",
    "CapabilitiesOutFeatures",
    "Compatibility",
    "CompatibilityToolVersions",
    "Conformance",
    "ConformanceStatus",
    "ContainerServiceBuild",
    "ContainerServiceBuildArgs",
    "ContainerServiceBuildSource",
    "ContainerServiceCache",
    "ContainerServiceCachePolicy",
    "ContainerServiceCacheScope",
    "ContainerServiceEndpoint",
    "ContainerServiceExecution",
    "ContainerServiceExecutionGpu",
    "ContainerServiceExecutionLogCollection",
    "ContainerServiceHealthcheck",
    "ContainerServiceImage",
    "ContainerServiceMounts",
    "ContainerServiceObjectStore",
    "ContainerServiceProvenance",
    "ContainerServiceRetry",
    "ContainerServiceRuntime",
    "CubemapProjectionRequest",
    "CubemapProjectionSpec",
    "CubemapProjectionSpecFaceOrderItem",
    "DatasetCreate",
    "DatasetCreateIntrinsicsMode",
    "DatasetCreateRigConfigType0",
    "DatasetOut",
    "DatasetOutLinksType0",
    "DatasetOutRigConfigJsonType0",
    "DatasetPatch",
    "DatasetPatchIntrinsicsModeType0",
    "DatasetPatchRigConfigType0",
    "DockerRuntime",
    "DoctorCheck",
    "DoctorCheckMetadata",
    "DoctorCheckStatus",
    "EquirectangularProjectionRequest",
    "EquirectangularProjectionSpec",
    "ExportSpec",
    "ExportSpecBackendOptions",
    "ExportSpecFormat",
    "ExternalToolRuntime",
    "FeaturesRequest",
    "FeaturesSpec",
    "FeaturesSpecBackendOptions",
    "FeaturesSpecInputArtifacts",
    "FeaturesSpecType",
    "GeoregisterRequest",
    "GeoregisterRequestBackendOptions",
    "GeoregisterRequestMode",
    "GlobalSpec",
    "GlobalSpecBackend",
    "GlobalSpecBackendOptions",
    "GlobalSpecFormulation",
    "GlobalSpecInputArtifacts",
    "GpsCoord",
    "HealthResponse",
    "HierarchicalSpec",
    "HierarchicalSpecBackendOptions",
    "HierarchicalSpecInputArtifacts",
    "HTTPValidationError",
    "ImageCreate",
    "ImageCreateExifType0",
    "ImageExifResponse",
    "ImageExifResponseExif",
    "ImageObservationRow",
    "ImageObservationsResponse",
    "ImageOut",
    "ImageOutLinksType0",
    "ImagePairRef",
    "ImuMeasurement",
    "IncrementalSpec",
    "IncrementalSpecBackendOptions",
    "IncrementalSpecInputArtifacts",
    "IssueKeyBody",
    "IssueKeyResponse",
    "JobAcceptedResponse",
    "JobDetail",
    "JobDetailLinksType0",
    "JobDetailStatus",
    "JobOut",
    "JobOutLinksType0",
    "JobOutStatus",
    "JobProgressOut",
    "JobProgressOutLatestEventType0",
    "JobProgressOutStatus",
    "JobProgressOutTaskCounts",
    "KaptureImportRequest",
    "LicenseInfo",
    "Link",
    "ListV1JobsGetStatusType0",
    "LocalizationRequest",
    "LocalizationRequestSiftType0",
    "LocalSourceSpec",
    "MatcherSpec",
    "MatcherSpecBackendOptions",
    "MatcherSpecInputArtifacts",
    "MatcherSpecType",
    "MatchesRequest",
    "MatchesRequestInputArtifacts",
    "MergeRequest",
    "MergeRequestSim3AlignersType0Item",
    "OneShotFeaturesPayload",
    "OneShotFeaturesResponse",
    "OneShotFeaturesResponseSpec",
    "OneshotFeaturesV1OneshotFeaturesPostType",
    "OneShotImageInfo",
    "OneShotLocalizeResponse",
    "OneShotLocalizeResponseResult",
    "OneShotLocalizeResponseSpec",
    "OneshotLocalizeV1OneshotLocalizePostType",
    "OneShotRuntimeInfo",
    "PageArtifactFormatOut",
    "PageArtifactKindOut",
    "PageBackendActionOut",
    "PageBackendArtifactContractOut",
    "PageBackendConfigSchemaOut",
    "PageCameraModelOut",
    "PageDatasetOut",
    "PageImageOut",
    "PageJobOut",
    "PagePluginEntryPointOut",
    "PagePluginRegistryItemOut",
    "PageProjectOut",
    "PageProviderOut",
    "PageRadianceEvaluationOut",
    "PageRadianceFieldOut",
    "PageStageArtifactOut",
    "PageSubModelOut",
    "PairsSpec",
    "PairsSpecBackendOptions",
    "PairsSpecInputArtifacts",
    "PairsSpecRetrievalStrategy",
    "PairsSpecStrategy",
    "PerspectiveProjectionRequest",
    "PerspectiveProjectionSpec",
    "PerspectiveViewSpec",
    "PipelineRequest",
    "PipelineRequestInputArtifacts",
    "PipelineRunRequest",
    "PipelineStep",
    "PipelineStepParams",
    "LegacyOperationStep",
    "LegacyOperationStepParams",
    "PluginAttributeManifest",
    "PluginAttributeManifestType",
    "PluginDataTypeManifest",
    "PluginDataTypeManifestKind",
    "PluginDependencyManifest",
    "PluginDetailOut",
    "PluginDetailOutLinksType0",
    "PluginDoctorOut",
    "PluginDoctorOutStatus",
    "PluginEntryPointOut",
    "PluginInstallRequest",
    "PluginInstallRequestMethod",
    "PluginInstallResponse",
    "PluginInstallResponseMethod",
    "PluginManifest",
    "PluginManifestTrustTier",
    "PluginPipelineManifest",
    "PluginPipelineStepManifest",
    "PluginPipelineStepManifestAttributes",
    "PluginPipelineStepManifestWires",
    "PluginPortSpecManifest",
    "PluginProcessorExtensionManifest",
    "PluginProcessorExtensionManifestSpecialInputs",
    "PluginProcessorManifest",
    "PluginProcessorManifestConsumer",
    "PluginProcessorManifestSupplier",
    "PluginProvisioningOut",
    "PluginProvisioningOutMetadata",
    "PluginProvisioningOutOutputs",
    "PluginProvisioningOutRedactedEnv",
    "PluginProvisionStepOut",
    "PluginRegistryItemOut",
    "PluginRegistryItemOutLinksType0",
    "PluginSpecialAttributeManifest",
    "PluginSpecialAttributeManifestType",
    "PluginSpecialInputPortSpecManifest",
    "PointObservationRow",
    "PointVisibilityResponse",
    "PoseGraphSpec",
    "PoseGraphSpecBackendOptions",
    "PosePrior",
    "PosePriorsBulkResponse",
    "PosePriorsBulkResponsePosePriors",
    "PosePriorsBulkWriteResponse",
    "ProblemError",
    "ProblemErrorCtxType0",
    "ProblemResponse",
    "ProcessorPipelineStep",
    "ProcessorPipelineStepAttributes",
    "ProcessorPipelineStepParams",
    "ProcessorPipelineStepWires",
    "ProjectCreate",
    "ProjectionJobRequest",
    "ProjectionJobRequestOperation",
    "ProjectionOutputOptions",
    "ProjectionOutputOptionsFormat",
    "ProjectionSampling",
    "ProjectionSamplingInterpolation",
    "ProjectOut",
    "ProjectOutLinksType0",
    "ProjectPatch",
    "ProviderManifest",
    "ProviderOut",
    "ProviderOutLinksType0",
    "RadianceEvalConfig",
    "RadianceEvalConfigBackground",
    "RadianceEvalConfigLpipsNet",
    "RadianceEvalConfigMetricsItem",
    "RadianceEvalConfigSplit",
    "RadianceEvaluateRequest",
    "RadianceEvaluateRequestBackendOptions",
    "RadianceEvaluationOut",
    "RadianceEvaluationOutArtifactsType0Item",
    "RadianceEvaluationOutConfig",
    "RadianceEvaluationOutErrorType0",
    "RadianceEvaluationOutLinksType0",
    "RadianceEvaluationOutStatus",
    "RadianceFieldOut",
    "RadianceFieldOutLinksType0",
    "RadianceFieldOutSpec",
    "RadianceFieldOutStatus",
    "RadianceFieldOutSummaryType0",
    "RadianceMetrics",
    "RadianceSnapshotListResponse",
    "RadianceSnapshotListResponseLinksType0",
    "RadianceSnapshotOut",
    "RadianceSnapshotOutLinksType0",
    "RadianceSnapshotOutSummaryType0",
    "RadianceTrainRequest",
    "RadianceTrainRequestBackendOptions",
    "ReadCorrespondenceGraphV1ReconstructionsReconIdCorrespondenceGraphJsonGetResponse200",
    "ReadTwoViewGeometriesV1ReconstructionsReconIdTwoViewGeometriesJsonGetResponse200",
    "ReadyzResponse",
    "ReadyzResponseChecks",
    "ReconstructionOut",
    "ReconstructionOutLinksType0",
    "ReconstructionOutStatus",
    "RelocalizeSpec",
    "RelocalizeSpecBackendOptions",
    "RigConfigSpec",
    "RigConfigSpecBackendOptions",
    "RigConfigSpecRigConfig",
    "Rigid3",
    "Rotation",
    "RoutingOut",
    "RoutingOutProfiles",
    "RoutingOutProjectProfiles",
    "RoutingOutWorkspaceProfiles",
    "RoutingProfile",
    "RoutingProfileRoutes",
    "RunRecipeV1ProjectsProjectIdPipelinesRecipePostRecipe",
    "RuntimeModes",
    "S3SourceSpec",
    "Sim3",
    "SnapshotListResponse",
    "SnapshotListResponseLinksType0",
    "SpecResponse",
    "SpecServerInfo",
    "SphericalSpec",
    "SphericalSpecBackendOptions",
    "SphericalSpecInputArtifacts",
    "StageArtifactOut",
    "StageArtifactOutLinksType0",
    "StageArtifactOutMetadataType0",
    "StageArtifactOutProducerType0",
    "StageArtifactOutSummaryType0",
    "SubModelOut",
    "SubModelOutLinksType0",
    "SubModelOutRigidityType0",
    "SubModelOutSummaryType0",
    "TaskOut",
    "TaskOutOutputsRefType0",
    "TaskOutStatus",
    "TaskProgressOut",
    "TaskProgressOutStatus",
    "TilesIndexV1ReconstructionsReconIdSnapshotsSeqTilesIndexJsonGetResponse200",
    "ToolDetection",
    "ToolDetectionOut",
    "ToolDetectionOutTools",
    "ToolDetectionSource",
    "TorchRuntime",
    "TorchRuntimeDevice",
    "TorchRuntimeInstallEnv",
    "TorchRuntimePolicy",
    "TriangulateSpec",
    "TriangulateSpecBackendOptions",
    "TwoViewSpec",
    "TwoViewSpecBackendOptions",
    "UndistortSpec",
    "UndistortSpecBackendOptions",
    "UploadEntrySpec",
    "UploadFinalizeRequest",
    "UploadInit",
    "UploadOut",
    "UploadOutState",
    "UploadSourceSpec",
    "UpstreamProject",
    "UvRuntime",
    "ValidationError",
    "ValidationErrorContext",
    "VerifyRequest",
    "VerifyRequestInputArtifacts",
    "VerifySpec",
    "VerifySpecBackendOptions",
    "VerifySpecInputArtifacts",
    "VersionResponse",
    "VideoFramesRequest",
    "VocabTreeSpec",
    "VocabTreeSpecBackendOptions",
)
