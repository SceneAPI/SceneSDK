"""Verify generated SDK artifacts match .sdk_codegen.sha256."""

from __future__ import annotations

from regen_from_openapi import ROOT, _codegen_provenance_hash


def main() -> int:
    expected_path = ROOT / ".sdk_codegen.sha256"
    if not expected_path.is_file():
        print("missing .sdk_codegen.sha256; run python scripts/regen_from_openapi.py")
        return 1
    expected = expected_path.read_text(encoding="utf-8").strip()
    actual = _codegen_provenance_hash(ROOT)
    if actual != expected:
        print("SDK codegen provenance mismatch")
        print(f"  expected: {expected}")
        print(f"  actual:   {actual}")
        print("Run python scripts/regen_from_openapi.py and commit the regenerated artifacts.")
        return 1
    print(f"SDK codegen provenance OK: {actual[:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
