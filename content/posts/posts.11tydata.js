// Applies to every markdown file in content/posts/.
// A post with `draft: true` produces no output file and joins no collection.
export default {
  layout: "post.njk",
  eleventyComputed: {
    permalink: (data) =>
      data.draft ? false : `${data.page.fileSlug}/index.html`,
    eleventyExcludeFromCollections: (data) => Boolean(data.draft),
  },
};
