/**
 * Shared filter/search/view controller for the Projects and Blog dashboards.
 *
 * These were two page-local copies, 91% byte-identical, that had already
 * diverged in behaviour: the blog matched categories with `includes()` on a
 * joined string while projects used `===`. Two copies drifting apart while
 * still looking identical is the argument for consolidating them. Both now use
 * comma-list membership, which is correct for the blog's joined categories and
 * for the projects' single values alike.
 *
 * Everything is driven by the markup, so neither page passes configuration:
 *   [data-dashboard="name"]          the root; `name` is the localStorage key
 *                                    and the noun in the result announcement
 *   [data-dashboard-items]           the grid/list container
 *   [data-card]                      a filterable card, carrying data-title,
 *                                    data-desc and one attribute per dimension
 *   .filter-group[data-filter="key"] a filter dimension; its buttons carry
 *                                    data-<key>, one of them valued "all"
 *
 * Adding a filter dimension therefore needs no change here.
 */
(() => {
  "use strict";

  const initDashboard = (root) => {
    const name = root.dataset.dashboard;
    const container = root.querySelector("[data-dashboard-items]");
    if (!container) return;

    const cards = container.querySelectorAll("[data-card]");
    const searchInput = root.querySelector(".search-input");
    const clearBtn = root.querySelector(".clear-search-btn");
    const emptyState = root.querySelector(".empty-state");
    const resetBtn = root.querySelector(".reset-filters-btn");
    const status = root.querySelector('[role="status"]');
    const viewBtns = root.querySelectorAll(".view-btn");
    const layoutKey = `${name}-layout`;

    let search = "";

    // One dimension per .filter-group that declares a key. The reset button sits
    // in a group with no data-filter, so it is skipped without a special case.
    const dimensions = [...root.querySelectorAll(".filter-group[data-filter]")].map((group) => ({
      key: group.dataset.filter,
      buttons: group.querySelectorAll(`button[data-${group.dataset.filter}]`),
    }));

    const selected = {};

    const select = (dimension, value) => {
      selected[dimension.key] = value;
      dimension.buttons.forEach((button) => {
        const on = button.dataset[dimension.key] === value;
        button.classList.toggle("active", on);
        button.setAttribute("aria-pressed", String(on));
      });
    };

    const matches = (card) =>
      (!search || card.dataset.title.includes(search) || card.dataset.desc.includes(search)) &&
      dimensions.every((d) => {
        const want = selected[d.key];
        return want === "all" || (card.dataset[d.key] || "").split(",").some((v) => v.trim() === want);
      });

    const apply = () => {
      let visible = 0;
      cards.forEach((card) => {
        const show = matches(card);
        card.classList.toggle("hidden", !show);
        if (show) visible++;
      });
      if (emptyState) emptyState.style.display = visible ? "none" : "block";
      // Filtering used to mutate the DOM silently, so no user could tell
      // "3 of 12" from "12 of 12" without counting.
      if (status) status.textContent = `Showing ${visible} of ${cards.length} ${name}.`;
    };

    // Filter state lives in the URL so a filtered view can be linked and
    // restored. Called only from user handlers: writing on load would strip the
    // fragment and any unrelated query parameters from the address bar.
    const writeUrl = () => {
      const params = new URLSearchParams();
      if (search) params.set("q", search);
      dimensions.forEach((d) => {
        if (selected[d.key] !== "all") params.set(d.key, selected[d.key]);
      });
      const qs = params.toString();
      history.replaceState(null, "", (qs ? `?${qs}` : location.pathname) + location.hash);
    };

    const update = () => {
      apply();
      writeUrl();
    };

    const setSearch = (value) => {
      if (searchInput) searchInput.value = value;
      search = value.toLowerCase().trim();
      if (clearBtn) clearBtn.style.display = search ? "flex" : "none";
    };

    const setView = (mode) => {
      const isList = mode === "list";
      container.classList.toggle("list-layout", isList);
      container.classList.toggle("grid-layout", !isList);
      viewBtns.forEach((button) => {
        const on = button.dataset.view === mode;
        button.classList.toggle("active", on);
        button.setAttribute("aria-pressed", String(on));
      });
      localStorage.setItem(layoutKey, mode);
    };

    dimensions.forEach((d) =>
      d.buttons.forEach((button) =>
        button.addEventListener("click", () => {
          select(d, button.dataset[d.key]);
          update();
        })
      )
    );

    viewBtns.forEach((button) => button.addEventListener("click", () => setView(button.dataset.view)));

    searchInput?.addEventListener("input", () => {
      setSearch(searchInput.value);
      update();
    });

    clearBtn?.addEventListener("click", () => {
      setSearch("");
      update();
    });

    resetBtn?.addEventListener("click", () => {
      setSearch("");
      dimensions.forEach((d) => select(d, "all"));
      update();
    });

    // Restore from the URL, falling back to "all" for any value with no
    // matching button, which would otherwise leave a group with nothing chosen.
    const params = new URLSearchParams(location.search);
    setSearch(params.get("q") || "");
    dimensions.forEach((d) => {
      const want = params.get(d.key);
      const known = want && [...d.buttons].some((b) => b.dataset[d.key] === want);
      select(d, known ? want : "all");
    });

    setView(localStorage.getItem(layoutKey) === "list" ? "list" : "grid");
    apply();
  };

  document.querySelectorAll("[data-dashboard]").forEach(initDashboard);
})();
