import { DateTime } from "luxon";
import feedPlugin from "@11ty/eleventy-plugin-rss";

const SITE = "https://vieren.studio";

export default function (eleventyConfig) {
  eleventyConfig.addPlugin(feedPlugin);

  // Published posts only. Drafts never reach a collection or an output file.
  const published = (api) =>
    api
      .getFilteredByGlob("content/posts/*.md")
      .filter((p) => !p.data.draft)
      .sort((a, b) => b.date - a.date);

  eleventyConfig.addCollection("posts", published);

  // Tag list built from published posts only, so a draft tag never makes a page.
  eleventyConfig.addCollection("tagList", (api) => {
    const counts = new Map();
    for (const post of published(api)) {
      for (const tag of post.data.tags || []) {
        counts.set(tag, (counts.get(tag) || 0) + 1);
      }
    }
    return [...counts.entries()]
      .map(([tag, count]) => ({ tag, count }))
      .sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag));
  });

  eleventyConfig.addCollection("postsByTag", (api) => {
    const byTag = new Map();
    for (const post of published(api)) {
      for (const tag of post.data.tags || []) {
        if (!byTag.has(tag)) byTag.set(tag, []);
        byTag.get(tag).push(post);
      }
    }
    return [...byTag.entries()].map(([tag, posts]) => ({ tag, posts }));
  });

  eleventyConfig.addFilter("readableDate", (d) =>
    DateTime.fromJSDate(d, { zone: "utc" }).toFormat("d LLLL yyyy")
  );
  eleventyConfig.addFilter("isoDate", (d) =>
    DateTime.fromJSDate(d, { zone: "utc" }).toFormat("yyyy-LL-dd")
  );
  // Output lands in /articles/, but Eleventy's page.url is relative to that
  // output root. `pub` restores the real public path; `absolute` makes it a
  // full URL. Always run page.url through `pub` before `absolute`.
  const pub = (url) => `/articles${url}`;
  eleventyConfig.addFilter("pub", pub);
  eleventyConfig.addFilter("absolute", (path) => new URL(path, SITE).href);

  // Reading time from the rendered body.
  eleventyConfig.addFilter("readingTime", (html) => {
    const words = String(html).replace(/<[^>]*>/g, " ").trim().split(/\s+/).length;
    return Math.max(1, Math.round(words / 225));
  });

  eleventyConfig.addFilter("slug", (s) =>
    String(s)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")
  );

  eleventyConfig.addGlobalData("site", {
    url: SITE,
    name: "Vieren",
    title: "Vieren Studio",
    author: "Richard van der Vieren",
    description:
      "Notes on building companies, film, and the systems behind them.",
    defaultOgImage: "/ogimage.png",
  });

  return {
    dir: {
      input: "content",
      output: "articles",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    templateFormats: ["md", "njk"],
  };
}
