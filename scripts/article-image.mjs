#!/usr/bin/env node
// Add an image to an article. Converts to WebP, caps the long edge, prints markdown.
//   npm run img -- <slug> <source-image> ["alt text"]
// Writes to image/articles/<slug>/<name>.webp and prints a paste-ready snippet.

import { existsSync, mkdirSync, statSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, dirname, basename, extname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const [slug, src, alt = ""] = process.argv.slice(2);

if (!slug || !src) {
  console.error('Usage: npm run img -- <slug> <source-image> ["alt text"]');
  process.exit(1);
}
if (!existsSync(src)) {
  console.error(`Not found: ${src}`);
  process.exit(1);
}

const MAX_EDGE = 1600; // plenty for a 720px column at 2x
const QUALITY = 86;

const outDir = join(ROOT, "image", "articles", slug);
mkdirSync(outDir, { recursive: true });

const name = basename(src, extname(src))
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, "-")
  .replace(/^-|-$/g, "");
const out = join(outDir, `${name}.webp`);

const dims = (file) => {
  const read = (key) =>
    Number(
      execFileSync("sips", ["-g", key, file], { encoding: "utf8" })
        .trim()
        .split(/\s+/)
        .pop()
    );
  return { w: read("pixelWidth"), h: read("pixelHeight") };
};

const before = dims(src);
const args = ["-q", String(QUALITY)];
if (Math.max(before.w, before.h) > MAX_EDGE) {
  args.push("-resize", before.w >= before.h ? `${MAX_EDGE}` : "0", before.w >= before.h ? "0" : `${MAX_EDGE}`);
}
args.push(src, "-o", out);

execFileSync("cwebp", args, { stdio: ["ignore", "ignore", "ignore"] });

const after = dims(out);
const srcKB = Math.round(statSync(src).size / 1024);
const outKB = Math.round(statSync(out).size / 1024);
const url = `/image/articles/${slug}/${name}.webp`;

console.log(`${before.w}x${before.h} ${srcKB}KB  ->  ${after.w}x${after.h} ${outKB}KB`);
console.log(`${url}\n`);
console.log(`![${alt}](${url})`);
if (!alt) console.log(`\nNo alt text given. Add some — it is a real accessibility and SEO field.`);
