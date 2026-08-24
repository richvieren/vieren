// Keep an empty listing out of Google, and let it back in on the first post.
// Must be a real boolean — a Nunjucks-rendered "false" is a truthy string,
// which silently pinned noindex on forever.
export default {
  eleventyComputed: {
    noindex: (data) => !data.collections?.posts?.length,
  },
};
