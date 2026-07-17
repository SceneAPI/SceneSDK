// SPDX-License-Identifier: Apache-2.0
// Copyright the sfmapi authors. See cpp/LICENSE (Apache-2.0).
// sfmapi C++ HTTP client — pluggable-transport.
//
// HTTP and JSON are platform-specific concerns; rather than picking
// one HTTP library and one JSON library, this header:
//
//   1. Defines a `Transport` callback type that takes an HTTP request
//      shape and returns an HTTP response shape. Consumers plug in:
//        - libcurl on the desktop
//        - cpp-httplib for header-only deployments
//        - Emscripten Fetch in WASM browser builds
//        - any custom std::function<> in tests
//
//   2. Provides a `Client` class that builds the right URL + body for
//      every endpoint and invokes the transport. JSON parsing is
//      delegated to a `JsonAdapter` that the consumer also injects
//      (typedef on a function that converts std::string ↔ generic
//      "value" type — see the README for an nlohmann::json sample).
//
// The result: zero hard dependencies, total flexibility, and one
// consistent surface across desktop/WASM/embedded.
//
// Usage (with libcurl + nlohmann::json):
//
//     #include "sfmapi/client.hpp"
//     #include "sfmapi/transport_curl.hpp"   // your wrapper
//
//     sfmapi::Client c{"http://localhost:8080", MakeCurlTransport(),
//                      MakeNlohmannJsonAdapter()};
//     auto caps = c.Capabilities();
//     if (caps.Supports("ba.standard")) {
//         auto job = c.SubmitBundleAdjust(recon_id);
//     }

#ifndef SFMAPI_CLIENT_HPP_
#define SFMAPI_CLIENT_HPP_

#include <chrono>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <functional>
#include <map>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <utility>
#include <vector>

#include "sfmapi/json.hpp"
#include "sfmapi/sfmapi.hpp"
#include "sfmapi/specs.hpp"
#include "sfmapi/sse.hpp"

namespace sfmapi {

// ====================================================================
//  Transport contract
// ====================================================================

struct HttpRequest {
  std::string method;       // "GET", "POST", "PATCH", "PUT", "DELETE"
  std::string url;          // fully-qualified
  std::map<std::string, std::string> headers;
  std::vector<std::uint8_t> body;
};

struct HttpResponse {
  int status = 0;
  std::map<std::string, std::string> headers;
  std::vector<std::uint8_t> body;
};

/// User-provided HTTP transport. Errors are signaled by throwing a
/// `TransportError` or returning a 5xx response — callers MUST handle
/// both.
using Transport = std::function<HttpResponse(const HttpRequest&)>;

class TransportError : public std::runtime_error {
 public:
  using std::runtime_error::runtime_error;
};

class HttpStatusError : public std::runtime_error {
 public:
  HttpStatusError(int status, std::string capability)
      : std::runtime_error("sfmapi HTTP status " + std::to_string(status)),
        status_(status),
        capability_(std::move(capability)) {}

  int status() const noexcept { return status_; }
  const std::string& capability() const noexcept { return capability_; }

 private:
  int status_ = 0;
  std::string capability_;
};

// ====================================================================
//  JSON adapter contract — keep the SDK JSON-library-agnostic.
//
//  `JsonValue` is intentionally untyped: it's whatever your JSON
//  library returns. The SDK only ever shuttles JSON between the
//  transport and the consumer. Decoding into `sfmapi::Camera` etc.
//  is the consumer's job (the structs in `sfmapi.hpp` are designed
//  to make that one-liners).
// ====================================================================

using JsonString = std::string;

/// Encode a JSON-shape (e.g. `{"name": "x"}`) to a string. Returns
/// the body to send.
using JsonEncoder = std::function<JsonString(const void* user_data)>;

/// The JSON adapter is a pair of encode + decode functions.
struct JsonAdapter {
  /// Encode a typed body to a JSON string. Implementations typically
  /// take an nlohmann::json / RapidJSON / picojson value via a
  /// type-erased pointer; see the README for ready-made adapters.
  std::function<JsonString(const void* body)> encode;
  /// Decode a JSON string to user-typed value.
  std::function<void(const JsonString& body, void* out)> decode;
};

// ====================================================================
//  Client
// ====================================================================

struct ClientOptions {
  std::string base_url;       // e.g. "http://localhost:8080"
  std::string api_key;        // optional bearer token
  Transport transport;        // required
  JsonAdapter json;           // optional; only methods returning typed
                              // values need it
  std::map<std::string, std::string> default_headers;
};

class Client {
 public:
  explicit Client(ClientOptions opts) : opts_(std::move(opts)) {
    if (!opts_.transport) {
      throw std::invalid_argument("sfmapi::Client requires a Transport");
    }
    while (!opts_.base_url.empty() && opts_.base_url.back() == '/') {
      opts_.base_url.pop_back();
    }
  }

  // --- meta -------------------------------------------------------

  HttpResponse Healthz() const { return Get("/healthz"); }
  HttpResponse Version() const { return Get("/version"); }
  HttpResponse Capabilities() const { return Get("/v1/capabilities"); }

  // --- projects ---------------------------------------------------

  HttpResponse CreateProject(const std::string& name,
                             const std::string& description = "") const {
    return Post("/v1/projects",
                "{\"name\":\"" + JsonEscape(name) + "\"," +
                    "\"description\":" +
                    (description.empty() ? "null"
                                         : "\"" + JsonEscape(description) + "\"") +
                    "}");
  }

  HttpResponse GetProject(const std::string& project_id) const {
    return Get("/v1/projects/" + project_id);
  }

  HttpResponse ListProjects() const { return Get("/v1/projects"); }

  HttpResponse DeleteProject(const std::string& project_id) const {
    return Delete("/v1/projects/" + project_id);
  }

  // --- datasets ---------------------------------------------------

  /// `body` is a pre-encoded JSON object (use the JSON adapter to
  /// build one). The C++ SDK keeps body construction explicit so
  /// you can reuse whatever JSON library your project already has.
  HttpResponse CreateDataset(const std::string& project_id,
                             const std::string& json_body) const {
    return Post("/v1/projects/" + project_id + "/datasets", json_body);
  }

  HttpResponse GetDataset(const std::string& project_id,
                          const std::string& dataset_id) const {
    return Get("/v1/projects/" + project_id + "/datasets/" + dataset_id);
  }

  HttpResponse ListDatasets(const std::string& project_id) const {
    return Get("/v1/projects/" + project_id + "/datasets");
  }

  HttpResponse DeleteDataset(const std::string& project_id,
                             const std::string& dataset_id) const {
    return Delete("/v1/projects/" + project_id + "/datasets/" + dataset_id);
  }

  // --- images / uploads -------------------------------------------

  HttpResponse AddImage(const std::string& dataset_id,
                        const std::string& json_body) const {
    return Post("/v1/datasets/" + dataset_id + "/images", json_body);
  }

  HttpResponse ListImages(const std::string& dataset_id) const {
    return Get("/v1/datasets/" + dataset_id + "/images");
  }

  HttpResponse InitUpload(const std::string& json_body) const {
    return Post("/v1/uploads", json_body);
  }

  HttpResponse PatchChunk(const std::string& upload_id,
                          std::vector<std::uint8_t> data,
                          std::int64_t offset) const {
    HttpRequest req{
        "PATCH",
        opts_.base_url + "/v1/uploads/" + upload_id,
        {{"Content-Range",
          "bytes " + std::to_string(offset) + "-" +
              std::to_string(offset + static_cast<std::int64_t>(data.size()) - 1) +
              "/" + std::to_string(offset + data.size())}},
        std::move(data),
    };
    AddAuth(req);
    return Send(req);
  }

  HttpResponse FinalizeUpload(const std::string& upload_id) const {
    return Post("/v1/uploads/" + upload_id + ":finalize", "{}");
  }

  /// Convenience: chunked upload of an in-memory blob. Initializes
  /// an upload, streams the bytes in ``chunk_size`` increments, and
  /// finalizes. Returns the finalize response (which carries the
  /// content-addressed ``blob_sha`` in its JSON body).
  HttpResponse UploadBytes(
      const std::vector<std::uint8_t>& data,
      std::size_t chunk_size = 1 * 1024 * 1024,
      const std::string& content_type = "") const {
    std::string init_body = "{\"expected_size\":" + std::to_string(data.size());
    if (!content_type.empty()) {
      init_body += ",\"content_type\":\"" + JsonEscape(content_type) + "\"";
    }
    init_body += "}";
    auto init_resp = RaiseOnError(InitUpload(init_body));
    std::string body(init_resp.body.begin(), init_resp.body.end());
    auto pos = body.find("\"upload_id\":\"");
    if (pos == std::string::npos) {
      throw std::runtime_error("UploadBytes: server response has no upload_id");
    }
    pos += std::string("\"upload_id\":\"").size();
    auto end = body.find('"', pos);
    if (end == std::string::npos) {
      throw std::runtime_error("UploadBytes: malformed upload_id");
    }
    std::string upload_id = body.substr(pos, end - pos);
    std::int64_t offset = 0;
    while (offset < static_cast<std::int64_t>(data.size())) {
      auto take = std::min(
          chunk_size, data.size() - static_cast<std::size_t>(offset));
      std::vector<std::uint8_t> chunk(
          data.begin() + offset, data.begin() + offset + take);
      RaiseOnError(PatchChunk(upload_id, std::move(chunk), offset));
      offset += static_cast<std::int64_t>(take);
    }
    return RaiseOnError(FinalizeUpload(upload_id));
  }

  // --- SfM stages -------------------------------------------------

  HttpResponse SubmitFeatures(const std::string& dataset_id,
                              const std::string& json_body = "{}") const {
    return Post("/v1/datasets/" + dataset_id + "/features", json_body);
  }

  HttpResponse SubmitMatches(const std::string& dataset_id,
                             const std::string& json_body = "{}") const {
    return Post("/v1/datasets/" + dataset_id + "/matches", json_body);
  }

  HttpResponse SubmitVerify(const std::string& dataset_id,
                            const std::string& json_body = "{}") const {
    return Post("/v1/datasets/" + dataset_id + "/verify", json_body);
  }

  HttpResponse RunPipeline(const std::string& project_id,
                           const std::string& kind,
                           const std::string& json_body) const {
    return Post("/v1/projects/" + project_id + "/pipelines/" + kind, json_body);
  }

  HttpResponse ValidatePipeline(const std::string& json_body) const {
    return Post("/v1/pipelines:validate", json_body);
  }

  HttpResponse ValidatePipeline(const PipelineValidateRequest& body) const {
    return ValidatePipeline(body.ToJsonString());
  }

  HttpResponse RunPipeline(const std::string& project_id,
                           const std::string& json_body) const {
    return Post("/v1/projects/" + project_id + "/pipelines:run", json_body);
  }

  HttpResponse RunPipeline(const std::string& project_id,
                           const PipelineRunRequest& body) const {
    return RunPipeline(project_id, body.ToJsonString());
  }

  HttpResponse ListAttributes() const { return Get("/v1/attributes"); }

  HttpResponse ListDataTypes() const { return Get("/v1/datatypes"); }

  HttpResponse ListOperations() const { return Get("/v1/operations"); }

  HttpResponse ListProcessors() const { return Get("/v1/processors"); }

  HttpResponse ListPipelines() const { return Get("/v1/pipelines"); }

  // --- jobs -------------------------------------------------------

  HttpResponse GetJob(const std::string& job_id) const {
    return Get("/v1/jobs/" + job_id);
  }

  HttpResponse ListJobArtifacts(
      const std::string& job_id,
      const std::string& kind = "",
      const std::string& task_id = "",
      const std::string& name = "",
      const std::string& page_token = "",
      int page_size = 0) const {
    std::string path = "/v1/jobs/" + job_id + "/artifacts";
    bool first = true;
    AppendQueryParam(path, first, "kind", kind);
    AppendQueryParam(path, first, "task_id", task_id);
    AppendQueryParam(path, first, "name", name);
    AppendQueryParam(path, first, "page_token", page_token);
    if (page_size > 0) {
      AppendQueryParam(path, first, "page_size", std::to_string(page_size));
    }
    return Get(path);
  }

  /// Buffered SSE stream for ``GET /v1/jobs/{id}/events``. Returns
  /// the full response body as ``text/event-stream``; pass to
  /// :func:`ParseSseEvents` (from ``sfmapi/sse.hpp``) to decode.
  /// True streaming requires a streaming-capable Transport — drive
  /// the SSE parser yourself with libcurl's ``CURLOPT_WRITEFUNCTION``
  /// or equivalent in that case.
  HttpResponse GetJobEvents(
      const std::string& job_id,
      std::int64_t last_event_id = -1) const {
    HttpRequest req;
    req.method = "GET";
    req.url = opts_.base_url + "/v1/jobs/" + job_id + "/events";
    req.headers["Accept"] = "text/event-stream";
    if (last_event_id >= 0) {
      req.headers["Last-Event-ID"] = std::to_string(last_event_id);
    }
    if (!opts_.api_key.empty()) {
      req.headers["Authorization"] = "Bearer " + opts_.api_key;
    }
    for (const auto& kv : opts_.default_headers) {
      req.headers[kv.first] = kv.second;
    }
    return opts_.transport(std::move(req));
  }

  /// Convenience: fetch + decode the buffered SSE stream in one
  /// call. Mirrors the Python ``stream_events()`` and TS
  /// ``streamEvents()`` ergonomics in the Client OO surface.
  /// Throws a typed ``HttpStatusError`` on any non-2xx open.
  std::vector<SseEvent> StreamEvents(
      const std::string& job_id,
      std::int64_t last_event_id = -1) const {
    auto resp = RaiseOnError(GetJobEvents(job_id, last_event_id));
    return ParseSseEvents(std::string(resp.body.begin(), resp.body.end()));
  }

  HttpResponse CancelJob(const std::string& job_id, bool force = false) const {
    return Post(std::string("/v1/jobs/") + job_id + ":cancel" +
                    (force ? "?force=true" : ""),
                "{}");
  }

  HttpResponse ResumeJob(const std::string& job_id) const {
    return Post("/v1/jobs/" + job_id + ":resume", "{}");
  }

  // --- reconstructions / snapshots --------------------------------

  HttpResponse GetReconstruction(const std::string& recon_id) const {
    return Get("/v1/reconstructions/" + recon_id);
  }

  HttpResponse ListReconstructionArtifacts(
      const std::string& recon_id,
      const std::string& kind = "",
      const std::string& task_id = "",
      const std::string& name = "",
      const std::string& page_token = "",
      int page_size = 0) const {
    std::string path = "/v1/reconstructions/" + recon_id + "/artifacts";
    bool first = true;
    AppendQueryParam(path, first, "kind", kind);
    AppendQueryParam(path, first, "task_id", task_id);
    AppendQueryParam(path, first, "name", name);
    AppendQueryParam(path, first, "page_token", page_token);
    if (page_size > 0) {
      AppendQueryParam(path, first, "page_size", std::to_string(page_size));
    }
    return Get(path);
  }

  HttpResponse ListSubmodels(const std::string& recon_id) const {
    return Get("/v1/reconstructions/" + recon_id + "/submodels");
  }

  HttpResponse ListSnapshots(const std::string& recon_id) const {
    return Get("/v1/reconstructions/" + recon_id + "/snapshots");
  }

  HttpResponse ReadSnapshotFile(const std::string& recon_id, int seq,
                                const std::string& name) const {
    return Get("/v1/reconstructions/" + recon_id + "/snapshots/" +
               std::to_string(seq) + "/" + name);
  }

  HttpResponse ReadTwoViewGeometries(const std::string& recon_id) const {
    return Get("/v1/reconstructions/" + recon_id + "/two_view_geometries.json");
  }

  HttpResponse ReadCorrespondenceGraph(const std::string& recon_id) const {
    return Get("/v1/reconstructions/" + recon_id + "/correspondence_graph.json");
  }

  // --- localize / georegister / cubemap / merge -------------------
  //
  // Dense MVS and mesh / texture generation are out of scope for
  // sfmapi by design (separate ``mvsapi`` / ``meshapi`` specs — see
  // SFMAPI-SPEC.md Appendix D). The SDK ships no Submit/Read methods
  // for them. The ``x-sfm-depth-v1`` / ``x-sfm-normal-v1`` binary
  // PARSERS (ParseDepthMap / ParseNormalMap) remain — they decode
  // wire formats a backend may emit as artifacts, independent of any
  // dense route.

  HttpResponse SubmitLocalize(const std::string& recon_id,
                              const std::string& json_body) const {
    return Post("/v1/reconstructions/" + recon_id + "/localize", json_body);
  }

  HttpResponse SubmitGeoregister(const std::string& recon_id,
                                 const std::string& json_body) const {
    return Post("/v1/reconstructions/" + recon_id + "/georegister", json_body);
  }

  HttpResponse SubmitToCubemap(const std::string& recon_id) const {
    return Post("/v1/reconstructions/" + recon_id + ":to_cubemap", "");
  }

  HttpResponse SubmitRenderCubemap(const std::string& dataset_id,
                                   int face_size = 0) const {
    std::string url = "/v1/datasets/" + dataset_id + ":render_cubemap";
    if (face_size > 0) url += "?face_size=" + std::to_string(face_size);
    return Post(url, "");
  }

  HttpResponse SubmitMergeRecons(const std::string& json_body) const {
    return Post("/v1/reconstructions:merge", json_body);
  }

  // --- portable post-mapping + dataset-prep stages ----------------

  HttpResponse SubmitBundleAdjust(const std::string& recon_id,
                                  const std::string& json_body = "{}") const {
    return Post("/v1/reconstructions/" + recon_id + ":bundleAdjust", json_body);
  }

  HttpResponse SubmitTriangulate(const std::string& recon_id,
                                 const std::string& json_body = "{}") const {
    return Post("/v1/reconstructions/" + recon_id + ":triangulate", json_body);
  }

  HttpResponse SubmitPoseGraphOptimize(const std::string& recon_id,
                                       const std::string& json_body = "{}") const {
    return Post("/v1/reconstructions/" + recon_id + ":poseGraphOptimize", json_body);
  }

  HttpResponse SubmitExport(const std::string& recon_id,
                            const std::string& json_body = "{}") const {
    return Post("/v1/reconstructions/" + recon_id + ":export", json_body);
  }

  HttpResponse SubmitRelocalize(const std::string& recon_id,
                                const std::string& json_body = "{}") const {
    return Post("/v1/reconstructions/" + recon_id + ":relocalize", json_body);
  }

  HttpResponse SubmitUndistort(const std::string& recon_id,
                               const std::string& json_body = "{}") const {
    return Post("/v1/reconstructions/" + recon_id + ":undistort", json_body);
  }

  HttpResponse SubmitBuildVocabTree(const std::string& dataset_id,
                                    const std::string& json_body = "{}") const {
    return Post("/v1/datasets/" + dataset_id + ":buildVocabTree", json_body);
  }

  HttpResponse SubmitConfigureRig(const std::string& dataset_id,
                                  const std::string& json_body = "{}") const {
    return Post("/v1/datasets/" + dataset_id + ":configureRig", json_body);
  }

  HttpResponse SubmitEstimateTwoView(const std::string& dataset_id,
                                     const std::string& json_body = "{}") const {
    return Post("/v1/datasets/" + dataset_id + ":estimateTwoView", json_body);
  }

  // --- pose priors -------------------------------------------------

  HttpResponse GetPosePrior(const std::string& image_id) const {
    return Get("/v1/images/" + image_id + "/pose_prior");
  }

  HttpResponse PutPosePrior(const std::string& image_id,
                            const std::string& json_body) const {
    HttpRequest req{
        "PUT",
        opts_.base_url + "/v1/images/" + image_id + "/pose_prior",
        {{"Content-Type", "application/json"}},
        ToBytes(json_body),
    };
    AddAuth(req);
    return Send(req);
  }

  HttpResponse DeletePosePrior(const std::string& image_id) const {
    return Delete("/v1/images/" + image_id + "/pose_prior");
  }

  HttpResponse ListPosePriors(const std::string& dataset_id) const {
    return Get("/v1/datasets/" + dataset_id + "/pose_priors");
  }

  HttpResponse BulkSetPosePriors(const std::string& dataset_id,
                                 const std::string& json_body) const {
    HttpRequest req{
        "PUT",
        opts_.base_url + "/v1/datasets/" + dataset_id + "/pose_priors",
        {{"Content-Type", "application/json"}},
        ToBytes(json_body),
    };
    AddAuth(req);
    return Send(req);
  }

  // --- similarity --------------------------------------------------

  HttpResponse SimilarityNeighbors(const std::string& dataset_id,
                                   const std::string& image_id, int k = 5,
                                   const std::string& strategy = "dhash",
                                   bool include_self = false) const {
    return Get("/v1/datasets/" + dataset_id +
               "/similarity?image_id=" + image_id + "&k=" + std::to_string(k) +
               "&strategy=" + strategy +
               "&include_self=" + (include_self ? "true" : "false"));
  }

  HttpResponse BuildSimilarityIndex(const std::string& dataset_id,
                                    const std::string& strategy = "dhash",
                                    bool force = true) const {
    return Post("/v1/datasets/" + dataset_id +
                    "/similarity:build?strategy=" + strategy +
                    "&force=" + (force ? "true" : "false"),
                "");
  }

  // --- ingest helpers ----------------------------------------------

  HttpResponse SubmitVideoFrames(const std::string& project_id,
                                 const std::string& json_body) const {
    return Post("/v1/projects/" + project_id + "/datasets:from_video", json_body);
  }

  HttpResponse SubmitKaptureImport(const std::string& project_id,
                                   const std::string& json_body) const {
    return Post("/v1/projects/" + project_id + "/datasets:import_kapture",
                json_body);
  }

  // --- meta (extended) -------------------------------------------

  HttpResponse Readyz() const { return Get("/readyz"); }
  HttpResponse Spec() const { return Get("/spec"); }
  HttpResponse OpenApi() const { return Get("/openapi.json"); }
  HttpResponse Metrics() const { return Get("/metrics"); }

  // --- stage artifacts -------------------------------------------

  HttpResponse ListArtifactKinds() const { return Get("/v1/artifacts/kinds"); }

  HttpResponse ListArtifactFormats() const {
    return Get("/v1/artifacts/formats");
  }

  HttpResponse ImportArtifact(const std::string& json_body) const {
    return Post("/v1/artifacts:import", json_body);
  }

  HttpResponse GetArtifact(const std::string& artifact_id) const {
    return Get("/v1/artifacts/" + artifact_id);
  }

  HttpResponse PlanArtifactConversion(const std::string& artifact_id,
                                      const std::string& json_body) const {
    return Post("/v1/artifacts/" + artifact_id + ":conversionPlan", json_body);
  }

  HttpResponse ConvertArtifact(const std::string& artifact_id,
                               const std::string& json_body) const {
    return Post("/v1/artifacts/" + artifact_id + ":convert", json_body);
  }

  HttpResponse ValidateArtifact(const std::string& artifact_id) const {
    return Post("/v1/artifacts/" + artifact_id + ":validate", "{}");
  }

  HttpResponse ReadArtifactContent(const std::string& artifact_id,
                                   bool download = false) const {
    return Get("/v1/artifacts/" + artifact_id + "/content" +
               (download ? "?download=true" : ""));
  }

  // --- projects (extended) ---------------------------------------

  HttpResponse PatchProject(const std::string& project_id,
                            const std::string& json_body) const {
    HttpRequest req{
        "PATCH", opts_.base_url + "/v1/projects/" + project_id,
        {{"Content-Type", "application/json"}}, ToBytes(json_body)};
    AddAuth(req);
    return Send(req);
  }

  // --- datasets (extended) ---------------------------------------

  HttpResponse PatchDataset(const std::string& project_id,
                            const std::string& dataset_id,
                            const std::string& json_body) const {
    HttpRequest req{
        "PATCH",
        opts_.base_url + "/v1/projects/" + project_id + "/datasets/" + dataset_id,
        {{"Content-Type", "application/json"}}, ToBytes(json_body)};
    AddAuth(req);
    return Send(req);
  }

  // --- images (extended) -----------------------------------------

  HttpResponse BatchCreateImages(const std::string& dataset_id,
                                 const std::string& json_body) const {
    return Post("/v1/datasets/" + dataset_id + "/images:batchCreate",
                json_body);
  }

  HttpResponse DeleteImage(const std::string& dataset_id,
                           const std::string& name) const {
    return Delete("/v1/datasets/" + dataset_id + "/images/" + name);
  }

  HttpResponse GetImage(const std::string& image_id) const {
    return Get("/v1/images/" + image_id);
  }

  HttpResponse GetImageBytes(const std::string& image_id,
                             bool download = false) const {
    return Get(std::string("/v1/images/") + image_id + "/bytes" +
               (download ? "?download=true" : ""));
  }

  HttpResponse GetImageThumbnail(const std::string& image_id,
                                 int size = 0) const {
    std::string url = "/v1/images/" + image_id + "/thumbnail";
    if (size > 0) url += "?size=" + std::to_string(size);
    return Get(url);
  }

  HttpResponse GetImageExif(const std::string& image_id) const {
    return Get("/v1/images/" + image_id + "/exif");
  }

  // --- uploads (extended) ----------------------------------------

  HttpResponse GetUpload(const std::string& upload_id) const {
    return Get("/v1/uploads/" + upload_id);
  }

  // --- reconstructions / submodels (extended) --------------------

  HttpResponse GetSubmodel(const std::string& submodel_id) const {
    return Get("/v1/submodels/" + submodel_id);
  }

  // --- snapshot inspection (observations / visibility / tiles) ---

  HttpResponse ReadImageObservations(const std::string& recon_id, int seq,
                                     const std::string& image_id) const {
    return Get("/v1/reconstructions/" + recon_id + "/snapshots/" +
               std::to_string(seq) + "/images/" + image_id + "/observations");
  }

  HttpResponse ReadPointVisibility(const std::string& recon_id, int seq,
                                   const std::string& point3d_id) const {
    return Get("/v1/reconstructions/" + recon_id + "/snapshots/" +
               std::to_string(seq) + "/points/" + point3d_id + "/visibility");
  }

  HttpResponse ReadTilesIndex(const std::string& recon_id, int seq,
                              int max_level = 0) const {
    std::string url = "/v1/reconstructions/" + recon_id + "/snapshots/" +
                      std::to_string(seq) + "/tiles/index.json";
    if (max_level > 0) url += "?max_level=" + std::to_string(max_level);
    return Get(url);
  }

  HttpResponse ReadTile(const std::string& recon_id, int seq, int level,
                        int x, int y, int z) const {
    return Get("/v1/reconstructions/" + recon_id + "/snapshots/" +
               std::to_string(seq) + "/tiles/" + std::to_string(level) + "/" +
               std::to_string(x) + "/" + std::to_string(y) + "/" +
               std::to_string(z) + ".bin");
  }

  // --- admin: api keys -------------------------------------------

  HttpResponse ListApiKeys() const { return Get("/v1/admin/api-keys"); }

  HttpResponse CreateApiKey() const {
    return CreateApiKeyForTenant("default");
  }

  HttpResponse CreateApiKey(const std::string& json_body) const {
    return Post("/v1/admin/api-keys", json_body);
  }

  HttpResponse CreateApiKeyForTenant(
      const std::string& tenant_id,
      const std::optional<std::string>& name = std::nullopt) const {
    Json::Object body{{"tenant_id", tenant_id}};
    if (name) body["name"] = *name;
    return Post("/v1/admin/api-keys", Json(std::move(body)).Dump());
  }

  HttpResponse CreateApiKeyRaw(const std::string& json_body) const {
    return CreateApiKey(json_body);
  }

  HttpResponse DeleteApiKey(const std::string& api_key_id) const {
    return Delete("/v1/admin/api-keys/" + api_key_id);
  }

  // ================================================================
  //  Convenience helpers (mirror Python/TS extras).
  // ================================================================

  /// Read a file from disk and call ``UploadBytes`` on its contents.
  HttpResponse UploadFile(
      const std::string& path,
      std::size_t chunk_size = 1 * 1024 * 1024,
      const std::string& content_type = "") const {
    std::ifstream f(path, std::ios::binary);
    if (!f) throw std::runtime_error("UploadFile: cannot open " + path);
    std::stringstream ss;
    ss << f.rdbuf();
    std::string s = ss.str();
    std::vector<std::uint8_t> bytes(s.begin(), s.end());
    return UploadBytes(bytes, chunk_size, content_type);
  }

  /// New-style match submission — separate `pairs` and `matcher`
  /// shapes (capabilities ``pairs.{strategy}`` + ``matchers.{type}``).
  HttpResponse SubmitMatchesSplit(const std::string& dataset_id,
                                  const PairsSpec& pairs,
                                  const MatcherSpec& matcher) const {
    Json::Object body{
        {"pairs", pairs.ToJson()},
        {"matcher", matcher.ToJson()},
    };
    return SubmitMatches(dataset_id, Json(std::move(body)).Dump());
  }

  /// Poll a localize job and decode the task output as a
  /// :class:`LocalizationResult`. Throws if the job has no completed
  /// localize task.
  LocalizationResult GetLocalizationResult(const std::string& job_id) const {
    auto resp = RaiseOnError(GetJob(job_id));
    auto body = Json::Parse(std::string(resp.body.begin(), resp.body.end()));
    if (!body.contains("tasks")) {
      throw std::runtime_error("GetLocalizationResult: no tasks in job " + job_id);
    }
    for (const auto& t : body["tasks"].as_array()) {
      if (t.contains("kind") && t["kind"].as_string() == "localize" &&
          t.contains("outputs_ref") && !t["outputs_ref"].is_null()) {
        return LocalizationResultFromJson(t["outputs_ref"]);
      }
    }
    throw std::runtime_error("job " + job_id + " has no completed localize task");
  }

  /// Decode a buffered SSE response body (e.g. from a manual
  /// libcurl streaming download) into discrete events.
  static std::vector<SseEvent> ParseEventsBuffer(const std::string& body) {
    return ParseSseEvents(body);
  }

  /// Decode the response of ``Capabilities()`` into a typed
  /// :class:`Capabilities` struct. Missing ``schema_version`` defaults
  /// to 1 for back-compat with pre-versioned servers.
  static sfmapi::Capabilities ParseCapabilities(const HttpResponse& resp) {
    auto body = Json::Parse(std::string(resp.body.begin(), resp.body.end()));
    sfmapi::Capabilities out;
    if (body.contains("schema_version")) {
      out.schema_version = static_cast<int>(body["schema_version"].as_number());
    }
    if (body.contains("backend")) {
      const auto& b = body["backend"];
      if (b.contains("name")) out.backend.name = b["name"].as_string();
      if (b.contains("version")) out.backend.version = b["version"].as_string();
      if (b.contains("vendor")) out.backend.vendor = b["vendor"].as_string();
    }
    if (body.contains("features")) {
      for (const auto& kv : body["features"].as_object()) {
        out.features[kv.first] = kv.second.is_bool() ? kv.second.as_bool() : false;
      }
    }
    return out;
  }

  static sfmapi::ApiKey ApiKeyFromJson(const Json& j) {
    sfmapi::ApiKey out;
    if (j.contains("api_key_id")) out.api_key_id = j["api_key_id"].as_string();
    if (j.contains("tenant_id")) out.tenant_id = j["tenant_id"].as_string();
    if (j.contains("name") && !j["name"].is_null()) {
      out.name = j["name"].as_string();
    }
    if (j.contains("label") && !j["label"].is_null()) {
      out.label = j["label"].as_string();
    } else {
      out.label = out.name;
    }
    if (j.contains("created_at") && !j["created_at"].is_null()) {
      out.created_at = j["created_at"].as_string();
    }
    if (j.contains("revoked")) out.revoked = j["revoked"].as_bool();
    return out;
  }

  static sfmapi::ApiKeyCreated ApiKeyCreatedFromJson(const Json& j) {
    sfmapi::ApiKeyCreated out;
    static_cast<sfmapi::ApiKey&>(out) = ApiKeyFromJson(j);
    if (j.contains("raw_key")) out.raw_key = j["raw_key"].as_string();
    return out;
  }

  static sfmapi::ApiKeyCreated ParseApiKeyCreated(const HttpResponse& resp) {
    return ApiKeyCreatedFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::ApiKey ParseApiKey(const HttpResponse& resp) {
    return ApiKeyFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static std::vector<sfmapi::ApiKey> ParseApiKeyList(const HttpResponse& resp) {
    auto j = Json::Parse(std::string(resp.body.begin(), resp.body.end()));
    std::vector<sfmapi::ApiKey> out;
    for (const auto& item : j.as_array()) out.push_back(ApiKeyFromJson(item));
    return out;
  }

  // ----- Job rollup + wait helpers ---------------------------------
  //  Mirror the Python `wait_for_job` and TS `waitForJob` ergonomics.
  //  C++ has no built-in sleep+backoff machinery so we keep the
  //  contract minimal: poll ``GetJob`` at a fixed interval until the
  //  status is one of the terminal values, return the parsed
  //  ``JobDetail``, throw a typed ``SfmApiError`` on any non-2xx.

  /// Terminal Job statuses. ``succeeded`` / ``failed`` /
  /// ``cancelled`` / ``cancelled_dirty`` come from the server's Job
  /// finite-state machine — see ``app/workers/dispatcher.py::_maybe_finalize_job``.
  static bool IsTerminalJobStatus(const std::string& s) noexcept {
    return s == "succeeded" || s == "failed" || s == "cancelled" ||
           s == "cancelled_dirty";
  }

  /// Decode a JobDetail body into a typed ``JobDetail`` POD struct.
  static sfmapi::JobDetail ParseJobDetail(const HttpResponse& resp) {
    auto j = Json::Parse(std::string(resp.body.begin(), resp.body.end()));
    return JobDetailFromJson(j);
  }

  /// Block until ``job_id`` reaches a terminal status and return the
  /// final ``JobDetail``.
  ///
  /// ``poll_interval_ms`` controls cadence. ``timeout_ms`` caps the
  /// total wait — throws ``std::runtime_error`` on timeout. Any
  /// non-2xx job poll throws via ``RaiseOnError``.
  ///
  /// Sleep is delegated to the supplied ``sleep_fn`` so consumers
  /// can plug in their own scheduler (single-thread reactor, fiber
  /// pool, etc.) instead of ``std::this_thread::sleep_for``.
  sfmapi::JobDetail WaitForJob(
      const std::string& job_id,
      int poll_interval_ms = 250,
      int timeout_ms = 600 * 1000,
      std::function<void(int)> sleep_fn = nullptr) const {
    auto sleeper = sleep_fn ? sleep_fn : [](int ms) {
      std::this_thread::sleep_for(std::chrono::milliseconds(ms));
    };
    auto start = std::chrono::steady_clock::now();
    while (true) {
      auto resp = RaiseOnError(GetJob(job_id));
      auto detail = ParseJobDetail(resp);
      if (IsTerminalJobStatus(detail.status)) {
        return detail;
      }
      auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
                         std::chrono::steady_clock::now() - start)
                         .count();
      if (elapsed >= timeout_ms) {
        throw std::runtime_error(
            "WaitForJob: " + job_id + " still in status='" + detail.status +
            "' after " + std::to_string(timeout_ms) + "ms");
      }
      sleeper(poll_interval_ms);
    }
  }

  /// Submit a job, then stream SSE events live via ``GetJobEvents``
  /// — invoking ``on_event`` for each, until the server closes the
  /// stream — and finally return the terminal :class:`JobDetail`
  /// via :meth:`WaitForJob`.
  ///
  /// C++17 has no generator syntax, so the streaming side is a
  /// callback. ``GetJobEvents`` returns the buffered SSE body as a
  /// single ``HttpResponse``; consumers wanting true streaming
  /// should drive the SSE parser themselves with their HTTP library
  /// of choice (the :func:`ParseSseEvents` helper from
  /// ``sfmapi/sse.hpp`` parses any buffered body).
  sfmapi::JobDetail SubmitAndStream(
      const std::function<HttpResponse()>& submit_fn,
      const std::function<void(const SseEvent&)>& on_event,
      int poll_interval_ms = 250,
      int timeout_ms = 600 * 1000,
      std::function<void(int)> sleep_fn = nullptr) const {
    auto resp = RaiseOnError(submit_fn());
    auto submit = ParseJobSubmitResponse(resp);
    if (submit.job_id.empty()) {
      throw std::runtime_error(
          "SubmitAndStream: submit_fn response carried no job_id");
    }
    // Buffer the SSE body once; tolerate non-200 (server may not
    // emit a stream for very fast jobs that finish before the
    // request lands).
    auto stream_resp = GetJobEvents(submit.job_id);
    if (stream_resp.status == 200 && on_event) {
      std::string body(stream_resp.body.begin(), stream_resp.body.end());
      for (const auto& ev : ParseSseEvents(body)) {
        on_event(ev);
      }
    }
    return WaitForJob(submit.job_id, poll_interval_ms, timeout_ms,
                      std::move(sleep_fn));
  }

  /// Submit a job via ``submit_fn`` then block on :meth:`WaitForJob`
  /// for the returned ``job_id``. The most-used end-to-end consumer
  /// flow: "do the thing, give me the final JobDetail".
  ///
  /// ``submit_fn`` is any callable that returns an
  /// :class:`HttpResponse`; it's typically a closure that calls one
  /// of the ``Submit*`` methods (e.g.
  /// ``[&]() { return SubmitFeatures(...); }``).
  sfmapi::JobDetail SubmitAndWait(
      const std::function<HttpResponse()>& submit_fn,
      int poll_interval_ms = 250,
      int timeout_ms = 600 * 1000,
      std::function<void(int)> sleep_fn = nullptr) const {
    auto resp = RaiseOnError(submit_fn());
    auto submit = ParseJobSubmitResponse(resp);
    if (submit.job_id.empty()) {
      throw std::runtime_error(
          "SubmitAndWait: submit_fn response carried no job_id");
    }
    return WaitForJob(submit.job_id, poll_interval_ms, timeout_ms,
                      std::move(sleep_fn));
  }

  /// Decode the response of any ``Submit*()`` into a typed
  /// :class:`JobSubmitResponse`.
  static sfmapi::JobSubmitResponse ParseJobSubmitResponse(
      const HttpResponse& resp) {
    auto body = Json::Parse(std::string(resp.body.begin(), resp.body.end()));
    sfmapi::JobSubmitResponse out;
    auto get_string = [&](const char* key) {
      return body.contains(key) && !body[key].is_null()
                 ? body[key].as_string()
                 : std::string();
    };
    if (body.contains("job_id")) out.job_id = body["job_id"].as_string();
    out.recon_id = get_string("recon_id");
    out.dataset_id = get_string("dataset_id");
    out.project_id = get_string("project_id");
    out.method = get_string("method");
    out.target_recon_id = get_string("target_recon_id");
    out.strategy = get_string("strategy");
    out.action_id = get_string("action_id");
    out.backend = get_string("backend");
    out.provider = get_string("provider");
    out.artifact_id = get_string("artifact_id");
    out.target_format = get_string("target_format");
    out.radiance_field_id = get_string("radiance_field_id");
    out.radiance_evaluation_id = get_string("radiance_evaluation_id");
    if (body.contains("applied_sim3") && !body["applied_sim3"].is_null()) {
      out.applied_sim3_json = body["applied_sim3"].Dump();
    }
    if (body.contains("source_recon_ids") &&
        !body["source_recon_ids"].is_null()) {
      for (const auto& item : body["source_recon_ids"].as_array()) {
        out.source_recon_ids.push_back(item.as_string());
      }
    }
    if (body.contains("task_ids")) {
      for (const auto& t : body["task_ids"].as_array()) {
        out.task_ids.push_back(t.as_string());
      }
    }
    return out;
  }

  static std::string OptionalString(const Json& j, const char* key) {
    return j.contains(key) && !j[key].is_null() ? j[key].as_string()
                                                : std::string();
  }

  static std::vector<std::string> StringArrayFromJson(const Json& j) {
    std::vector<std::string> out;
    if (j.is_null()) return out;
    for (const auto& item : j.as_array()) out.push_back(item.as_string());
    return out;
  }

  static std::map<std::string, std::string> StringMapFromJson(const Json& j) {
    std::map<std::string, std::string> out;
    if (j.is_null()) return out;
    for (const auto& kv : j.as_object()) {
      if (!kv.second.is_null()) out[kv.first] = kv.second.as_string();
    }
    return out;
  }

  static sfmapi::AttributeOut AttributeOutFromJson(const Json& j) {
    sfmapi::AttributeOut out;
    out.name = OptionalString(j, "name");
    out.type = OptionalString(j, "type");
    if (j.contains("required")) out.required = j["required"].as_bool();
    out.description = OptionalString(j, "description");
    if (j.contains("default") && !j["default"].is_null()) {
      out.default_json = j["default"].Dump();
    }
    if (j.contains("enum") && !j["enum"].is_null()) {
      out.enum_values = StringArrayFromJson(j["enum"]);
    }
    if (j.contains("min") && !j["min"].is_null()) {
      out.min = j["min"].as_number();
    }
    if (j.contains("max") && !j["max"].is_null()) {
      out.max = j["max"].as_number();
    }
    return out;
  }

  static sfmapi::DataTypeOut DataTypeOutFromJson(const Json& j) {
    sfmapi::DataTypeOut out;
    out.type_id = OptionalString(j, "type_id");
    out.title = OptionalString(j, "title");
    out.kind = OptionalString(j, "kind");
    if (j.contains("aliases") && !j["aliases"].is_null()) {
      out.aliases = StringArrayFromJson(j["aliases"]);
    }
    out.description = OptionalString(j, "description");
    return out;
  }

  static sfmapi::PortSpecOut PortSpecOutFromJson(const Json& j) {
    sfmapi::PortSpecOut out;
    out.datatype = OptionalString(j, "datatype");
    if (j.contains("required")) out.required = j["required"].as_bool();
    if (j.contains("multiple")) out.multiple = j["multiple"].as_bool();
    out.description = OptionalString(j, "description");
    return out;
  }

  static std::map<std::string, sfmapi::PortSpecOut> PortSpecMapFromJson(
      const Json& j) {
    std::map<std::string, sfmapi::PortSpecOut> out;
    if (j.is_null()) return out;
    for (const auto& kv : j.as_object()) {
      if (!kv.second.is_null()) out[kv.first] = PortSpecOutFromJson(kv.second);
    }
    return out;
  }

  static sfmapi::ProcessorOut ProcessorOutFromJson(const Json& j) {
    sfmapi::ProcessorOut out;
    out.processor_id = OptionalString(j, "processor_id");
    out.title = OptionalString(j, "title");
    if (j.contains("consumer")) out.consumer = PortSpecMapFromJson(j["consumer"]);
    if (j.contains("supplier")) out.supplier = PortSpecMapFromJson(j["supplier"]);
    if (j.contains("attributes") && !j["attributes"].is_null()) {
      for (const auto& item : j["attributes"].as_array()) {
        out.attributes.push_back(AttributeOutFromJson(item));
      }
    }
    if (j.contains("special_inputs")) {
      out.special_inputs = PortSpecMapFromJson(j["special_inputs"]);
    }
    if (j.contains("special_attributes") &&
        !j["special_attributes"].is_null()) {
      for (const auto& item : j["special_attributes"].as_array()) {
        out.special_attributes.push_back(AttributeOutFromJson(item));
      }
    }
    if (j.contains("capabilities") && !j["capabilities"].is_null()) {
      out.capabilities = StringArrayFromJson(j["capabilities"]);
    }
    out.config_stage = OptionalString(j, "config_stage");
    if (j.contains("aliases") && !j["aliases"].is_null()) {
      out.aliases = StringArrayFromJson(j["aliases"]);
    }
    out.description = OptionalString(j, "description");
    return out;
  }

  static sfmapi::OperationOut OperationOutFromJson(const Json& j) {
    sfmapi::OperationOut out;
    out.op_id = OptionalString(j, "op_id");
    out.title = OptionalString(j, "title");
    if (j.contains("consumes") && !j["consumes"].is_null()) {
      out.consumes = StringArrayFromJson(j["consumes"]);
    }
    if (j.contains("produces") && !j["produces"].is_null()) {
      out.produces = StringArrayFromJson(j["produces"]);
    }
    if (j.contains("capabilities") && !j["capabilities"].is_null()) {
      out.capabilities = StringArrayFromJson(j["capabilities"]);
    }
    out.config_stage = OptionalString(j, "config_stage");
    out.description = OptionalString(j, "description");
    return out;
  }

  static sfmapi::PipelineDefinitionStepOut PipelineDefinitionStepOutFromJson(
      const Json& j) {
    sfmapi::PipelineDefinitionStepOut out;
    out.ref = OptionalString(j, "ref");
    out.processor = OptionalString(j, "processor");
    if (j.contains("attributes") && !j["attributes"].is_null()) {
      out.attributes_json = j["attributes"].Dump();
    }
    if (j.contains("wires") && !j["wires"].is_null()) {
      out.wires_json = j["wires"].Dump();
    }
    return out;
  }

  static sfmapi::PipelineDefinitionOut PipelineDefinitionOutFromJson(
      const Json& j) {
    sfmapi::PipelineDefinitionOut out;
    out.pipeline_id = OptionalString(j, "pipeline_id");
    out.title = OptionalString(j, "title");
    if (j.contains("aliases") && !j["aliases"].is_null()) {
      out.aliases = StringArrayFromJson(j["aliases"]);
    }
    if (j.contains("initial_inputs") && !j["initial_inputs"].is_null()) {
      out.initial_inputs = StringArrayFromJson(j["initial_inputs"]);
    }
    if (j.contains("steps") && !j["steps"].is_null()) {
      for (const auto& item : j["steps"].as_array()) {
        out.steps.push_back(PipelineDefinitionStepOutFromJson(item));
      }
    }
    out.description = OptionalString(j, "description");
    return out;
  }

  static std::map<std::string, std::vector<std::string>>
  StringListMapFromJson(const Json& j) {
    std::map<std::string, std::vector<std::string>> out;
    if (j.is_null()) return out;
    for (const auto& kv : j.as_object()) {
      if (!kv.second.is_null()) out[kv.first] = StringArrayFromJson(kv.second);
    }
    return out;
  }

  static sfmapi::AttributesContractOut AttributesContractOutFromJson(
      const Json& j) {
    sfmapi::AttributesContractOut out;
    out.contract = OptionalString(j, "contract");
    if (j.contains("contract_schema_version")) {
      out.contract_schema_version =
          static_cast<std::int32_t>(j["contract_schema_version"].as_number());
    }
    if (j.contains("attribute_types") && !j["attribute_types"].is_null()) {
      out.attribute_types = StringArrayFromJson(j["attribute_types"]);
    }
    if (j.contains("rules")) out.rules = StringMapFromJson(j["rules"]);
    return out;
  }

  static sfmapi::DataTypesContractOut DataTypesContractOutFromJson(
      const Json& j) {
    sfmapi::DataTypesContractOut out;
    out.contract = OptionalString(j, "contract");
    if (j.contains("contract_schema_version")) {
      out.contract_schema_version =
          static_cast<std::int32_t>(j["contract_schema_version"].as_number());
    }
    if (j.contains("kinds") && !j["kinds"].is_null()) {
      out.kinds = StringArrayFromJson(j["kinds"]);
    }
    if (j.contains("types") && !j["types"].is_null()) {
      for (const auto& item : j["types"].as_array()) {
        out.types.push_back(DataTypeOutFromJson(item));
      }
    }
    return out;
  }

  static sfmapi::OperationsContractOut OperationsContractOutFromJson(
      const Json& j) {
    sfmapi::OperationsContractOut out;
    out.contract = OptionalString(j, "contract");
    if (j.contains("contract_schema_version")) {
      out.contract_schema_version =
          static_cast<std::int32_t>(j["contract_schema_version"].as_number());
    }
    if (j.contains("operations") && !j["operations"].is_null()) {
      for (const auto& item : j["operations"].as_array()) {
        out.operations.push_back(OperationOutFromJson(item));
      }
    }
    if (j.contains("compatibility")) {
      out.compatibility = StringMapFromJson(j["compatibility"]);
    }
    return out;
  }

  static sfmapi::ProcessorsContractOut ProcessorsContractOutFromJson(
      const Json& j) {
    sfmapi::ProcessorsContractOut out;
    out.contract = OptionalString(j, "contract");
    if (j.contains("contract_schema_version")) {
      out.contract_schema_version =
          static_cast<std::int32_t>(j["contract_schema_version"].as_number());
    }
    if (j.contains("processors") && !j["processors"].is_null()) {
      for (const auto& item : j["processors"].as_array()) {
        out.processors.push_back(ProcessorOutFromJson(item));
      }
    }
    if (j.contains("rules")) out.rules = StringMapFromJson(j["rules"]);
    return out;
  }

  static sfmapi::PipelinesContractOut PipelinesContractOutFromJson(
      const Json& j) {
    sfmapi::PipelinesContractOut out;
    out.contract = OptionalString(j, "contract");
    if (j.contains("contract_schema_version")) {
      out.contract_schema_version =
          static_cast<std::int32_t>(j["contract_schema_version"].as_number());
    }
    out.composition_rule = OptionalString(j, "composition_rule");
    if (j.contains("initial_inputs") && !j["initial_inputs"].is_null()) {
      out.initial_inputs = StringArrayFromJson(j["initial_inputs"]);
    }
    if (j.contains("canonical_pipelines")) {
      out.canonical_pipelines = StringListMapFromJson(j["canonical_pipelines"]);
    }
    if (j.contains("plugin_pipelines") && !j["plugin_pipelines"].is_null()) {
      for (const auto& item : j["plugin_pipelines"].as_array()) {
        out.plugin_pipelines.push_back(PipelineDefinitionOutFromJson(item));
      }
    }
    if (j.contains("step_schema") && !j["step_schema"].is_null()) {
      out.step_schema_json = j["step_schema"].Dump();
    }
    if (j.contains("validation_reasons") &&
        !j["validation_reasons"].is_null()) {
      out.validation_reasons = StringArrayFromJson(j["validation_reasons"]);
    }
    return out;
  }

  static sfmapi::AttributesContractOut ParseAttributesContract(
      const HttpResponse& resp) {
    return AttributesContractOutFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::DataTypesContractOut ParseDataTypesContract(
      const HttpResponse& resp) {
    return DataTypesContractOutFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::OperationsContractOut ParseOperationsContract(
      const HttpResponse& resp) {
    return OperationsContractOutFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::ProcessorsContractOut ParseProcessorsContract(
      const HttpResponse& resp) {
    return ProcessorsContractOutFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::PipelinesContractOut ParsePipelinesContract(
      const HttpResponse& resp) {
    return PipelinesContractOutFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::ArtifactKind ArtifactKindFromJson(const Json& j) {
    sfmapi::ArtifactKind out;
    if (j.contains("kind")) out.kind = j["kind"].as_string();
    if (j.contains("datatype") && !j["datatype"].is_null()) {
      out.datatype = j["datatype"].as_string();
    }
    if (j.contains("title")) out.title = j["title"].as_string();
    if (j.contains("description")) out.description = j["description"].as_string();
    if (j.contains("durable")) out.durable = j["durable"].as_bool();
    if (j.contains("artifact_format") && !j["artifact_format"].is_null()) {
      out.artifact_format = j["artifact_format"].as_string();
    }
    if (j.contains("schema_version") && !j["schema_version"].is_null()) {
      out.schema_version = static_cast<std::int32_t>(j["schema_version"].as_number());
    }
    return out;
  }

  static sfmapi::ArtifactKind ParseArtifactKind(const HttpResponse& resp) {
    return ArtifactKindFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static Page<sfmapi::ArtifactKind> ParseArtifactKindPage(
      const HttpResponse& resp) {
    return ParsePage<sfmapi::ArtifactKind>(
        resp, [](const Json& item) { return ArtifactKindFromJson(item); });
  }

  static sfmapi::ArtifactFormat ArtifactFormatFromJson(const Json& j) {
    sfmapi::ArtifactFormat out;
    if (j.contains("format_id")) out.format_id = j["format_id"].as_string();
    if (j.contains("datatype")) out.datatype = j["datatype"].as_string();
    if (j.contains("title")) out.title = j["title"].as_string();
    if (j.contains("description")) out.description = j["description"].as_string();
    if (j.contains("schema_version") && !j["schema_version"].is_null()) {
      out.schema_version = static_cast<std::int32_t>(j["schema_version"].as_number());
    }
    if (j.contains("media_types") && j["media_types"].is_array()) {
      for (const auto& item : j["media_types"].as_array()) {
        out.media_types.push_back(item.as_string());
      }
    }
    if (j.contains("json_schema") && !j["json_schema"].is_null()) {
      out.json_schema_json = j["json_schema"].Dump();
    }
    if (j.contains("examples") && !j["examples"].is_null()) {
      out.examples_json = j["examples"].Dump();
    }
    if (j.contains("portable")) out.portable = j["portable"].as_bool();
    return out;
  }

  static sfmapi::ArtifactFormat ParseArtifactFormat(const HttpResponse& resp) {
    return ArtifactFormatFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static Page<sfmapi::ArtifactFormat> ParseArtifactFormatPage(
      const HttpResponse& resp) {
    return ParsePage<sfmapi::ArtifactFormat>(
        resp, [](const Json& item) { return ArtifactFormatFromJson(item); });
  }

  static sfmapi::ArtifactConversionStep ArtifactConversionStepFromJson(
      const Json& j) {
    sfmapi::ArtifactConversionStep out;
    if (j.contains("contract_id") && !j["contract_id"].is_null()) {
      out.contract_id = j["contract_id"].as_string();
    }
    if (j.contains("backend") && !j["backend"].is_null()) {
      out.backend = j["backend"].as_string();
    }
    if (j.contains("provider") && !j["provider"].is_null()) {
      out.provider = j["provider"].as_string();
    }
    if (j.contains("from_format")) out.from_format = j["from_format"].as_string();
    if (j.contains("to_format")) out.to_format = j["to_format"].as_string();
    if (j.contains("lossless")) out.lossless = j["lossless"].as_bool();
    if (j.contains("description") && !j["description"].is_null()) {
      out.description = j["description"].as_string();
    }
    return out;
  }

  static sfmapi::ArtifactConversionPlan ArtifactConversionPlanFromJson(
      const Json& j) {
    sfmapi::ArtifactConversionPlan out;
    if (j.contains("artifact_id")) out.artifact_id = j["artifact_id"].as_string();
    if (j.contains("source_format") && !j["source_format"].is_null()) {
      out.source_format = j["source_format"].as_string();
    }
    if (j.contains("target_format")) out.target_format = j["target_format"].as_string();
    if (j.contains("conversion_required")) {
      out.conversion_required = j["conversion_required"].as_bool();
    }
    if (j.contains("executable")) out.executable = j["executable"].as_bool();
    if (j.contains("reason") && !j["reason"].is_null()) {
      out.reason = j["reason"].as_string();
    }
    if (j.contains("steps") && j["steps"].is_array()) {
      for (const auto& item : j["steps"].as_array()) {
        out.steps.push_back(ArtifactConversionStepFromJson(item));
      }
    }
    return out;
  }

  static sfmapi::ArtifactConversionPlan ParseArtifactConversionPlan(
      const HttpResponse& resp) {
    return ArtifactConversionPlanFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::ArtifactValidationIssue ArtifactValidationIssueFromJson(
      const Json& j) {
    sfmapi::ArtifactValidationIssue out;
    if (j.contains("level")) out.level = j["level"].as_string();
    if (j.contains("field") && !j["field"].is_null()) {
      out.field = j["field"].as_string();
    }
    if (j.contains("message")) out.message = j["message"].as_string();
    return out;
  }

  static sfmapi::ArtifactValidation ArtifactValidationFromJson(const Json& j) {
    sfmapi::ArtifactValidation out;
    if (j.contains("artifact_id")) out.artifact_id = j["artifact_id"].as_string();
    if (j.contains("valid")) out.valid = j["valid"].as_bool();
    if (j.contains("artifact_format") && !j["artifact_format"].is_null()) {
      out.artifact_format = j["artifact_format"].as_string();
    }
    if (j.contains("datatype") && !j["datatype"].is_null()) {
      out.datatype = j["datatype"].as_string();
    }
    if (j.contains("checked_content")) {
      out.checked_content = j["checked_content"].as_bool();
    }
    if (j.contains("issues") && j["issues"].is_array()) {
      for (const auto& item : j["issues"].as_array()) {
        out.issues.push_back(ArtifactValidationIssueFromJson(item));
      }
    }
    return out;
  }

  static sfmapi::ArtifactValidation ParseArtifactValidation(
      const HttpResponse& resp) {
    return ArtifactValidationFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::StageArtifact StageArtifactFromJson(const Json& j) {
    sfmapi::StageArtifact out;
    if (j.contains("artifact_id")) out.artifact_id = j["artifact_id"].as_string();
    if (j.contains("job_id")) out.job_id = j["job_id"].as_string();
    if (j.contains("task_id")) out.task_id = j["task_id"].as_string();
    if (j.contains("recon_id") && !j["recon_id"].is_null()) {
      out.recon_id = j["recon_id"].as_string();
    }
    if (j.contains("dataset_id") && !j["dataset_id"].is_null()) {
      out.dataset_id = j["dataset_id"].as_string();
    }
    if (j.contains("kind")) out.kind = j["kind"].as_string();
    if (j.contains("name") && !j["name"].is_null()) {
      out.name = j["name"].as_string();
    }
    if (j.contains("uri") && !j["uri"].is_null()) {
      out.uri = j["uri"].as_string();
    }
    if (j.contains("media_type") && !j["media_type"].is_null()) {
      out.media_type = j["media_type"].as_string();
    }
    if (j.contains("artifact_format") && !j["artifact_format"].is_null()) {
      out.artifact_format = j["artifact_format"].as_string();
    }
    if (j.contains("datatype") && !j["datatype"].is_null()) {
      out.datatype = j["datatype"].as_string();
    }
    if (j.contains("schema_version") && !j["schema_version"].is_null()) {
      out.schema_version = static_cast<std::int32_t>(j["schema_version"].as_number());
    }
    if (j.contains("files") && !j["files"].is_null()) {
      out.files_json = j["files"].Dump();
    }
    if (j.contains("sha256") && !j["sha256"].is_null()) {
      out.sha256 = j["sha256"].as_string();
    }
    if (j.contains("byte_size") && !j["byte_size"].is_null()) {
      out.byte_size = static_cast<std::int64_t>(j["byte_size"].as_number());
    }
    if (j.contains("coordinate_frame") && !j["coordinate_frame"].is_null()) {
      out.coordinate_frame = j["coordinate_frame"].as_string();
    }
    if (j.contains("producer") && !j["producer"].is_null()) {
      out.producer_json = j["producer"].Dump();
    }
    if (j.contains("summary") && !j["summary"].is_null()) {
      out.summary_json = j["summary"].Dump();
    }
    if (j.contains("metadata") && !j["metadata"].is_null()) {
      out.metadata_json = j["metadata"].Dump();
    }
    if (j.contains("_links") && !j["_links"].is_null()) {
      out.links_json = j["_links"].Dump();
    }
    if (j.contains("created_at")) out.created_at = j["created_at"].as_string();
    return out;
  }

  static sfmapi::StageArtifact ParseStageArtifact(const HttpResponse& resp) {
    return StageArtifactFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static Page<sfmapi::StageArtifact> ParseStageArtifactPage(
      const HttpResponse& resp) {
    return ParsePage<sfmapi::StageArtifact>(
        resp, [](const Json& item) { return StageArtifactFromJson(item); });
  }

  // ----- generic JSON-body decoders for resource shapes ------------
  //  These are the C++ analogues of Python Pydantic validation +
  //  TypeScript interface assignment: read a JSON value and populate
  //  a typed POD struct. Fields absent from the body keep their POD
  //  defaults so partial responses don't crash.

  static sfmapi::Project ProjectFromJson(const Json& j) {
    sfmapi::Project out;
    if (j.contains("project_id")) out.project_id = j["project_id"].as_string();
    if (j.contains("tenant_id")) out.tenant_id = j["tenant_id"].as_string();
    if (j.contains("name")) out.name = j["name"].as_string();
    if (j.contains("description") && !j["description"].is_null()) {
      out.description = j["description"].as_string();
    }
    if (j.contains("created_at")) out.created_at = j["created_at"].as_string();
    return out;
  }

  static sfmapi::Project ParseProject(const HttpResponse& resp) {
    return ProjectFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::Dataset DatasetFromJson(const Json& j) {
    sfmapi::Dataset out;
    if (j.contains("dataset_id")) out.dataset_id = j["dataset_id"].as_string();
    if (j.contains("tenant_id")) out.tenant_id = j["tenant_id"].as_string();
    if (j.contains("project_id")) out.project_id = j["project_id"].as_string();
    if (j.contains("source_id") && !j["source_id"].is_null()) {
      out.source_id = j["source_id"].as_string();
    }
    if (j.contains("name")) out.name = j["name"].as_string();
    if (j.contains("camera_model")) out.camera_model = j["camera_model"].as_string();
    if (j.contains("intrinsics_mode")) {
      out.intrinsics_mode = j["intrinsics_mode"].as_string();
    }
    if (j.contains("is_spherical")) out.is_spherical = j["is_spherical"].as_bool();
    if (j.contains("respect_exif_orientation")) {
      out.respect_exif_orientation = j["respect_exif_orientation"].as_bool();
    }
    if (j.contains("active_maskset_id") && !j["active_maskset_id"].is_null()) {
      out.active_maskset_id = j["active_maskset_id"].as_string();
    }
    if (j.contains("manifest_hash") && !j["manifest_hash"].is_null()) {
      out.manifest_hash = j["manifest_hash"].as_string();
    }
    if (j.contains("created_at")) out.created_at = j["created_at"].as_string();
    return out;
  }

  static sfmapi::Dataset ParseDataset(const HttpResponse& resp) {
    return DatasetFromJson(
        Json::Parse(std::string(resp.body.begin(), resp.body.end())));
  }

  static sfmapi::TaskRow TaskRowFromJson(const Json& j) {
    sfmapi::TaskRow out;
    if (j.contains("task_id")) out.task_id = j["task_id"].as_string();
    if (j.contains("job_id")) out.job_id = j["job_id"].as_string();
    if (j.contains("kind")) out.kind = j["kind"].as_string();
    if (j.contains("status")) out.status = j["status"].as_string();
    if (j.contains("provider") && !j["provider"].is_null()) {
      out.provider = j["provider"].as_string();
    }
    if (j.contains("cache_key")) out.cache_key = j["cache_key"].as_string();
    if (j.contains("inputs_hash")) out.inputs_hash = j["inputs_hash"].as_string();
    if (j.contains("params_hash")) out.params_hash = j["params_hash"].as_string();
    if (j.contains("outputs_ref") && !j["outputs_ref"].is_null()) {
      out.outputs_ref_json = j["outputs_ref"].Dump();
    }
    return out;
  }

  static sfmapi::JobDetail JobDetailFromJson(const Json& j) {
    sfmapi::JobDetail out;
    if (j.contains("job_id")) out.job_id = j["job_id"].as_string();
    if (j.contains("tenant_id")) out.tenant_id = j["tenant_id"].as_string();
    if (j.contains("project_id")) out.project_id = j["project_id"].as_string();
    if (j.contains("recipe")) out.recipe = j["recipe"].as_string();
    if (j.contains("status")) out.status = j["status"].as_string();
    if (j.contains("cancel_requested")) {
      out.cancel_requested = j["cancel_requested"].as_bool();
    }
    if (j.contains("cancel_force")) {
      out.cancel_force = j["cancel_force"].as_bool();
    }
    if (j.contains("created_at")) out.created_at = j["created_at"].as_string();
    if (j.contains("started_at") && !j["started_at"].is_null()) {
      out.started_at = j["started_at"].as_string();
    }
    if (j.contains("finished_at") && !j["finished_at"].is_null()) {
      out.finished_at = j["finished_at"].as_string();
    }
    if (j.contains("error_class") && !j["error_class"].is_null()) {
      out.error_class = j["error_class"].as_string();
    }
    if (j.contains("error_message") && !j["error_message"].is_null()) {
      out.error_message = j["error_message"].as_string();
    }
    if (j.contains("tasks") && j["tasks"].is_array()) {
      for (const auto& t : j["tasks"].as_array()) {
        out.tasks.push_back(TaskRowFromJson(t));
      }
    }
    return out;
  }

  static sfmapi::HealthResponse ParseHealthResponse(const HttpResponse& resp) {
    auto j = Json::Parse(std::string(resp.body.begin(), resp.body.end()));
    sfmapi::HealthResponse out;
    if (j.contains("status")) out.status = j["status"].as_string();
    return out;
  }

  static sfmapi::VersionResponse ParseVersionResponse(const HttpResponse& resp) {
    auto j = Json::Parse(std::string(resp.body.begin(), resp.body.end()));
    sfmapi::VersionResponse out;
    if (j.contains("sfmapi")) out.sfmapi = j["sfmapi"].as_string();
    if (j.contains("backend") && !j["backend"].is_null()) {
      auto& jb = j["backend"];
      sfmapi::BackendVersion bv;
      if (jb.contains("name")) bv.name = jb["name"].as_string();
      if (jb.contains("version")) bv.version = jb["version"].as_string();
      if (jb.contains("vendor") && !jb["vendor"].is_null()) {
        bv.vendor = jb["vendor"].as_string();
      }
      if (jb.contains("runtime_versions")) {
        for (auto& kv : jb["runtime_versions"].as_object()) {
          bv.runtime_versions[kv.first] = kv.second.as_string();
        }
      }
      out.backend = bv;
    }
    return out;
  }

  /// Decode a Page<T> envelope. ``item_decode`` is a function that
  /// converts a single ``Json`` item to T.
  template <typename T>
  static Page<T> ParsePage(
      const HttpResponse& resp,
      const std::function<T(const Json&)>& item_decode) {
    auto j = Json::Parse(std::string(resp.body.begin(), resp.body.end()));
    Page<T> out;
    if (j.contains("items")) {
      for (const auto& item : j["items"].as_array()) {
        out.items.push_back(item_decode(item));
      }
    }
    if (j.contains("next_page_token") && !j["next_page_token"].is_null()) {
      out.next_page_token = j["next_page_token"].as_string();
    }
    if (j.contains("total") && !j["total"].is_null()) {
      out.total = static_cast<std::int64_t>(j["total"].as_number());
    }
    return out;
  }

 private:
  static LocalizationResult LocalizationResultFromJson(const Json& j) {
    LocalizationResult out;
    if (j.contains("success")) out.success = j["success"].as_bool();
    if (j.contains("num_inliers")) {
      out.num_inliers = static_cast<std::int32_t>(j["num_inliers"].as_number());
    }
    if (j.contains("cam_from_world") && !j["cam_from_world"].is_null()) {
      const auto& cfw = j["cam_from_world"];
      Rigid3 r;
      if (cfw.contains("rotation")) {
        const auto& rot = cfw["rotation"];
        r.rotation.w = rot["w"].as_number();
        r.rotation.x = rot["x"].as_number();
        r.rotation.y = rot["y"].as_number();
        r.rotation.z = rot["z"].as_number();
      }
      if (cfw.contains("translation")) {
        const auto& t = cfw["translation"].as_array();
        for (std::size_t i = 0; i < 3 && i < t.size(); ++i) {
          r.translation[i] = t[i].as_number();
        }
      }
      out.cam_from_world = r;
    }
    if (j.contains("inlier_matches")) {
      for (const auto& pair : j["inlier_matches"].as_array()) {
        if (pair.is_array() && pair.as_array().size() >= 2) {
          out.inlier_matches.emplace_back(
              static_cast<std::int32_t>(pair[0].as_number()),
              static_cast<std::int64_t>(pair[1].as_number()));
        }
      }
    }
    return out;
  }

 public:

  // --- helpers / utility ------------------------------------------

  /// Raise on status >= 400. Returns the response unchanged on 2xx/3xx.
  /// Optional helper — most callers will want to call this on every
  /// response to centralize error handling.
  static HttpResponse RaiseOnError(HttpResponse resp) {
    if (resp.status >= 400) {
      // Best-effort: pull `capability` out of a problem+json body so
      // callers can switch on it. We don't depend on a JSON library
      // here — the body is whatever the server returned and the
      // caller can decode it themselves if richer info is needed.
      std::string body(resp.body.begin(), resp.body.end());
      auto pos = body.find("\"capability\":\"");
      std::string cap;
      if (pos != std::string::npos) {
        pos += std::string("\"capability\":\"").size();
        auto end = body.find('"', pos);
        if (end != std::string::npos) cap = body.substr(pos, end - pos);
      }
      throw HttpStatusError(resp.status, std::move(cap));
    }
    return resp;
  }

 private:
  ClientOptions opts_;

  HttpResponse Get(const std::string& path) const {
    HttpRequest req{"GET", opts_.base_url + path, {}, {}};
    AddAuth(req);
    return Send(req);
  }

  HttpResponse Post(const std::string& path, const std::string& body) const {
    HttpRequest req{
        "POST", opts_.base_url + path,
        {{"Content-Type", "application/json"}}, ToBytes(body)};
    AddAuth(req);
    return Send(req);
  }

  HttpResponse Delete(const std::string& path) const {
    HttpRequest req{"DELETE", opts_.base_url + path, {}, {}};
    AddAuth(req);
    return Send(req);
  }

  HttpResponse Send(HttpRequest req) const {
    for (const auto& kv : opts_.default_headers) {
      if (req.headers.find(kv.first) == req.headers.end()) {
        req.headers.insert(kv);
      }
    }
    return opts_.transport(req);
  }

  void AddAuth(HttpRequest& req) const {
    if (!opts_.api_key.empty() &&
        req.headers.find("Authorization") == req.headers.end()) {
      req.headers["Authorization"] = "Bearer " + opts_.api_key;
    }
  }

  static std::vector<std::uint8_t> ToBytes(const std::string& s) {
    return {s.begin(), s.end()};
  }

  static void AppendQueryParam(std::string& path, bool& first,
                               const std::string& name,
                               const std::string& value) {
    if (value.empty()) {
      return;
    }
    path += first ? "?" : "&";
    first = false;
    path += PercentEncodeQuery(name) + "=" + PercentEncodeQuery(value);
  }

  static bool IsQueryUnreserved(unsigned char c) {
    return std::isalnum(c) || c == '-' || c == '.' || c == '_' || c == '~';
  }

  static std::string PercentEncodeQuery(const std::string& value) {
    static constexpr char kHex[] = "0123456789ABCDEF";
    std::string out;
    out.reserve(value.size());
    for (unsigned char c : value) {
      if (IsQueryUnreserved(c)) {
        out.push_back(static_cast<char>(c));
      } else {
        out.push_back('%');
        out.push_back(kHex[c >> 4]);
        out.push_back(kHex[c & 0x0F]);
      }
    }
    return out;
  }

  static std::string JsonEscape(const std::string& s) {
    std::string out;
    out.reserve(s.size());
    for (char c : s) {
      switch (c) {
        case '"': out += "\\\""; break;
        case '\\': out += "\\\\"; break;
        case '\n': out += "\\n"; break;
        case '\r': out += "\\r"; break;
        case '\t': out += "\\t"; break;
        default: out += c;
      }
    }
    return out;
  }
};

}  // namespace sfmapi

#endif  // SFMAPI_CLIENT_HPP_
