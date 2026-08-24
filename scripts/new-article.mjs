#!/usr/bin/env node
// Create a new article stub.
//   npm run new -- "My Title" --tags "systems,ai" --subtitle "One line"
// Starts as a draft. Flip `draft: false` to publish.

import { writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const argv = process.argv.slice(2);

const flag = (name) => {
  const i = argv.indexOf(`--${name}`);
  return i !== -1 && argv[i + 1] ? argv[i + 1] : "";
};

// Title is the first argument, before any --flags.
const title = argv[0] && !argv[0].startsWith("--") ? argv[0] : "";
if (!title) {
  console.error('Usage: npm run new -- "My Title" [--tags "a,b"] [--subtitle "..."] [--slug custom-slug]');
  process.exit(1);
}

const slugify = (s) =>
  s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

const slug = flag("slug") || slugify(title);
const tags = flag("tags").split(",").map((t) => t.trim()).filter(Boolean);
const subtitle = flag("subtitle");
const today = new Date().toISOString().slice(0, 10);

const dir = join(ROOT, "content", "posts");
mkdirSync(dir, { recursive: true });
const file = join(dir, `${slug}.md`);

if (existsSync(file)) {
  console.error(`Refusing to overwrite: content/posts/${slug}.md`);
  process.exit(1);
}

const yaml = (s) => `"${String(s).replace(/"/g, '\\"')}"`;

const front = [
  "---",
  `title: ${yaml(title)}`,
  subtitle ? `subtitle: ${yaml(subtitle)}` : null,
  `date: ${today}`,
  `description: ${yaml(subtitle || title)}`,
  tags.length
    ? `tags:\n${tags.map((t) => `  - ${yaml(t)}`).join("\n")}`
    : "tags: []",
  "draft: true",
  "# image: /image/articles/" + slug + "/hero.webp",
  "# imageAlt: \"\"",
  "# canonical:   # only if the original lives elsewhere",
  "# source:      # link to the Substack/X version, shown as attribution",
  "# sourceName: Substack",
  "# noindex: true",
  "---",
  "",
  "Opening line.",
  "",
].filter(Boolean).join("\n");

writeFileSync(file, front, "utf8");
console.log(`content/posts/${slug}.md`);
console.log(`→ will publish at /articles/${slug}/ once draft: false`);
