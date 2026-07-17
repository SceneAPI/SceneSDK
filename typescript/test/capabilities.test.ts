import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

import { CORE_CAPABILITIES, OPTIONAL_CAPABILITIES } from "../src/capabilities";

const serverCapabilitiesPath = fileURLToPath(
  new URL("../../../sfmapi/app/core/capabilities.py", import.meta.url),
);

function parseTuple(source: string, name: string): string[] {
  const lines = source.split(/\r?\n/);
  const start = lines.findIndex((line) => line.startsWith(`${name}:`));
  if (start < 0) {
    throw new Error(`could not find ${name}`);
  }
  const body: string[] = [];
  for (let index = start + 1; index < lines.length; index += 1) {
    const line = lines[index];
    if (line === undefined || line.startsWith(")")) {
      break;
    }
    body.push(line);
  }
  return [...body.join("\n").matchAll(/"([^"]+)"/g)].map((item) => {
    const value = item[1];
    if (value === undefined) {
      throw new Error(`invalid capability tuple entry in ${name}`);
    }
    return value;
  });
}

describe("capability constants", () => {
  it.runIf(existsSync(serverCapabilitiesPath))(
    "match the server closed vocabulary",
    () => {
      const source = readFileSync(serverCapabilitiesPath, "utf8");
      expect([...CORE_CAPABILITIES]).toEqual(parseTuple(source, "CORE_CAPABILITIES"));
      expect([...OPTIONAL_CAPABILITIES]).toEqual(
        parseTuple(source, "OPTIONAL_CAPABILITIES"),
      );
    },
  );
});
