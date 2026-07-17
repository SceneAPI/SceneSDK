// SPDX-License-Identifier: Apache-2.0
// Copyright the sfmapi authors. See cpp/LICENSE (Apache-2.0).
// sfmapi — pipeline / stage spec POD structs for C++.
//
// The C++ SDK historically asked callers to build JSON bodies as
// strings. These structs give parity with Python / TypeScript: build
// a `FeaturesSpec`/`MatcherSpec`/etc. and call `.ToJson()` to get a
// `sfmapi::Json` value (or `.ToJsonString()` for the wire body).
//
// Field layout exactly mirrors `app/schemas/pipeline_spec.py` and
// `clients/python/sfmapi_client/models.py`.

#ifndef SFMAPI_SPECS_HPP_
#define SFMAPI_SPECS_HPP_

#include <map>
#include <optional>
#include <string>
#include <utility>
#include <vector>

#include "sfmapi/json.hpp"

namespace sfmapi {

// ====================================================================
//  Stage artifact inputs
// ====================================================================

struct ArtifactRef {
  std::string artifact_id;
  std::optional<std::string> kind;

  Json ToJson() const {
    Json::Object o{{"artifact_id", artifact_id}};
    if (kind) {
      o["kind"] = *kind;
    }
    return Json(std::move(o));
  }
};

using ArtifactInputMap = std::map<std::string, ArtifactRef>;

inline void AddInputArtifacts(Json::Object& o,
                              const ArtifactInputMap& input_artifacts) {
  if (input_artifacts.empty()) {
    return;
  }
  Json::Object refs;
  for (const auto& kv : input_artifacts) {
    refs[kv.first] = kv.second.ToJson();
  }
  o["input_artifacts"] = Json(std::move(refs));
}

// ====================================================================
//  Local-feature extractor
// ====================================================================

/// Canonical extractor types — mirrors `FeatureType`.
constexpr const char* kFeatureTypeSift = "sift";
constexpr const char* kFeatureTypeSuperPoint = "superpoint";
constexpr const char* kFeatureTypeAliked = "aliked";
constexpr const char* kFeatureTypeDisk = "disk";
constexpr const char* kFeatureTypeR2D2 = "r2d2";
constexpr const char* kFeatureTypeD2Net = "d2net";
constexpr const char* kFeatureTypeSosNet = "sosnet";

struct FeaturesSpec {
  int version = 1;
  std::string type = kFeatureTypeSift;
  std::optional<std::string> provider;
  int max_num_features = 8192;
  bool use_gpu = true;
  int seed = 0;
  Json::Object backend_options;
  ArtifactInputMap input_artifacts;

  Json ToJson() const {
    Json::Object o{
        {"version", static_cast<double>(version)},
        {"type", type},
        {"max_num_features", static_cast<double>(max_num_features)},
        {"use_gpu", use_gpu},
        {"seed", static_cast<double>(seed)},
    };
    if (provider) {
      o["provider"] = *provider;
    }
    if (!backend_options.empty()) {
      o["backend_options"] = Json(backend_options);
    }
    AddInputArtifacts(o, input_artifacts);
    return Json(std::move(o));
  }

  std::string ToJsonString() const { return ToJson().Dump(); }
};

// ====================================================================
//  Pair-selection
// ====================================================================

constexpr const char* kPairExhaustive = "exhaustive";
constexpr const char* kPairSequential = "sequential";
constexpr const char* kPairSpatial = "spatial";
constexpr const char* kPairVocabTree = "vocabtree";
constexpr const char* kPairRetrieval = "retrieval";
constexpr const char* kPairFromPoses = "from_poses";
constexpr const char* kPairExplicit = "explicit";
constexpr const char* kPairsBlobFormatImageNamePairsTxt = "image_name_pairs_txt";

struct ImagePairRef {
  std::string image_name1;
  std::string image_name2;

  Json ToJson() const {
    return Json(Json::Object{
        {"image_name1", image_name1},
        {"image_name2", image_name2},
    });
  }
};

struct PairsSpec {
  int version = 1;
  std::string strategy = kPairExhaustive;
  std::optional<std::string> provider;
  int overlap = 10;
  std::optional<std::string> vocab_tree_path;
  std::string retrieval_strategy = "vlad";  // dhash | vlad | netvlad
  int retrieval_k = 20;
  std::optional<double> overlap_distance_m;
  std::optional<double> max_angle_deg;
  std::vector<ImagePairRef> image_pairs;
  std::optional<std::string> pairs_blob_sha;
  std::string pairs_blob_format = kPairsBlobFormatImageNamePairsTxt;
  Json::Object backend_options;
  ArtifactInputMap input_artifacts;

  Json ToJson() const {
    Json::Object o{
        {"version", static_cast<double>(version)},
        {"strategy", strategy},
        {"overlap", static_cast<double>(overlap)},
        {"retrieval_strategy", retrieval_strategy},
        {"retrieval_k", static_cast<double>(retrieval_k)},
        {"pairs_blob_format", pairs_blob_format},
    };
    if (provider) o["provider"] = *provider;
    if (vocab_tree_path) o["vocab_tree_path"] = *vocab_tree_path;
    if (overlap_distance_m) o["overlap_distance_m"] = *overlap_distance_m;
    if (max_angle_deg) o["max_angle_deg"] = *max_angle_deg;
    if (!image_pairs.empty()) {
      Json::Array pairs;
      for (const auto& pair : image_pairs) {
        pairs.push_back(pair.ToJson());
      }
      o["image_pairs"] = Json(std::move(pairs));
    }
    if (pairs_blob_sha) o["pairs_blob_sha"] = *pairs_blob_sha;
    if (!backend_options.empty()) o["backend_options"] = Json(backend_options);
    AddInputArtifacts(o, input_artifacts);
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

// ====================================================================
//  Matcher
// ====================================================================

constexpr const char* kMatcherNnMutual = "nn-mutual";
constexpr const char* kMatcherNnRatio = "nn-ratio";
constexpr const char* kMatcherSuperGlue = "superglue";
constexpr const char* kMatcherLightGlue = "lightglue";
constexpr const char* kMatcherLoFTR = "loftr";
constexpr const char* kMatcherMASt3R = "mast3r";

struct MatcherSpec {
  int version = 1;
  std::string type = kMatcherNnMutual;
  std::optional<std::string> provider;
  bool use_gpu = true;
  bool cross_check = true;
  double max_ratio = 0.8;
  double max_distance = 0.7;
  Json::Object backend_options;
  ArtifactInputMap input_artifacts;

  Json ToJson() const {
    Json::Object o{
        {"version", static_cast<double>(version)},
        {"type", type},
        {"use_gpu", use_gpu},
        {"cross_check", cross_check},
        {"max_ratio", max_ratio},
        {"max_distance", max_distance},
    };
    if (provider) {
      o["provider"] = *provider;
    }
    if (!backend_options.empty()) {
      o["backend_options"] = Json(backend_options);
    }
    AddInputArtifacts(o, input_artifacts);
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

// ====================================================================
//  Verify + BA
// ====================================================================

struct VerifySpec {
  int version = 1;
  std::optional<std::string> provider;
  bool use_gpu = true;
  double min_inlier_ratio = 0.25;
  Json::Object backend_options;
  ArtifactInputMap input_artifacts;

  Json ToJson() const {
    Json::Object o{
        {"version", static_cast<double>(version)},
        {"use_gpu", use_gpu},
        {"min_inlier_ratio", min_inlier_ratio},
    };
    if (provider) {
      o["provider"] = *provider;
    }
    if (!backend_options.empty()) {
      o["backend_options"] = Json(backend_options);
    }
    AddInputArtifacts(o, input_artifacts);
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

constexpr const char* kBaModeStandard = "standard";
constexpr const char* kBaModeTwoStage = "two_stage";
constexpr const char* kBaModeFeaturemetric = "featuremetric";
constexpr const char* kBaModeRig = "rig";

constexpr const char* kBaLossSquared = "squared";
constexpr const char* kBaLossHuber = "huber";
constexpr const char* kBaLossCauchy = "cauchy";
constexpr const char* kBaLossSoftL1 = "soft_l1";
constexpr const char* kBaLossTukey = "tukey";

struct BundleAdjustmentSpec {
  int version = 1;
  std::string mode = kBaModeStandard;
  std::optional<std::string> provider;
  bool refine_focal_length = true;
  bool refine_principal_point = false;
  bool refine_extra_params = true;
  int max_num_iterations = 100;
  std::string loss_kernel = kBaLossSquared;
  double loss_threshold = 1.0;
  Json::Object backend_options;

  Json ToJson() const {
    Json::Object o{
        {"version", static_cast<double>(version)},
        {"mode", mode},
        {"refine_focal_length", refine_focal_length},
        {"refine_principal_point", refine_principal_point},
        {"refine_extra_params", refine_extra_params},
        {"max_num_iterations", static_cast<double>(max_num_iterations)},
        {"loss_kernel", loss_kernel},
        {"loss_threshold", loss_threshold},
    };
    if (provider) {
      o["provider"] = *provider;
    }
    if (!backend_options.empty()) {
      o["backend_options"] = Json(backend_options);
    }
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

// ====================================================================
//  Mapping pipeline specs (discriminated by `kind`)
// ====================================================================

struct IncrementalSpec {
  std::string kind = "incremental";
  int version = 1;
  std::optional<std::string> provider;
  int seed = 0;
  std::optional<int> max_runtime_seconds;
  std::optional<int> snapshot_frames_freq = 50;
  Json::Object backend_options;
  std::optional<std::pair<std::string, std::string>> init_image_pair;
  bool multiple_models = true;
  int max_num_models = 50;
  int min_num_matches = 15;
  bool ba_global_use_pba = true;
  bool extract_colors = true;
  ArtifactInputMap input_artifacts;

  Json ToJson() const {
    Json::Object o{
        {"kind", kind},
        {"version", static_cast<double>(version)},
        {"seed", static_cast<double>(seed)},
        {"multiple_models", multiple_models},
        {"max_num_models", static_cast<double>(max_num_models)},
        {"min_num_matches", static_cast<double>(min_num_matches)},
        {"ba_global_use_pba", ba_global_use_pba},
        {"extract_colors", extract_colors},
    };
    if (provider) {
      o["provider"] = *provider;
    }
    if (!backend_options.empty()) {
      o["backend_options"] = Json(backend_options);
    }
    if (max_runtime_seconds) {
      o["max_runtime_seconds"] = static_cast<double>(*max_runtime_seconds);
    }
    if (snapshot_frames_freq) {
      o["snapshot_frames_freq"] = static_cast<double>(*snapshot_frames_freq);
    }
    if (init_image_pair) {
      Json::Array p{init_image_pair->first, init_image_pair->second};
      o["init_image_pair"] = Json(std::move(p));
    }
    AddInputArtifacts(o, input_artifacts);
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

struct GlobalSpec {
  std::string kind = "global";
  int version = 1;
  std::optional<std::string> provider;
  int seed = 0;
  std::optional<int> max_runtime_seconds;
  std::optional<int> snapshot_frames_freq = 50;
  std::string backend = "AUTO";
  std::string formulation = "AUTO";
  bool use_incremental_quality_fallback = true;
  Json::Object backend_options;
  ArtifactInputMap input_artifacts;

  Json ToJson() const {
    Json::Object o{
        {"kind", kind},
        {"version", static_cast<double>(version)},
        {"seed", static_cast<double>(seed)},
        {"backend", backend},
        {"formulation", formulation},
        {"use_incremental_quality_fallback", use_incremental_quality_fallback},
    };
    if (provider) {
      o["provider"] = *provider;
    }
    if (!backend_options.empty()) {
      o["backend_options"] = Json(backend_options);
    }
    if (max_runtime_seconds) {
      o["max_runtime_seconds"] = static_cast<double>(*max_runtime_seconds);
    }
    if (snapshot_frames_freq) {
      o["snapshot_frames_freq"] = static_cast<double>(*snapshot_frames_freq);
    }
    AddInputArtifacts(o, input_artifacts);
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

struct HierarchicalSpec {
  std::string kind = "hierarchical";
  int version = 1;
  std::optional<std::string> provider;
  int seed = 0;
  std::optional<int> max_runtime_seconds;
  std::optional<int> snapshot_frames_freq = 50;
  int cluster_max_size = 100;
  int cluster_overlap = 25;
  Json::Object backend_options;
  ArtifactInputMap input_artifacts;

  Json ToJson() const {
    Json::Object o{
        {"kind", kind},
        {"version", static_cast<double>(version)},
        {"seed", static_cast<double>(seed)},
        {"cluster_max_size", static_cast<double>(cluster_max_size)},
        {"cluster_overlap", static_cast<double>(cluster_overlap)},
    };
    if (provider) {
      o["provider"] = *provider;
    }
    if (!backend_options.empty()) {
      o["backend_options"] = Json(backend_options);
    }
    if (max_runtime_seconds) {
      o["max_runtime_seconds"] = static_cast<double>(*max_runtime_seconds);
    }
    if (snapshot_frames_freq) {
      o["snapshot_frames_freq"] = static_cast<double>(*snapshot_frames_freq);
    }
    AddInputArtifacts(o, input_artifacts);
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

struct SphericalSpec {
  std::string kind = "spherical";
  int version = 1;
  std::optional<std::string> provider;
  int seed = 0;
  std::optional<int> max_runtime_seconds;
  std::optional<int> snapshot_frames_freq = 50;
  bool panorama = true;
  Json::Object backend_options;
  ArtifactInputMap input_artifacts;

  Json ToJson() const {
    Json::Object o{
        {"kind", kind},
        {"version", static_cast<double>(version)},
        {"seed", static_cast<double>(seed)},
        {"panorama", panorama},
    };
    if (provider) {
      o["provider"] = *provider;
    }
    if (!backend_options.empty()) {
      o["backend_options"] = Json(backend_options);
    }
    if (max_runtime_seconds) {
      o["max_runtime_seconds"] = static_cast<double>(*max_runtime_seconds);
    }
    if (snapshot_frames_freq) {
      o["snapshot_frames_freq"] = static_cast<double>(*snapshot_frames_freq);
    }
    AddInputArtifacts(o, input_artifacts);
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

// ====================================================================
//  Typed dataflow pipeline request bodies
// ====================================================================

struct PipelineStep {
  std::string op;
  std::optional<std::string> provider;
  Json::Object params;

  Json ToJson() const {
    Json::Object o{{"op", op}};
    if (provider) o["provider"] = *provider;
    if (!params.empty()) o["params"] = Json(params);
    return Json(std::move(o));
  }
};

struct ProcessorPipelineStep {
  std::string processor;
  std::optional<std::string> ref;
  std::optional<std::string> provider;
  Json::Object attributes;
  Json::Object params;
  Json::Object wires;

  Json ToJson() const {
    Json::Object o{{"processor", processor}};
    if (ref) o["ref"] = *ref;
    if (provider) o["provider"] = *provider;
    if (!attributes.empty()) o["attributes"] = Json(attributes);
    if (!params.empty()) o["params"] = Json(params);
    if (!wires.empty()) o["wires"] = Json(wires);
    return Json(std::move(o));
  }
};

struct PipelineValidateRequest {
  std::vector<std::string> initial_inputs;
  std::vector<Json> steps;

  void AddStep(const std::string& step_id) { steps.push_back(Json(step_id)); }
  void AddStep(const PipelineStep& step) { steps.push_back(step.ToJson()); }
  void AddStep(const ProcessorPipelineStep& step) {
    steps.push_back(step.ToJson());
  }

  Json ToJson() const {
    Json::Object o;
    if (!initial_inputs.empty()) {
      Json::Array inputs;
      for (const auto& item : initial_inputs) inputs.push_back(Json(item));
      o["initial_inputs"] = Json(std::move(inputs));
    }
    Json::Array body_steps;
    for (const auto& step : steps) body_steps.push_back(step);
    o["steps"] = Json(std::move(body_steps));
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

struct PipelineRunRequest : PipelineValidateRequest {
  std::string dataset_id;

  Json ToJson() const {
    Json value = PipelineValidateRequest::ToJson();
    value["dataset_id"] = dataset_id;
    return value;
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

// ====================================================================
//  Reconstruction-level stage request bodies
// ====================================================================

/// Body for `POST /v1/reconstructions/{rid}/localize`.
struct LocalizationRequest {
  std::string blob_sha;
  std::optional<std::string> provider;
  Json::Object sift;  // optional SIFT extraction overrides

  Json ToJson() const {
    Json::Object o{{"blob_sha", blob_sha}};
    if (provider) {
      o["provider"] = *provider;
    }
    if (!sift.empty()) {
      o["sift"] = Json(sift);
    }
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

/// Body for `POST /v1/reconstructions:merge`.
struct MergeRequest {
  std::string target_recon_id;
  std::vector<std::string> source_recon_ids;
  std::optional<std::string> provider;
  std::vector<Json::Object> sim3_aligners;

  Json ToJson() const {
    Json::Object o{{"target_recon_id", target_recon_id}};
    Json::Array sources;
    for (const auto& rid : source_recon_ids) {
      sources.push_back(Json(rid));
    }
    o["source_recon_ids"] = Json(std::move(sources));
    if (provider) {
      o["provider"] = *provider;
    }
    if (!sim3_aligners.empty()) {
      Json::Array aligners;
      for (const auto& aligner : sim3_aligners) {
        aligners.push_back(Json(aligner));
      }
      o["sim3_aligners"] = Json(std::move(aligners));
    }
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

/// Body for the dataset-scoped projection routes
/// (`:project_images` / `:render_cubemap` / `:render_equirectangular`
/// / `:render_perspective`). Exactly one of `cubemap` / `perspective`
/// / `equirectangular` is set, matching `operation`.
struct ProjectionJobRequest {
  std::string operation;
  std::optional<std::string> provider;
  Json::Object cubemap;
  Json::Object perspective;
  Json::Object equirectangular;

  Json ToJson() const {
    Json::Object o{{"operation", operation}};
    if (provider) {
      o["provider"] = *provider;
    }
    if (!cubemap.empty()) {
      o["cubemap"] = Json(cubemap);
    }
    if (!perspective.empty()) {
      o["perspective"] = Json(perspective);
    }
    if (!equirectangular.empty()) {
      o["equirectangular"] = Json(equirectangular);
    }
    return Json(std::move(o));
  }
  std::string ToJsonString() const { return ToJson().Dump(); }
};

}  // namespace sfmapi

#endif  // SFMAPI_SPECS_HPP_
