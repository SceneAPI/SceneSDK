"""Regenerate SDK artifacts from the local OpenAPI snapshot."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "openapi.json"
PYTHON_OUT = ROOT / "python" / "sfmapi_client_gen"
TS_ROOT = ROOT / "typescript"
TS_OUT = TS_ROOT / "src" / "_generated" / "openapi.d.ts"
PYTHON_METADATA_FILES = ("pyproject.toml", "README.md", "py.typed", "_ergonomics.py")


def _snapshot_metadata() -> dict[str, str]:
    return {
        name: (PYTHON_OUT / name).read_text(encoding="utf-8")
        for name in PYTHON_METADATA_FILES
        if (PYTHON_OUT / name).is_file()
    }


def _restore_metadata(cache: dict[str, str]) -> None:
    for name, content in cache.items():
        (PYTHON_OUT / name).write_text(content, encoding="utf-8")


def main() -> int:
    if not SPEC_PATH.is_file():
        print(f"missing {SPEC_PATH}", file=sys.stderr)
        return 2
    if not shutil.which("uvx"):
        print("uvx not on PATH", file=sys.stderr)
        return 2

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

    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if npx is None:
        print("skipping TypeScript generation: npx not on PATH")
        return 0
    TS_OUT.parent.mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        [npx, "openapi-typescript", str(SPEC_PATH), "-o", str(TS_OUT)],
        cwd=TS_ROOT,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
