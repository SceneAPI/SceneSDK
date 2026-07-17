// Smoke tests for the new sfmapi C++ extras: json.hpp, specs.hpp,
// sse.hpp, and the convenience methods on Client (UploadFile,
// SubmitMatchesSplit, GetLocalizationResult, ParseCapabilities,
// ParseJobSubmitResponse, ParseEventsBuffer).

#include <cstdio>
#include <cstring>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

#include "sfmapi/client.hpp"
#include "sfmapi/json.hpp"
#include "sfmapi/specs.hpp"
#include "sfmapi/sse.hpp"

#define CHECK(cond, msg)                                              \
  do {                                                                \
    if (!(cond)) {                                                    \
      std::fprintf(stderr, "FAIL: %s\n", msg);                        \
      std::fprintf(stderr, "  at %s:%d\n", __FILE__, __LINE__);       \
      std::exit(1);                                                   \
    }                                                                 \
  } while (0)

// ---- json.hpp ----------------------------------------------------------

static void TestJsonRoundTrip() {
  auto v = sfmapi::Json::Parse(
      R"({"name":"x","arr":[1,2.5,true,null,"s"],"nested":{"k":42}})");
  CHECK(v.is_object(), "top should be object");
  CHECK(v["name"].as_string() == "x", "name == x");
  CHECK(v["arr"].as_array().size() == 5, "arr size 5");
  CHECK(v["arr"][0].as_number() == 1.0, "arr[0] == 1");
  CHECK(v["arr"][1].as_number() == 2.5, "arr[1] == 2.5");
  CHECK(v["arr"][2].as_bool() == true, "arr[2] == true");
  CHECK(v["arr"][3].is_null(), "arr[3] null");
  CHECK(v["arr"][4].as_string() == "s", "arr[4] == 's'");
  CHECK(v["nested"]["k"].as_number() == 42.0, "nested.k == 42");

  std::string compact = v.Dump();
  auto v2 = sfmapi::Json::Parse(compact);
  CHECK(v2["nested"]["k"].as_number() == 42.0, "round-trip preserved");

  std::string pretty = v.Dump(2);
  CHECK(pretty.find('\n') != std::string::npos, "pretty has newlines");
  std::printf("  json round-trip OK\n");
}

static void TestJsonEscapes() {
  auto v = sfmapi::Json::Parse(R"({"k":"line1\nline2\t\"q\""})");
  CHECK(v["k"].as_string() == "line1\nline2\t\"q\"", "escape decoding");
  // Re-encode and re-parse
  std::string out = v.Dump();
  auto v2 = sfmapi::Json::Parse(out);
  CHECK(v2["k"].as_string() == "line1\nline2\t\"q\"", "escape round-trip");
  std::printf("  json escapes OK\n");
}

static void TestJsonNumbers() {
  auto v = sfmapi::Json::Parse(R"([0,-1,1.5,1e3,-2.5e-2])");
  const auto& a = v.as_array();
  CHECK(a[0].as_number() == 0.0, "0");
  CHECK(a[1].as_number() == -1.0, "-1");
  CHECK(a[2].as_number() == 1.5, "1.5");
  CHECK(a[3].as_number() == 1000.0, "1e3");
  CHECK(a[4].as_number() < 0 && a[4].as_number() > -0.05, "-2.5e-2");
  std::printf("  json numbers OK\n");
}

static void TestJsonErrors() {
  bool threw = false;
  try { sfmapi::Json::Parse("{not json"); } catch (const sfmapi::JsonError&) { threw = true; }
  CHECK(threw, "bad JSON should throw");

  threw = false;
  try {
    const auto v = sfmapi::Json::Parse(R"({"a":1})");
    (void)v["missing"];  // const op[] throws on missing
  } catch (const sfmapi::JsonError&) { threw = true; }
  CHECK(threw, "missing key (const access) should throw");
  std::printf("  json errors OK\n");
}

static void TestJsonBuilder() {
  sfmapi::Json obj{{"x", 1}, {"y", "hi"}};
  obj["z"] = sfmapi::Json::Array{1, 2, 3};
  std::string out = obj.Dump();
  auto v = sfmapi::Json::Parse(out);
  CHECK(v["x"].as_number() == 1.0, "builder x");
  CHECK(v["y"].as_string() == "hi", "builder y");
  CHECK(v["z"].as_array().size() == 3, "builder z");
  std::printf("  json builder OK\n");
}

// ---- specs.hpp ---------------------------------------------------------

static void TestSpecs() {
  sfmapi::FeaturesSpec fs;
  fs.type = sfmapi::kFeatureTypeSuperPoint;
  fs.provider = "hloc";
  fs.max_num_features = 4096;
  fs.backend_options["SuperPoint.max_keypoints"] = 4096;
  auto fs_json = sfmapi::Json::Parse(fs.ToJsonString());
  CHECK(fs_json["type"].as_string() == "superpoint", "features.type");
  CHECK(fs_json["provider"].as_string() == "hloc", "features.provider");
  CHECK(fs_json["max_num_features"].as_number() == 4096, "features.max_num");
  CHECK(fs_json["backend_options"]["SuperPoint.max_keypoints"].as_number() == 4096,
        "features.backend_options");
  CHECK(!fs_json.contains("extractor_options"), "features has no stale extractor_options");
  CHECK(fs_json["version"].as_number() == 1, "features.version");

  sfmapi::PairsSpec ps;
  ps.strategy = sfmapi::kPairExplicit;
  ps.retrieval_strategy = "vlad";
  ps.retrieval_k = 30;
  ps.image_pairs.push_back({"a.jpg", "b.jpg"});
  ps.pairs_blob_sha = std::string(64, 'a');
  auto ps_json = sfmapi::Json::Parse(ps.ToJsonString());
  CHECK(ps_json["strategy"].as_string() == "explicit", "pairs.strategy");
  CHECK(ps_json["retrieval_k"].as_number() == 30, "pairs.k");
  CHECK(ps_json["image_pairs"].as_array().size() == 1, "pairs image_pairs");
  CHECK(ps_json["image_pairs"][0]["image_name1"].as_string() == "a.jpg",
        "pairs image_name1");
  CHECK(ps_json["pairs_blob_sha"].as_string() == std::string(64, 'a'),
        "pairs blob sha");
  CHECK(ps_json["pairs_blob_format"].as_string() == "image_name_pairs_txt",
        "pairs blob format");
  CHECK(!ps_json.contains("vocab_tree_path"), "optional omitted when nullopt");

  sfmapi::MatcherSpec ms;
  ms.type = sfmapi::kMatcherLightGlue;
  ms.backend_options["LightGlue.depth_confidence"] = 0.9;
  sfmapi::ArtifactRef features_ref;
  features_ref.artifact_id = "01HZARTIFACT000000000000";
  features_ref.kind = "features.database";
  ms.input_artifacts["features"] = features_ref;
  auto ms_json = sfmapi::Json::Parse(ms.ToJsonString());
  CHECK(ms_json["type"].as_string() == "lightglue", "matcher.type");
  CHECK(ms_json["backend_options"]["LightGlue.depth_confidence"].as_number() == 0.9,
        "matcher.backend_options");
  CHECK(!ms_json.contains("matcher_options"), "matcher has no stale matcher_options");
  CHECK(ms_json["input_artifacts"]["features"]["artifact_id"].as_string() ==
            "01HZARTIFACT000000000000",
        "matcher input_artifacts artifact_id");
  CHECK(ms_json["input_artifacts"]["features"]["kind"].as_string() ==
            "features.database",
        "matcher input_artifacts kind");

  sfmapi::BundleAdjustmentSpec ba;
  ba.mode = sfmapi::kBaModeFeaturemetric;
  ba.loss_kernel = sfmapi::kBaLossHuber;
  auto ba_json = sfmapi::Json::Parse(ba.ToJsonString());
  CHECK(ba_json["mode"].as_string() == "featuremetric", "ba.mode");
  CHECK(ba_json["loss_kernel"].as_string() == "huber", "ba.loss");

  sfmapi::IncrementalSpec inc;
  inc.init_image_pair = std::make_pair(std::string("a.jpg"), std::string("b.jpg"));
  inc.max_runtime_seconds = 600;
  auto inc_json = sfmapi::Json::Parse(inc.ToJsonString());
  CHECK(inc_json["kind"].as_string() == "incremental", "inc.kind");
  CHECK(inc_json["init_image_pair"].as_array().size() == 2, "inc pair");
  CHECK(inc_json["init_image_pair"][0].as_string() == "a.jpg", "inc pair[0]");
  CHECK(inc_json["max_runtime_seconds"].as_number() == 600, "inc max_rt");
  CHECK(inc_json["ba_global_use_pba"].as_bool() == true, "inc pba default");

  sfmapi::GlobalSpec global;
  global.max_runtime_seconds = 900;
  auto global_json = sfmapi::Json::Parse(global.ToJsonString());
  CHECK(global_json["kind"].as_string() == "global", "global.kind");
  CHECK(global_json["max_runtime_seconds"].as_number() == 900, "global max_rt");
  CHECK(global_json["snapshot_frames_freq"].as_number() == 50, "global snapshot freq");

  sfmapi::HierarchicalSpec hierarchical;
  hierarchical.max_runtime_seconds = 1200;
  auto hierarchical_json = sfmapi::Json::Parse(hierarchical.ToJsonString());
  CHECK(hierarchical_json["kind"].as_string() == "hierarchical", "hier.kind");
  CHECK(hierarchical_json["max_runtime_seconds"].as_number() == 1200, "hier max_rt");

  sfmapi::SphericalSpec sp;
  sp.max_runtime_seconds = 300;
  auto sp_json = sfmapi::Json::Parse(sp.ToJsonString());
  CHECK(sp_json["kind"].as_string() == "spherical", "sp.kind");
  CHECK(sp_json["panorama"].as_bool() == true, "sp.panorama default");
  CHECK(sp_json["max_runtime_seconds"].as_number() == 300, "sp max_rt");
  CHECK(sp_json["snapshot_frames_freq"].as_number() == 50, "sp snapshot freq");

  sfmapi::ProcessorPipelineStep proc_step;
  proc_step.processor = "features";
  proc_step.ref = "feat";
  proc_step.provider = "hloc";
  proc_step.attributes["type"] = "superpoint";
  proc_step.wires["images"] = "input.images";
  sfmapi::PipelineValidateRequest validate_req;
  validate_req.initial_inputs.push_back("images");
  validate_req.AddStep(proc_step);
  auto validate_json = sfmapi::Json::Parse(validate_req.ToJsonString());
  CHECK(validate_json["initial_inputs"].as_array()[0].as_string() == "images",
        "validate initial input");
  CHECK(validate_json["steps"].as_array()[0]["processor"].as_string() == "features",
        "processor pipeline step");
  CHECK(validate_json["steps"].as_array()[0]["attributes"]["type"].as_string() ==
            "superpoint",
        "processor attributes");
  CHECK(validate_json["steps"].as_array()[0]["wires"]["images"].as_string() ==
            "input.images",
        "processor wires");

  sfmapi::PipelineRunRequest run_req;
  run_req.dataset_id = "01HZDATASET0000000000000";
  sfmapi::PipelineStep legacy_step;
  legacy_step.op = "map";
  legacy_step.params["quality"] = "draft";
  run_req.AddStep(legacy_step);
  auto run_json = sfmapi::Json::Parse(run_req.ToJsonString());
  CHECK(run_json["dataset_id"].as_string() == "01HZDATASET0000000000000",
        "run dataset_id");
  CHECK(run_json["steps"].as_array()[0]["op"].as_string() == "map",
        "legacy pipeline step");

  std::printf("  specs ToJson OK\n");
}

static void TestArtifactDecoders() {
  auto make_json = [](int status, std::string body) {
    sfmapi::HttpResponse r;
    r.status = status;
    r.headers["content-type"] = "application/json";
    r.body.assign(body.begin(), body.end());
    return r;
  };

  auto kind_resp = make_json(
      200,
      R"({"items":[{"kind":"features.database","datatype":"feature_set","title":"Feature database","description":"COLMAP database","durable":true,"artifact_format":"sfmapi.features.colmap_db.v1","schema_version":1}],"next_page_token":null})");
  auto kinds = sfmapi::Client::ParseArtifactKindPage(kind_resp);
  CHECK(kinds.items.size() == 1, "artifact kind page item");
  CHECK(kinds.items[0].kind == "features.database", "artifact kind");
  CHECK(kinds.items[0].durable, "artifact kind durable");
  CHECK(kinds.items[0].datatype == "feature_set", "artifact kind datatype");
  CHECK(kinds.items[0].artifact_format == "sfmapi.features.colmap_db.v1",
        "artifact kind format");

  auto artifact_resp = make_json(
      200,
      R"({"artifact_id":"01HZARTIFACT000000000000","job_id":"01HZJOB000000000000000000","task_id":"01HZTASK0000000000000000A","recon_id":null,"dataset_id":"01HZDATASET0000000000000","kind":"features.database","name":"database","uri":"/v1/artifacts/01HZARTIFACT000000000000/content","media_type":"application/vnd.sqlite3","artifact_format":"sfmapi.features.colmap_db.v1","datatype":"feature_set","schema_version":1,"files":[{"name":"database.db","uri":"/v1/artifacts/01HZARTIFACT000000000000/content","sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","byte_size":12}],"sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","byte_size":12,"coordinate_frame":"world","producer":{"provider":"colmap"},"summary":{"num_images":2},"metadata":{"backend":"colmap"},"created_at":"2026-05-10T00:00:00Z","_links":{"self":{"href":"/v1/artifacts/01HZARTIFACT000000000000"}}})");
  auto artifact = sfmapi::Client::ParseStageArtifact(artifact_resp);
  CHECK(artifact.artifact_id == "01HZARTIFACT000000000000", "artifact_id");
  CHECK(artifact.kind == "features.database", "artifact kind");
  CHECK(artifact.dataset_id == "01HZDATASET0000000000000", "artifact dataset");
  CHECK(artifact.uri == "/v1/artifacts/01HZARTIFACT000000000000/content",
        "artifact uri");
  CHECK(artifact.artifact_format == "sfmapi.features.colmap_db.v1",
        "artifact format");
  CHECK(artifact.datatype == "feature_set", "artifact datatype");
  CHECK(artifact.schema_version && *artifact.schema_version == 1,
        "artifact schema_version");
  CHECK(artifact.files_json.find("database.db") != std::string::npos,
        "artifact files json");
  CHECK(artifact.sha256 == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "artifact sha256");
  CHECK(artifact.byte_size && *artifact.byte_size == 12, "artifact byte size");
  CHECK(artifact.coordinate_frame == "world", "artifact coordinate frame");
  CHECK(artifact.producer_json.find("colmap") != std::string::npos,
        "artifact producer json");
  CHECK(artifact.summary_json.find("num_images") != std::string::npos,
        "artifact summary json");
  CHECK(artifact.metadata_json.find("colmap") != std::string::npos,
        "artifact metadata json");
  CHECK(artifact.links_json.find("/v1/artifacts/") != std::string::npos,
        "artifact links json");

  auto artifact_page = make_json(
      200,
      R"({"items":[{"artifact_id":"01HZARTIFACT000000000000","job_id":"01HZJOB000000000000000000","task_id":"01HZTASK0000000000000000A","kind":"matches.raw","created_at":"2026-05-10T00:00:00Z"}],"next_page_token":"next"})");
  auto page = sfmapi::Client::ParseStageArtifactPage(artifact_page);
  CHECK(page.items.size() == 1, "artifact page item");
  CHECK(page.items[0].kind == "matches.raw", "artifact page kind");
  CHECK(page.next_page_token == "next", "artifact page token");

  auto formats_resp = make_json(
      200,
      R"({"items":[{"format_id":"sfmapi.features.local.v1","datatype":"feature_set","title":"Local features","description":"Portable local features","schema_version":1,"media_types":["application/json"],"json_schema":{"type":"object"},"examples":[{"features":[]}],"portable":true}],"next_page_token":null})");
  auto formats = sfmapi::Client::ParseArtifactFormatPage(formats_resp);
  CHECK(formats.items.size() == 1, "artifact format page item");
  CHECK(formats.items[0].format_id == "sfmapi.features.local.v1",
        "artifact format id");
  CHECK(formats.items[0].media_types.size() == 1, "artifact media type list");
  CHECK(formats.items[0].json_schema_json.find("object") != std::string::npos,
        "artifact format schema json");

  auto plan_resp = make_json(
      200,
      R"({"artifact_id":"a1","source_format":"sfmapi.features.colmap_db.v1","target_format":"sfmapi.features.local.v1","conversion_required":true,"executable":true,"reason":null,"steps":[{"contract_id":"c1","backend":"hloc","provider":"hloc","from_format":"sfmapi.features.colmap_db.v1","to_format":"sfmapi.features.local.v1","lossless":true,"description":"export"}]})");
  auto plan = sfmapi::Client::ParseArtifactConversionPlan(plan_resp);
  CHECK(plan.executable, "artifact conversion executable");
  CHECK(plan.steps.size() == 1, "artifact conversion step");
  CHECK(plan.steps[0].provider == "hloc", "artifact conversion provider");

  auto validation_resp = make_json(
      200,
      R"({"artifact_id":"a1","valid":false,"artifact_format":"sfmapi.features.local.v1","datatype":"feature_set","checked_content":true,"issues":[{"level":"error","field":"files[0]","message":"missing"}]})");
  auto validation = sfmapi::Client::ParseArtifactValidation(validation_resp);
  CHECK(!validation.valid, "artifact validation valid");
  CHECK(validation.checked_content, "artifact validation checked content");
  CHECK(validation.issues.size() == 1, "artifact validation issue");
  CHECK(validation.issues[0].field == "files[0]", "artifact validation field");
  std::printf("  artifact decoders OK\n");
}

static void TestDataflowContractDecoders() {
  auto make_json = [](int status, std::string body) {
    sfmapi::HttpResponse r;
    r.status = status;
    r.headers["content-type"] = "application/json";
    r.body.assign(body.begin(), body.end());
    return r;
  };

  auto attributes = sfmapi::Client::ParseAttributesContract(make_json(
      200,
      R"({"contract":"attributes","contract_schema_version":1,)"
      R"("attribute_types":["string","integer"],)"
      R"("rules":{"required":"must be supplied"}})"));
  CHECK(attributes.contract == "attributes", "attributes contract");
  CHECK(attributes.attribute_types.size() == 2, "attribute types");
  CHECK(attributes.rules["required"] == "must be supplied", "attribute rules");

  auto datatypes = sfmapi::Client::ParseDataTypesContract(make_json(
      200,
      R"({"contract":"datatypes","contract_schema_version":1,)"
      R"("kinds":["core"],"types":[{"type_id":"feature_set",)"
      R"("title":"Feature set","kind":"core","aliases":["features"],)"
      R"("description":"Local features"}]})"));
  CHECK(datatypes.types.size() == 1, "datatype item");
  CHECK(datatypes.types[0].type_id == "feature_set", "datatype id");
  CHECK(datatypes.types[0].aliases[0] == "features", "datatype alias");

  auto operations = sfmapi::Client::ParseOperationsContract(make_json(
      200,
      R"({"contract":"operations","contract_schema_version":1,)"
      R"("operations":[{"op_id":"features","title":"Features",)"
      R"("consumes":["image_sequence"],"produces":["feature_set"],)"
      R"("capabilities":["features.extract"],"config_stage":"features",)"
      R"("description":"extract"}],)"
      R"("compatibility":{"operation":"legacy"}})"));
  CHECK(operations.operations.size() == 1, "operation item");
  CHECK(operations.operations[0].produces[0] == "feature_set",
        "operation produces");
  CHECK(operations.compatibility["operation"] == "legacy",
        "operation compatibility");

  auto processors = sfmapi::Client::ParseProcessorsContract(make_json(
      200,
      R"({"contract":"processors","contract_schema_version":1,)"
      R"("processors":[{"processor_id":"features","title":"Features",)"
      R"("consumer":{"images":{"datatype":"image_sequence",)"
      R"("required":true,"multiple":false,"description":"images"}},)"
      R"("supplier":{"features":{"datatype":"feature_set",)"
      R"("required":true,"multiple":false,"description":"features"}},)"
      R"("attributes":[{"name":"type","type":"string","required":true,)"
      R"("description":"extractor","default":"sift","enum":["sift"]}],)"
      R"("special_inputs":{},"special_attributes":[],)"
      R"("capabilities":["features.extract"],"config_stage":"features",)"
      R"("aliases":["extract"],"description":"extract"}],)"
      R"("rules":{"composition":"datatype match"}})"));
  CHECK(processors.processors.size() == 1, "processor item");
  CHECK(processors.processors[0].consumer["images"].datatype ==
            "image_sequence",
        "processor consumer");
  CHECK(processors.processors[0].attributes[0].default_json == "\"sift\"",
        "processor attribute default");

  auto pipelines = sfmapi::Client::ParsePipelinesContract(make_json(
      200,
      R"({"contract":"pipelines","contract_schema_version":1,)"
      R"("composition_rule":"supplier datatype must match consumer datatype",)"
      R"("initial_inputs":["image_sequence"],)"
      R"("canonical_pipelines":{"incremental":["features","map"]},)"
      R"("plugin_pipelines":[{"pipeline_id":"radiance","title":"Radiance",)"
      R"("aliases":["3dgs"],"initial_inputs":["sparse_model"],)"
      R"("steps":[{"ref":"train","processor":"radiance.train",)"
      R"("attributes":{"method":"gsplat"},)"
      R"("wires":{"model":"input.sparse_model"}}],)"
      R"("description":"train"}],)"
      R"("step_schema":{"type":"object"},)"
      R"("validation_reasons":["datatype_mismatch"]})"));
  CHECK(pipelines.canonical_pipelines["incremental"].size() == 2,
        "canonical pipeline");
  CHECK(pipelines.plugin_pipelines.size() == 1, "plugin pipeline");
  CHECK(pipelines.plugin_pipelines[0].steps[0].attributes_json.find("gsplat") !=
            std::string::npos,
        "pipeline step attributes");
  CHECK(pipelines.validation_reasons[0] == "datatype_mismatch",
        "pipeline validation reason");

  std::printf("  dataflow contract decoders OK\n");
}

// ---- sse.hpp -----------------------------------------------------------

static void TestSseParse() {
  std::string body =
      "id: 1\n"
      "event: progress\n"
      "data: {\"phase\":\"extract\",\"current\":5,\"total\":10}\n"
      "\n"
      ": this is a comment\n"
      "id: 2\n"
      "data: line1\n"
      "data: line2\n"
      "\n";
  auto events = sfmapi::ParseSseEvents(body);
  CHECK(events.size() == 2, "two events");
  CHECK(events[0].id == "1", "ev0 id");
  CHECK(events[0].event == "progress", "ev0 event");
  CHECK(events[0].data.find("phase") != std::string::npos, "ev0 data");
  CHECK(events[1].id == "2", "ev1 id");
  CHECK(events[1].data == "line1\nline2", "multi-line data joined");
  std::printf("  SSE parse OK\n");
}

static void TestSseCrLf() {
  std::string body =
      "id: 7\r\n"
      "event: msg\r\n"
      "data: hello\r\n"
      "\r\n";
  auto events = sfmapi::ParseSseEvents(body);
  CHECK(events.size() == 1, "1 event from CRLF");
  CHECK(events[0].data == "hello", "data trimmed of CR");
  std::printf("  SSE CRLF OK\n");
}

// ---- Client convenience ------------------------------------------------

namespace {
struct Recorder {
  std::vector<sfmapi::HttpRequest> calls;
  std::function<sfmapi::HttpResponse(const sfmapi::HttpRequest&)> reply;

  sfmapi::HttpResponse operator()(sfmapi::HttpRequest req) {
    sfmapi::HttpResponse out = reply(req);
    calls.push_back(std::move(req));
    return out;
  }
};

sfmapi::HttpResponse OkJson(int status, std::string body) {
  sfmapi::HttpResponse r;
  r.status = status;
  r.headers["content-type"] = "application/json";
  r.body.assign(body.begin(), body.end());
  return r;
}
}  // namespace

static void TestUploadFile() {
  // Write a temp file with some bytes
  std::string path = "test_upload_payload.bin";
  {
    std::ofstream f(path, std::ios::binary);
    for (int i = 0; i < 4096; ++i) f.put(static_cast<char>(i & 0xFF));
  }

  auto rec = std::make_shared<Recorder>();
  rec->reply = [](const sfmapi::HttpRequest& req) -> sfmapi::HttpResponse {
    if (req.method == "POST" && req.url.find(":finalize") == std::string::npos &&
        req.url.find("/v1/uploads") != std::string::npos &&
        req.url.find("/uploads/") == std::string::npos) {
      return OkJson(200, R"({"upload_id":"u_test","received_bytes":0,"complete":false})");
    }
    if (req.method == "PATCH") {
      return OkJson(200, R"({"upload_id":"u_test","received_bytes":4096,"complete":false})");
    }
    if (req.method == "POST" && req.url.find(":finalize") != std::string::npos) {
      return OkJson(200, R"({"upload_id":"u_test","received_bytes":4096,"complete":true,"sha256":"abc","size_bytes":4096})");
    }
    return OkJson(404, "{}");
  };
  sfmapi::ClientOptions opts;
  opts.base_url = "http://x";
  opts.transport = [rec](sfmapi::HttpRequest req) {
    return (*rec)(std::move(req));
  };
  sfmapi::Client c{opts};

  auto resp = c.UploadFile(path, /*chunk_size=*/1024);
  CHECK(resp.status == 200, "upload finalize returned 200");
  // 1 init + 4 chunks (4096/1024) + 1 finalize = 6 calls
  CHECK(rec->calls.size() == 6, "6 HTTP calls");
  CHECK(rec->calls[0].method == "POST", "init POST");
  CHECK(rec->calls[1].method == "PATCH", "first chunk PATCH");
  CHECK(rec->calls[5].method == "POST", "finalize POST");
  CHECK(rec->calls[5].url.find(":finalize") != std::string::npos, "finalize URL");

  std::remove(path.c_str());
  std::printf("  UploadFile OK\n");
}

static void TestSubmitMatchesSplit() {
  auto rec = std::make_shared<Recorder>();
  rec->reply = [](const sfmapi::HttpRequest&) {
    return OkJson(200, R"({"job_id":"j_1","task_ids":["t_1"]})");
  };
  sfmapi::ClientOptions opts;
  opts.base_url = "http://x";
  opts.transport = [rec](sfmapi::HttpRequest req) {
    return (*rec)(std::move(req));
  };
  sfmapi::Client c{opts};

  sfmapi::PairsSpec p;
  p.strategy = sfmapi::kPairSequential;
  p.overlap = 5;
  sfmapi::MatcherSpec m;
  m.type = sfmapi::kMatcherLightGlue;

  auto resp = c.SubmitMatchesSplit("ds_1", p, m);
  CHECK(resp.status == 200, "split match 200");
  CHECK(rec->calls.size() == 1, "1 call");
  CHECK(rec->calls[0].url.find("/v1/datasets/ds_1/match") != std::string::npos,
        "match URL");
  std::string body(rec->calls[0].body.begin(), rec->calls[0].body.end());
  auto j = sfmapi::Json::Parse(body);
  CHECK(j.contains("pairs"), "body has pairs");
  CHECK(j.contains("matcher"), "body has matcher");
  CHECK(j["pairs"]["strategy"].as_string() == "sequential", "split pairs");
  CHECK(j["matcher"]["type"].as_string() == "lightglue", "split matcher");
  std::printf("  SubmitMatchesSplit OK\n");
}

static void TestParseCapabilities() {
  sfmapi::HttpResponse r = OkJson(
      200,
      R"({"backend":{"name":"colmap_mod","version":"1.0","vendor":"v"},)"
      R"("features":{"matchers.lightglue":true,"ba.featuremetric":false}})");
  auto caps = sfmapi::Client::ParseCapabilities(r);
  CHECK(caps.backend.name == "colmap_mod", "backend name");
  CHECK(caps.backend.version == "1.0", "backend version");
  CHECK(caps.Supports("matchers.lightglue"), "supports lightglue");
  CHECK(!caps.Supports("ba.featuremetric"), "doesn't support featuremetric (false)");
  CHECK(!caps.Supports("absent"), "absent => false");
  std::printf("  ParseCapabilities OK\n");
}

static void TestParseJobSubmitResponse() {
  sfmapi::HttpResponse r = OkJson(
      200,
      R"({"job_id":"j_x","task_ids":["t_a","t_b"],"recon_id":"r_1",)"
      R"("dataset_id":"d_1","project_id":"p_1","method":"stub",)"
      R"("applied_sim3":{"rotation":{"w":1,"x":0,"y":0,"z":0},)"
      R"("translation":[0,0,0],"scale":1},)"
      R"("target_recon_id":"r_target","source_recon_ids":["r_a","r_b"],)"
      R"("strategy":"dhash","action_id":"hloc.extractFeatures","backend":"hloc",)"
      R"("provider":"colmap_cli","artifact_id":"a_1",)"
      R"("target_format":"sfmapi.features.local.v1",)"
      R"("radiance_field_id":"rf_1","radiance_evaluation_id":"re_1"})");
  auto js = sfmapi::Client::ParseJobSubmitResponse(r);
  CHECK(js.job_id == "j_x", "job_id");
  CHECK(js.task_ids.size() == 2, "2 tasks");
  CHECK(js.task_ids[0] == "t_a", "task[0]");
  CHECK(js.recon_id == "r_1", "recon_id");
  CHECK(js.dataset_id == "d_1", "dataset_id");
  CHECK(js.project_id == "p_1", "project_id");
  CHECK(js.method == "stub", "method");
  CHECK(js.applied_sim3_json.find("\"scale\":1") != std::string::npos,
        "applied_sim3 json");
  CHECK(js.target_recon_id == "r_target", "target_recon_id");
  CHECK(js.source_recon_ids.size() == 2, "source_recon_ids");
  CHECK(js.source_recon_ids[1] == "r_b", "source_recon_ids[1]");
  CHECK(js.strategy == "dhash", "strategy");
  CHECK(js.action_id == "hloc.extractFeatures", "action_id");
  CHECK(js.backend == "hloc", "backend");
  CHECK(js.provider == "colmap_cli", "provider echoed from 202");
  CHECK(js.artifact_id == "a_1", "artifact_id");
  CHECK(js.target_format == "sfmapi.features.local.v1", "target_format");
  CHECK(js.radiance_field_id == "rf_1", "radiance_field_id");
  CHECK(js.radiance_evaluation_id == "re_1", "radiance_evaluation_id");

  auto r2 = OkJson(
      200,
      R"({"job_id":"j_y","task_ids":[],"recon_id":null,"dataset_id":"d_1",)"
      R"("provider":null})");
  auto js2 = sfmapi::Client::ParseJobSubmitResponse(r2);
  CHECK(js2.job_id == "j_y", "y job_id");
  CHECK(js2.task_ids.empty(), "no tasks");
  CHECK(js2.recon_id.empty(), "null recon_id => empty string");
  CHECK(js2.dataset_id == "d_1", "dataset_id");
  CHECK(js2.provider.empty(), "null provider => empty string");
  CHECK(js2.source_recon_ids.empty(), "null source_recon_ids => empty vector");
  std::printf("  ParseJobSubmitResponse OK\n");
}

static void TestGetLocalizationResult() {
  // Mock GetJob to return a job with a localize task containing
  // a wire-shape LocalizationResult in outputs_ref.
  auto rec = std::make_shared<Recorder>();
  rec->reply = [](const sfmapi::HttpRequest&) {
    return OkJson(200, R"({
      "job_id":"j_loc",
      "tasks":[
        {"task_id":"t_1","kind":"extract_features","outputs_ref":null},
        {"task_id":"t_2","kind":"localize","outputs_ref":{
          "success":true,
          "num_inliers":42,
          "cam_from_world":{
            "rotation":{"w":1,"x":0,"y":0,"z":0},
            "translation":[1.5,2.5,3.5]
          },
          "inlier_matches":[[1,100],[2,200],[3,300]]
        }}
      ]
    })");
  };
  sfmapi::ClientOptions opts;
  opts.base_url = "http://x";
  opts.transport = [rec](sfmapi::HttpRequest req) {
    return (*rec)(std::move(req));
  };
  sfmapi::Client c{opts};
  auto loc = c.GetLocalizationResult("j_loc");
  CHECK(loc.success, "success");
  CHECK(loc.num_inliers == 42, "inliers");
  CHECK(loc.cam_from_world.has_value(), "has pose");
  CHECK(loc.cam_from_world->rotation.w == 1.0, "rot.w");
  CHECK(loc.cam_from_world->translation[0] == 1.5, "tx");
  CHECK(loc.inlier_matches.size() == 3, "3 matches");
  CHECK(loc.inlier_matches[2].first == 3, "match[2].kp");
  CHECK(loc.inlier_matches[2].second == 300, "match[2].p3d");
  std::printf("  GetLocalizationResult OK\n");
}

static void TestGetLocalizationResultThrowsWhenAbsent() {
  auto rec = std::make_shared<Recorder>();
  rec->reply = [](const sfmapi::HttpRequest&) {
    return OkJson(200, R"({"job_id":"j_x","tasks":[
      {"task_id":"t","kind":"extract_features","outputs_ref":null}
    ]})");
  };
  sfmapi::ClientOptions opts;
  opts.base_url = "http://x";
  opts.transport = [rec](sfmapi::HttpRequest req) {
    return (*rec)(std::move(req));
  };
  sfmapi::Client c{opts};
  bool threw = false;
  try { c.GetLocalizationResult("j_x"); } catch (const std::runtime_error&) { threw = true; }
  CHECK(threw, "should throw when no localize task");
  std::printf("  GetLocalizationResult absence OK\n");
}

static void TestParseEventsBuffer() {
  std::string body =
      "id: 1\nevent: progress\ndata: hi\n\n"
      "id: 2\ndata: bye\n\n";
  auto evs = sfmapi::Client::ParseEventsBuffer(body);
  CHECK(evs.size() == 2, "2 SSE events via Client static");
  CHECK(evs[0].event == "progress", "first event");
  CHECK(evs[1].data == "bye", "second data");
  std::printf("  Client::ParseEventsBuffer OK\n");
}

int main() {
  std::cout << "sfmapi C++ extras (json/specs/sse/convenience):\n";
  TestJsonRoundTrip();
  TestJsonEscapes();
  TestJsonNumbers();
  TestJsonErrors();
  TestJsonBuilder();
  TestSpecs();
  TestArtifactDecoders();
  TestDataflowContractDecoders();
  TestSseParse();
  TestSseCrLf();
  TestUploadFile();
  TestSubmitMatchesSplit();
  TestParseCapabilities();
  TestParseJobSubmitResponse();
  TestGetLocalizationResult();
  TestGetLocalizationResultThrowsWhenAbsent();
  TestParseEventsBuffer();
  std::cout << "all OK\n";
  return 0;
}
