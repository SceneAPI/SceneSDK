// Verifies the generated SDK's binary wire-format parser decodes
// canonical byte buffers correctly. Synthesizes payloads via
// DataView so the test runs without a live server; cross-language
// parity is enforced by Python's
// test_e_generated_ergonomics.py::test_parse_points_binary_round_trip_against_server_encoder
// and the server-owned golden fixture in golden_points.test.ts.
// (The depth / normal parsers were removed per lean-audit item 5.4 —
// no server route emits those formats.)

import { describe, expect, it } from "vitest";

import {
  parsePointsBinary,
  WireFormatError,
} from "../src/_generated/client.js";

const POINTS_HEADER_SIZE = 44;
const POINTS_RECORD_SIZE = 26;

function writeMagic(view: DataView, magic: number[]) {
  for (let i = 0; i < magic.length; i++) view.setUint8(i, magic[i]!);
}

function makePointsBlob(points: Array<{
  xyz: [number, number, number];
  rgb: [number, number, number];
  track_len: number;
  point3d_id: bigint;
}>, bboxMin: [number, number, number], bboxMax: [number, number, number]): ArrayBuffer {
  const total = POINTS_HEADER_SIZE + points.length * POINTS_RECORD_SIZE;
  const buf = new ArrayBuffer(total);
  const view = new DataView(buf);
  writeMagic(view, [0x53, 0x46, 0x4d, 0x50, 0x33, 0x44, 0x00, 0x00]);
  view.setUint32(8, 1, true);                        // version
  view.setBigUint64(12, BigInt(points.length), true); // count
  view.setFloat32(20, bboxMin[0], true);
  view.setFloat32(24, bboxMin[1], true);
  view.setFloat32(28, bboxMin[2], true);
  view.setFloat32(32, bboxMax[0], true);
  view.setFloat32(36, bboxMax[1], true);
  view.setFloat32(40, bboxMax[2], true);
  for (let i = 0; i < points.length; i++) {
    const off = POINTS_HEADER_SIZE + i * POINTS_RECORD_SIZE;
    const p = points[i]!;
    view.setFloat32(off, p.xyz[0], true);
    view.setFloat32(off + 4, p.xyz[1], true);
    view.setFloat32(off + 8, p.xyz[2], true);
    view.setUint8(off + 12, p.rgb[0]);
    view.setUint8(off + 13, p.rgb[1]);
    view.setUint8(off + 14, p.rgb[2]);
    view.setUint8(off + 15, 0); // padding
    view.setUint16(off + 16, p.track_len, true);
    view.setBigUint64(off + 18, p.point3d_id, true);
  }
  return buf;
}

describe("generated TS parsePointsBinary", () => {
  it("round-trips a synthesized 2-point payload", () => {
    const buf = makePointsBlob(
      [
        { xyz: [1, 2, 3], rgb: [255, 0, 0], track_len: 5, point3d_id: 100n },
        { xyz: [4.5, -1.5, 0.25], rgb: [0, 128, 255], track_len: 12, point3d_id: 0xDEADBEEFn },
      ],
      [0, -1.5, 0],
      [4.5, 2, 3],
    );
    const out = parsePointsBinary(buf);
    expect(out.count).toBe(2);
    expect(out.bbox_min).toEqual([0, -1.5, 0]);
    expect(out.bbox_max).toEqual([4.5, 2, 3]);
    expect(out.records[0]!.point3d_id).toBe(100n);
    expect(out.records[0]!.xyz).toEqual([1, 2, 3]);
    expect(out.records[0]!.rgb).toEqual([255, 0, 0]);
    expect(out.records[0]!.track_len).toBe(5);
    expect(out.records[1]!.point3d_id).toBe(0xDEADBEEFn);
  });

  it("rejects bad magic with WireFormatError", () => {
    const buf = new ArrayBuffer(POINTS_HEADER_SIZE);
    new DataView(buf).setUint32(0, 0xCAFEBABE, true);
    expect(() => parsePointsBinary(buf)).toThrow(WireFormatError);
  });

  it("rejects short buffer", () => {
    expect(() => parsePointsBinary(new ArrayBuffer(8))).toThrow(WireFormatError);
  });
});
