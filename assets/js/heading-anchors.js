/* Clickable permalinks on section headings.
 *
 * Kramdown already emits an id on every heading, so the anchors exist and the
 * table of contents uses them, but there is no way for a reader to grab a link
 * to a specific section. This adds a discreet marker that appears on hover and
 * is reachable by keyboard, which is the standard pattern on documentation and
 * long-form technical writing.
 *
 * Scoped to article content so it never touches the navbar, cards, or the CV.
 */
document.addEventListener("DOMContentLoaded", () => {
  const scopes = document.querySelectorAll(".post > article, .post > .post-content");
  scopes.forEach((scope) => {
    scope.querySelectorAll("h2[id], h3[id], h4[id]").forEach((heading) => {
      if (heading.querySelector(".heading-anchor")) return;
      const link = document.createElement("a");
      link.className = "heading-anchor";
      link.href = `#${heading.id}`;
      link.setAttribute("aria-label", `Link to section: ${heading.textContent.trim()}`);
      link.textContent = "#";
      heading.appendChild(link);
    });
  });
});
