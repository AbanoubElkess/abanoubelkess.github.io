module.exports = {
  content: ["_site/**/*.html", "_site/**/*.js"],
  css: ["_site/assets/css/*.css"],
  output: "_site/assets/css/",
  skippedContentGlobs: ["_site/assets/**/*.html"],
  safelist: {
    // A selector that is only a pseudo-class carries no identifier for the
    // extractor to match against, so it would be dropped silently along with
    // the site's only visible focus indicator. Every other runtime-applied
    // class is already found: the dashboard markup is in _site/**/*.html and
    // the class names toggled by JS appear as string literals in
    // _site/assets/js/dashboard.js, which `content` above already scans.
    standard: [/focus-visible/],
  },
};
