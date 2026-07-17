import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts", "src/_generated/client.ts", "src/errors.ts"],
  format: ["esm", "cjs"],
  dts: true,
  sourcemap: true,
  clean: true,
  target: "es2022",
  splitting: true,
  treeshake: true,
});
