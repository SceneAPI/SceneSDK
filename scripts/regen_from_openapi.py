"""Regenerate SDK artifacts from the local OpenAPI snapshot."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "openapi.json"
PYTHON_OUT = ROOT / "python" / "scenesdk"
TS_ROOT = ROOT / "typescript"
TS_OUT = TS_ROOT / "src" / "_generated" / "openapi.d.ts"
PYTHON_METADATA_FILES = ("pyproject.toml", "README.md", "py.typed", "_ergonomics.py")
CODEGEN_PROVENANCE_PATHS = (
    "openapi.json",
    "python/scenesdk/api",
    "python/scenesdk/models",
    "python/scenesdk/client.py",
    "python/scenesdk/__init__.py",
    "python/scenesdk/errors.py",
    "python/scenesdk/types.py",
    "python/scenesdk/_ergonomics.py",
    "python/scenesdk/pyproject.toml",
    "typescript/src/_generated",
    "typescript/src/errors.ts",
    "typescript/src/index.ts",
)


def _snapshot_metadata() -> dict[str, str]:
    return {
        name: (PYTHON_OUT / name).read_text(encoding="utf-8")
        for name in PYTHON_METADATA_FILES
        if (PYTHON_OUT / name).is_file()
    }


def _restore_metadata(cache: dict[str, str]) -> None:
    for name, content in cache.items():
        (PYTHON_OUT / name).write_text(content, encoding="utf-8")


def _iter_codegen_files(root: Path):
    for rel in CODEGEN_PROVENANCE_PATHS:
        path = root / rel
        if path.is_file():
            yield path
            continue
        if not path.is_dir():
            raise FileNotFoundError(f"missing generated SDK artifact: {path}")
        for child in sorted(path.rglob("*")):
            if not child.is_file():
                continue
            if "__pycache__" in child.parts or child.suffix == ".pyc":
                continue
            yield child


def _codegen_provenance_hash(root: Path) -> str:
    h = hashlib.sha256()
    for path in _iter_codegen_files(root):
        rel = path.relative_to(root).as_posix()
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(path.read_bytes().replace(b"\r\n", b"\n"))
        h.update(b"\0")
    return h.hexdigest()


def _replace_once(text: str, old: str, new: str, path: Path) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"expected exactly one generated SDK patch target in {path}: {old!r}; "
            f"found {count}"
        )
    return text.replace(old, new)


def _patch_pipeline_step_models() -> None:
    def patch_file(path: Path, reps: dict[str, str]) -> None:
        if not path.is_file():
            raise FileNotFoundError(f"generated SDK patch target missing: {path}")
        text = path.read_text(encoding="utf-8")
        for old, new in reps.items():
            text = _replace_once(text, old, new, path)
        path.write_text(text, encoding="utf-8")

    dict_reps = {
        "attributes = self.attributes.to_dict()": (
            "attributes = self.attributes.to_dict() if hasattr(self.attributes, \"to_dict\") "
            "else dict(self.attributes)"
        ),
        "params = self.params.to_dict()": (
            "params = self.params.to_dict() if hasattr(self.params, \"to_dict\") "
            "else dict(self.params)"
        ),
        "wires = self.wires.to_dict()": (
            "wires = self.wires.to_dict() if hasattr(self.wires, \"to_dict\") "
            "else dict(self.wires)"
        ),
    }
    patch_file(PYTHON_OUT / "models" / "processor_pipeline_step.py", dict_reps)

    legacy_path = PYTHON_OUT / "models" / "legacy_operation_step.py"
    legacy_params_path = PYTHON_OUT / "models" / "legacy_operation_step_params.py"
    pipeline_path = PYTHON_OUT / "models" / "pipeline_step.py"
    pipeline_params_path = PYTHON_OUT / "models" / "pipeline_step_params.py"
    step_reps = {
        "params = self.params.to_dict()": (
            "params = self.params.to_dict() if hasattr(self.params, \"to_dict\") "
            "else dict(self.params)"
        ),
    }
    if legacy_path.is_file():
        patch_file(legacy_path, step_reps)
        pipeline_path.write_text(
            "from .legacy_operation_step import LegacyOperationStep as PipelineStep\n\n"
            "__all__ = [\"PipelineStep\"]\n",
            encoding="utf-8",
        )
        pipeline_params_path.write_text(
            "from .legacy_operation_step_params import LegacyOperationStepParams as PipelineStepParams\n\n"
            "__all__ = [\"PipelineStepParams\"]\n",
            encoding="utf-8",
        )
    elif pipeline_path.is_file():
        patch_file(pipeline_path, step_reps)
        legacy_path.write_text(
            "from .pipeline_step import PipelineStep as LegacyOperationStep\n\n"
            "__all__ = [\"LegacyOperationStep\"]\n",
            encoding="utf-8",
        )
        if not pipeline_params_path.is_file():
            raise FileNotFoundError(f"generated SDK patch target missing: {pipeline_params_path}")
        legacy_params_path.write_text(
            "from .pipeline_step_params import PipelineStepParams as LegacyOperationStepParams\n\n"
            "__all__ = [\"LegacyOperationStepParams\"]\n",
            encoding="utf-8",
        )
    else:
        raise FileNotFoundError(
            f"generated SDK step model missing: expected {legacy_path} or {pipeline_path}"
        )

    init_path = PYTHON_OUT / "models" / "__init__.py"
    if init_path.is_file():
        text = init_path.read_text(encoding="utf-8")
        if "from .legacy_operation_step import LegacyOperationStep" not in text:
            text = _replace_once(
                text,
                "from .pipeline_step_params import PipelineStepParams\n",
                "from .pipeline_step_params import PipelineStepParams\n"
                "from .legacy_operation_step import LegacyOperationStep\n"
                "from .legacy_operation_step_params import LegacyOperationStepParams\n",
                init_path,
            )
        if "from .pipeline_step import PipelineStep" not in text:
            text = _replace_once(
                text,
                "from .legacy_operation_step_params import LegacyOperationStepParams\n",
                "from .legacy_operation_step_params import LegacyOperationStepParams\n"
                "from .pipeline_step import PipelineStep\n"
                "from .pipeline_step_params import PipelineStepParams\n",
                init_path,
            )
        if '"LegacyOperationStep",' not in text:
            text = _replace_once(
                text,
                '    "PipelineStepParams",\n',
                '    "PipelineStepParams",\n'
                '    "LegacyOperationStep",\n'
                '    "LegacyOperationStepParams",\n',
                init_path,
            )
        if '"PipelineStep",' not in text:
            text = _replace_once(
                text,
                '    "LegacyOperationStepParams",\n',
                '    "LegacyOperationStepParams",\n'
                '    "PipelineStep",\n'
                '    "PipelineStepParams",\n',
                init_path,
            )
        init_path.write_text(text, encoding="utf-8")


def _patch_documented_problem_responses() -> None:
    """Preserve generated parsing for ProblemResponse while keeping
    ``raise_on_unexpected_status=True`` fail-closed for every non-2xx
    response, including those now documented in OpenAPI.
    """
    needle = "    if response.status_code == "
    guard = (
        "    if response.status_code >= 400 and client.raise_on_unexpected_status:\n"
        "        raise errors.UnexpectedStatus(response.status_code, response.content)\n\n"
    )
    seen = 0
    inserted = 0
    for path in sorted((PYTHON_OUT / "api").rglob("*.py")):
        if path.name == "__init__.py":
            continue
        text = path.read_text(encoding="utf-8")
        if "def _parse_response(" not in text:
            continue
        text = text.replace(
            "errors.UnexpectedStatus: If the server returns an undocumented status code "
            "and Client.raise_on_unexpected_status is True.",
            "errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) "
            "and Client.raise_on_unexpected_status is True.",
        )
        count = text.count("def _parse_response(")
        if count != 1:
            raise RuntimeError(f"expected one _parse_response in {path}, found {count}")
        seen += 1
        fn_start = text.find("def _parse_response(")
        next_def = text.find("\ndef ", fn_start + 1)
        fn_end = len(text) if next_def < 0 else next_def
        fn_text = text[fn_start:fn_end]
        guard_count = fn_text.count("response.status_code >= 400 and client.raise_on_unexpected_status")
        if guard_count > 1:
            raise RuntimeError(f"expected one problem-response guard in {path}, found {guard_count}")
        if guard_count == 1:
            path.write_text(text, encoding="utf-8")
            continue
        idx = text.find(needle, fn_start, fn_end)
        if idx < 0:
            raise RuntimeError(f"could not find first response branch in {path}")
        text = text[:idx] + guard + text[idx:]
        path.write_text(text, encoding="utf-8")
        inserted += 1
    if seen == 0:
        raise RuntimeError("no generated API files with _parse_response were found")


def _patch_mixed_json_file_responses() -> None:
    def _remove_generated_model_import(text: str, model_name: str) -> str:
        lines = text.splitlines(keepends=True)
        out: list[str] = []
        removed = False
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("from ...models.") and line.rstrip().endswith("import ("):
                block = [line]
                j = i + 1
                while j < len(lines):
                    block.append(lines[j])
                    if lines[j].strip() == ")":
                        break
                    j += 1
                if any(model_name in block_line for block_line in block):
                    removed = True
                    i = j + 1
                    continue
            elif line.startswith("from ...models.") and model_name in line:
                removed = True
                i += 1
                continue
            out.append(line)
            i += 1
        if not removed:
            raise RuntimeError(f"generated response model import missing for {model_name}")
        return "".join(out)

    def _ensure_bytes_io_import(text: str) -> str:
        if "from io import BytesIO\n" in text:
            return text
        return text.replace("from http import HTTPStatus\n", "from http import HTTPStatus\nfrom io import BytesIO\n", 1)

    targets = [
        (
            PYTHON_OUT
            / "api"
            / "radiance"
            / "read_radiance_snapshot_file_v1_radiance_fields_radiance_field_id_snapshots_seq_name_get.py",
            "ReadRadianceSnapshotFileV1RadianceFieldsRadianceFieldIdSnapshotsSeqNameGetResponse200",
        ),
        (
            PYTHON_OUT
            / "api"
            / "reconstructions"
            / "read_snapshot_file_v1_reconstructions_recon_id_snapshots_seq_name_get.py",
            "ReadSnapshotFileV1ReconstructionsReconIdSnapshotsSeqNameGetResponse200",
        ),
        (
            PYTHON_OUT
            / "api"
            / "reconstructions"
            / "read_submodel_snapshot_file_v1_reconstructions_recon_id_snapshots_seq_submodels_idx_name_get.py",
            "ReadSubmodelSnapshotFileV1ReconstructionsReconIdSnapshotsSeqSubmodelsIdxNameGetResponse200",
        ),
    ]
    old_parse = (
        "    if response.status_code == 200:\n"
        "        response_200 = File(payload=BytesIO(response.content))\n\n"
        "        return response_200\n"
    )
    new_parse = (
        "    if response.status_code == 200:\n"
        "        content_type = response.headers.get(\"content-type\", \"\").split(\";\", 1)[0].strip().lower()\n"
        "        if content_type == \"application/json\":\n"
        "            response_200 = response.json()\n"
        "        else:\n"
        "            response_200 = File(payload=BytesIO(response.content))\n\n"
        "        return response_200\n"
    )
    for path, model_name in targets:
        if not path.is_file():
            raise FileNotFoundError(f"generated mixed file response target missing: {path}")
        text = path.read_text(encoding="utf-8")
        model_parse = (
            "    if response.status_code == 200:\n"
            f"        response_200 = {model_name}.from_dict(\n"
            "            response.json()\n"
            "        )\n\n"
            "        return response_200\n"
        )
        if old_parse in text:
            text = text.replace(old_parse, new_parse, 1)
        elif model_parse in text:
            text = text.replace(model_parse, new_parse, 1)
            text = _remove_generated_model_import(text, model_name)
            text = text.replace(model_name, "dict[str, Any] | File")
        elif new_parse not in text:
            raise RuntimeError(f"generated mixed file response parse block missing in {path}")
        text = _ensure_bytes_io_import(text)
        text = text.replace(
            "from ...types import UNSET, Response, Unset",
            "from ...types import File, UNSET, Response, Unset",
        )
        text = text.replace(
            "File | ProblemResponse | None",
            "dict[str, Any] | File | ProblemResponse | None",
        )
        text = text.replace(
            "Response[File | ProblemResponse]",
            "Response[dict[str, Any] | File | ProblemResponse]",
        )
        text = text.replace(
            "File | ProblemResponse",
            "dict[str, Any] | File | ProblemResponse",
        )
        text = text.replace("dict[str, Any] | dict[str, Any] | ", "dict[str, Any] | ")
        text = text.replace("File | dict[str, Any] | File", "dict[str, Any] | File")
        path.write_text(text, encoding="utf-8")


def _patch_artifact_content_response() -> None:
    path = (
        PYTHON_OUT
        / "api"
        / "artifacts"
        / "read_artifact_content_v1_artifacts_artifact_id_content_get.py"
    )
    if not path.is_file():
        raise FileNotFoundError(f"generated artifact content target missing: {path}")
    old_parse = (
        "    if response.status_code == 200:\n"
        "        response_200 = File(payload=BytesIO(response.json()))\n\n"
        "        return response_200\n"
    )
    new_parse = (
        "    if response.status_code == 200:\n"
        "        response_200 = File(payload=BytesIO(response.content))\n\n"
        "        return response_200\n"
    )
    text = path.read_text(encoding="utf-8")
    text = _replace_once(text, old_parse, new_parse, path)
    path.write_text(text, encoding="utf-8")


def _patch_ts_binary_media_types(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"generated TypeScript OpenAPI target missing: {path}")
    replacements = {
        '"application/octet-stream": string;': '"application/octet-stream": ArrayBuffer;',
        '"application/x-sfm-points-v1": string;': '"application/x-sfm-points-v1": ArrayBuffer;',
        '"image/bmp": string;': '"image/bmp": ArrayBuffer;',
        '"image/heic": string;': '"image/heic": ArrayBuffer;',
        '"image/heif": string;': '"image/heif": ArrayBuffer;',
        '"image/jpeg": string;': '"image/jpeg": ArrayBuffer;',
        '"image/png": string;': '"image/png": ArrayBuffer;',
        '"image/tiff": string;': '"image/tiff": ArrayBuffer;',
        '"image/webp": string;': '"image/webp": ArrayBuffer;',
    }
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    marker = "            /** @description Artifact content bytes. */"
    end_marker = "            /** @description Bad request. */"
    start = text.find(marker)
    if start == -1:
        raise ValueError("generated TypeScript OpenAPI artifact content block missing")
    end = text.find(end_marker, start)
    if end == -1:
        raise ValueError("generated TypeScript OpenAPI artifact content block malformed")
    block = text[start:end]
    for media in (
        '"application/json"',
        '"application/octet-stream"',
        '"application/x-ndjson"',
        '"image/jpeg"',
        '"image/png"',
        '"text/plain"',
    ):
        block = block.replace(f"{media}: string;", f"{media}: ArrayBuffer;")
    text = text[:start] + block + text[end:]
    path.write_text(text, encoding="utf-8")


def _patch_ts_defaulted_request_properties(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    old = "            require_lossless: boolean;"
    new = "            require_lossless?: boolean;"
    count = text.count(old)
    if count == 0 and text.count(new) >= 2:
        return
    if count != 2:
        raise RuntimeError(
            f"expected two defaulted require_lossless fields in {path}, found {count}"
        )
    text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def _patch_ts_artifact_conversion_targets(path: Path) -> None:
    def _replace_schema_block(text: str, label: str, new_block: str) -> str:
        start = text.find(f"        {label}: {{")
        if start == -1:
            raise RuntimeError(f"generated TypeScript {label} block missing in {path}")
        unpatched_end_marker = "\n        };"
        end = text.find(unpatched_end_marker, start)
        if end == -1:
            patched_end = text.find("\n        });", start)
            if patched_end != -1:
                block = text[start : patched_end + len("\n        });")]
                if "accepted_formats?: [string, ...string[]];" in block and "} & ({" in block:
                    return text
            raise RuntimeError(f"generated TypeScript {label} block malformed in {path}")
        end += len(unpatched_end_marker)
        old_block = text[start:end]
        if "accepted_formats?: [string, ...string[]];" in old_block and "} & ({" in old_block:
            return text
        if "accepted_formats?: string[];" not in old_block:
            raise RuntimeError(f"generated TypeScript {label} accepted_formats field missing in {path}")
        return text[:start] + new_block + text[end:]

    text = path.read_text(encoding="utf-8")
    plan_new = """        ArtifactConversionPlanRequest: {
            /**
             * Provider
             * @description Optional provider id to use when planning backend-native conversions.
             */
            provider?: string | null;
            /**
             * To Format
             * @description Exact target format id. Mutually compatible with accepted_formats.
             */
            to_format?: string | null;
            /**
             * Accepted Formats
             * @description Acceptable target format ids in preference order. Required to be non-empty when to_format is omitted.
             */
            accepted_formats?: [string, ...string[]];
            /**
             * Require Lossless
             * @default false
             */
            require_lossless?: boolean;
        } & ({
            to_format: string;
        } | {
            accepted_formats: [string, ...string[]];
        });"""
    convert_new = """        ArtifactConvertRequest: {
            /**
             * Provider
             * @description Optional provider id to use when planning backend-native conversions.
             */
            provider?: string | null;
            /**
             * To Format
             * @description Exact target format id. Mutually compatible with accepted_formats.
             */
            to_format?: string | null;
            /**
             * Accepted Formats
             * @description Acceptable target format ids in preference order. Required to be non-empty when to_format is omitted.
             */
            accepted_formats?: [string, ...string[]];
            /**
             * Require Lossless
             * @default false
             */
            require_lossless?: boolean;
            /** Name */
            name?: string | null;
            /** To Kind */
            to_kind?: string | null;
            /** Options */
            options?: {
                [key: string]: unknown;
            };
        } & ({
            to_format: string;
        } | {
            accepted_formats: [string, ...string[]];
        });"""
    text = _replace_schema_block(text, "ArtifactConversionPlanRequest", plan_new)
    text = _replace_schema_block(text, "ArtifactConvertRequest", convert_new)
    path.write_text(text, encoding="utf-8")


def _patch_python_artifact_conversion_targets() -> None:
    accepted_formats_block = """        accepted_formats: list[str] | Unset = UNSET
        if not isinstance(self.accepted_formats, Unset):
            accepted_formats = self.accepted_formats

"""
    to_format_block = """        to_format: None | str | Unset
        if isinstance(self.to_format, Unset):
            to_format = UNSET
        else:
            to_format = self.to_format

"""
    validation_block = """        to_format: None | str | Unset
        if isinstance(self.to_format, Unset):
            to_format = UNSET
        else:
            to_format = self.to_format

        if accepted_formats is not UNSET and len(accepted_formats) == 0:
            raise ValueError(
                "Artifact conversion requests require to_format or "
                "non-empty accepted_formats"
            )
        if (to_format is UNSET or to_format is None) and accepted_formats is UNSET:
            raise ValueError(
                "Artifact conversion requests require to_format or "
                "non-empty accepted_formats"
            )

"""
    for name in (
        "artifact_conversion_plan_request.py",
        "artifact_convert_request.py",
    ):
        path = PYTHON_OUT / "models" / name
        if not path.is_file():
            raise FileNotFoundError(f"generated conversion request model missing: {path}")
        text = path.read_text(encoding="utf-8")
        if validation_block in text:
            continue
        count = text.count(accepted_formats_block)
        if count != 1:
            raise RuntimeError(
                f"expected one accepted_formats patch point in {path}, found {count}"
            )
        count = text.count(to_format_block)
        if count != 1:
            raise RuntimeError(f"expected one to_format patch point in {path}, found {count}")
        path.write_text(text.replace(to_format_block, validation_block, 1), encoding="utf-8")


def _patch_unexpected_status_docs() -> None:
    replacements = {
        "errors.UnexpectedStatus: If the server returns an undocumented status code "
        "and Client.raise_on_unexpected_status is True.": (
            "errors.UnexpectedStatus: If the server returns any HTTP error status (>=400) "
            "and Client.raise_on_unexpected_status is True."
        ),
        "Raised by api functions when the response status an undocumented status "
        "and Client.raise_on_unexpected_status is True": (
            "Raised by API functions when the response status is an HTTP error "
            "and Client.raise_on_unexpected_status is True"
        ),
    }
    for path in sorted(PYTHON_OUT.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate SDK artifacts from the local OpenAPI snapshot."
    )
    parser.add_argument(
        "--typescript-only",
        action="store_true",
        help="Regenerate only TypeScript OpenAPI declarations with sfmapi patches.",
    )
    args = parser.parse_args(argv)

    if not SPEC_PATH.is_file():
        print(f"missing {SPEC_PATH}", file=sys.stderr)
        return 2

    if not args.typescript_only and not shutil.which("uvx"):
        print("uvx not on PATH", file=sys.stderr)
        return 2

    if not args.typescript_only:
        metadata = _snapshot_metadata()
        rc = subprocess.run(
            [
                "uvx",
                "openapi-python-client",
                "generate",
                "--path",
                str(SPEC_PATH),
                "--output-path",
                str(PYTHON_OUT),
                "--overwrite",
                "--meta",
                "none",
            ],
            check=False,
        ).returncode
        if rc != 0:
            return rc
        _restore_metadata(metadata)
        _patch_pipeline_step_models()
        _patch_documented_problem_responses()
        _patch_mixed_json_file_responses()
        _patch_artifact_content_response()
        _patch_python_artifact_conversion_targets()
        _patch_unexpected_status_docs()

    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if npx is None:
        print("npx not on PATH; TypeScript OpenAPI generation is required")
        return 2
    TS_OUT.parent.mkdir(parents=True, exist_ok=True)
    rc = subprocess.run(
        [
            npx,
            "openapi-typescript",
            str(SPEC_PATH),
            "-o",
            str(TS_OUT),
        ],
        cwd=TS_ROOT,
        check=False,
    ).returncode
    if rc == 0:
        _patch_ts_binary_media_types(TS_OUT)
        _patch_ts_defaulted_request_properties(TS_OUT)
        _patch_ts_artifact_conversion_targets(TS_OUT)
        if args.typescript_only:
            print("TypeScript OpenAPI declarations regenerated; codegen provenance unchanged")
        else:
            sha = _codegen_provenance_hash(ROOT)
            (ROOT / ".sdk_codegen.sha256").write_text(sha + "\n", encoding="utf-8")
            print(f"wrote .sdk_codegen.sha256 = {sha[:12]}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
