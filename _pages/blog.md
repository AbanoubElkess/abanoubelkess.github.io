---
layout: default
permalink: /blog/
title: Blog
nav: true
nav_order: 1
pagination:
  enabled: false
---

<div class="post">

{% assign blog_name_size = site.blog_name | size %}
{% assign blog_description_size = site.blog_description | size %}

{% if blog_name_size > 0 or blog_description_size > 0 %}
<div class="header-bar">
<h1>{{ site.blog_name }}</h1>
<h2>{{ site.blog_description }}</h2>
</div>
{% endif %}

  <div class="blogs-dashboard">
    <!-- Controls Panel -->
    <div class="controls-panel">
      <!-- Search and View Switcher -->
      <div class="search-and-view">
        <div class="search-wrapper">
          <i class="fa-solid fa-magnifying-glass search-icon"></i>
          <input type="text" id="blog-search" class="search-input" placeholder="Search blogs by title or description..." autocomplete="off">
          <button id="clear-search" class="clear-search-btn" style="display: none;">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
        <div class="view-toggle-container">
          <button id="grid-view-btn" class="view-btn active" title="Grid View">
            <i class="fa-solid fa-table-cells"></i> Grid
          </button>
          <button id="list-view-btn" class="view-btn" title="List View">
            <i class="fa-solid fa-list"></i> List
          </button>
        </div>
      </div>

      <!-- Category Filters -->
      <div class="filter-group">
        <span class="filter-label">Category</span>
        <div class="filter-buttons">
          <button class="filter-btn category-filter active" data-category="all">All</button>
          <button class="filter-btn category-filter" data-category="machine-learning">Machine Learning</button>
          <button class="filter-btn category-filter" data-category="deep-learning">Deep Learning</button>
        </div>
      </div>

      <!-- Year Filters -->
      <div class="filter-group">
        <span class="filter-label">Year</span>
        <div class="area-chips">
          <button class="area-chip year-filter active" data-year="all">All Years</button>
          <button class="area-chip year-filter" data-year="2024">2024</button>
          <button class="area-chip year-filter" data-year="2022">2022</button>
        </div>
      </div>
    </div>

    <!-- Blogs Grid/List Container -->
    <div class="blogs-container grid-layout" id="blogs-container">
      {% for post in site.posts %}
        {% if post.external_source == blank %}
          {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
        {% else %}
          {% assign read_time = post.feed_content | strip_html | number_of_words | divided_by: 180 | plus: 1 %}
        {% endif %}
        {% assign year = post.date | date: "%Y" %}
        {% assign date_str = post.date | date: "%B %d, %Y" %}

        <div class="blog-card" data-title="{{ post.title | downcase }}" data-desc="{{ post.description | downcase }}" data-category="{{ post.categories | join: ',' }}" data-year="{{ year }}">
          <a href="{% if post.redirect %}{{ post.redirect }}{% else %}{{ post.url | relative_url }}{% endif %}" class="blog-link" {% if post.redirect contains '://' %}target="_blank"{% endif %}>
            <div class="blog-card-inner">
              <div class="blog-details">
                <div class="blog-header">
                  <h3 class="blog-title">{{ post.title }}</h3>
                  <div class="blog-meta-badges">
                    <span class="blog-date-badge"><i class="fa-solid fa-calendar fa-sm"></i> {{ date_str }}</span>
                    <span class="blog-read-badge"><i class="fa-solid fa-clock fa-sm"></i> {{ read_time }} min read</span>
                  </div>
                </div>
                <p class="blog-description">{{ post.description }}</p>
                <div class="blog-footer">
                  <span class="blog-category-badge">{{ post.categories | join: ", " }}</span>
                </div>
              </div>
            </div>
          </a>
        </div>
      {% endfor %}
    </div>

    <!-- Empty State -->
    <div class="empty-state" id="blogs-empty-state">
      <div class="empty-state-icon">
        <i class="fa-solid fa-box-open"></i>
      </div>
      <div class="empty-state-title">No blog posts match the criteria</div>
      <div class="empty-state-desc">Try modifying your search keywords or resetting the filter categories.</div>
      <button id="reset-filters-btn" class="reset-filters-btn">Reset Filters</button>
    </div>

  </div>
</div>

<style>
/* Custom styling for blogs dashboard */
.blogs-dashboard {
  margin-top: 1.5rem;
}

/* Controls Panel */
.controls-panel {
  background: var(--global-card-bg-color);
  border: 1px solid var(--global-divider-color);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  border-radius: 14px;
  padding: 1.25rem;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: all 0.3s ease;
}

.search-and-view {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-wrapper {
  position: relative;
  flex: 1;
  min-width: 260px;
}

.search-input {
  width: 100%;
  padding: 0.65rem 2.5rem 0.65rem 2.5rem;
  border-radius: 30px;
  border: 1px solid var(--global-divider-color);
  background: var(--global-bg-color);
  color: var(--global-text-color);
  font-size: 0.95rem;
  transition: all 0.25s ease;
  outline: none;
}

.search-input:focus {
  border-color: var(--global-theme-color);
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--global-text-color-light);
  font-size: 0.95rem;
  pointer-events: none;
}

.clear-search-btn {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--global-text-color-light);
  cursor: pointer;
  padding: 0.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-search-btn:hover {
  color: var(--global-theme-color);
}

.view-toggle-container {
  display: flex;
  background: var(--global-bg-color);
  border: 1px solid var(--global-divider-color);
  border-radius: 30px;
  padding: 0.2rem;
}

.view-btn {
  background: transparent;
  border: none;
  color: var(--global-text-color-light);
  padding: 0.4rem 0.9rem;
  border-radius: 25px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.view-btn:hover {
  color: var(--global-text-color);
}

.view-btn.active {
  background: var(--global-theme-color);
  color: #fff !important;
}

/* Filter groups */
.filter-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  border-top: 1px solid var(--global-divider-color);
  padding-top: 0.75rem;
}

.filter-label {
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--global-text-color-light);
  min-width: 80px;
}

.filter-buttons {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.filter-btn {
  background: var(--global-bg-color);
  border: 1px solid var(--global-divider-color);
  color: var(--global-text-color);
  padding: 0.35rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  border-color: var(--global-theme-color);
  color: var(--global-theme-color);
}

.filter-btn.active {
  background: var(--global-theme-color);
  border-color: var(--global-theme-color);
  color: #fff !important;
}

/* Year Chips */
.area-chips {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.area-chip {
  background: var(--global-bg-color);
  border: 1px solid var(--global-divider-color);
  color: var(--global-text-color);
  padding: 0.35rem 0.9rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.area-chip:hover {
  border-color: var(--global-theme-color);
  color: var(--global-theme-color);
}

.area-chip.active {
  background: var(--global-theme-color);
  border-color: var(--global-theme-color);
  color: #fff !important;
}

/* Blogs Layouts */
.blogs-container {
  transition: all 0.3s ease;
}

/* Grid Layout */
.blogs-container.grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* List Layout */
.blogs-container.list-layout {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Card Styling */
.blog-card {
  background: var(--global-card-bg-color);
  border: 1px solid var(--global-divider-color);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.01);
  transition: all 0.25s ease;
  display: flex;
}

.blog-card.hidden {
  display: none !important;
}

.blog-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  border-color: var(--global-theme-color);
}

.blog-link {
  color: inherit !important;
  text-decoration: none !important;
  width: 100%;
  display: flex;
}

.blog-card-inner {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.blog-details {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.blog-header {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 0.75rem;
}

.blog-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.3;
  color: var(--global-text-color);
}

.blog-meta-badges {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.blog-date-badge, .blog-read-badge {
  font-size: 0.75rem;
  color: var(--global-text-color-light);
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.blog-description {
  font-size: 0.875rem;
  color: var(--global-text-color-light);
  line-height: 1.5;
  margin-bottom: 1.25rem;
  flex-grow: 1;
}

.blog-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  border-top: 1px solid var(--global-divider-color);
  padding-top: 0.75rem;
  margin-top: auto;
}

.blog-category-badge {
  font-size: 0.7rem;
  color: var(--global-text-color-light);
  background: var(--global-bg-color);
  border: 1px solid var(--global-divider-color);
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

/* Empty State */
.empty-state {
  display: none;
  text-align: center;
  padding: 3.5rem 1.5rem;
  background: var(--global-card-bg-color);
  border: 1px dashed var(--global-divider-color);
  border-radius: 12px;
  margin-top: 1.5rem;
}

.empty-state-icon {
  font-size: 2.5rem;
  color: var(--global-text-color-light);
  margin-bottom: 0.75rem;
}

.empty-state-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--global-text-color);
  margin-bottom: 0.4rem;
}

.empty-state-desc {
  color: var(--global-text-color-light);
  font-size: 0.85rem;
  margin-bottom: 1.25rem;
}

.reset-filters-btn {
  background: var(--global-theme-color);
  color: #fff !important;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 25px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.reset-filters-btn:hover {
  transform: scale(1.03);
}
</style>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const searchInput = document.getElementById("blog-search");
  const clearSearchBtn = document.getElementById("clear-search");
  const categoryBtns = document.querySelectorAll(".category-filter");
  const yearChips = document.querySelectorAll(".year-filter");
  const gridViewBtn = document.getElementById("grid-view-btn");
  const listViewBtn = document.getElementById("list-view-btn");
  const container = document.getElementById("blogs-container");
  const blogCards = document.querySelectorAll(".blog-card");
  const emptyState = document.getElementById("blogs-empty-state");
  const resetBtn = document.getElementById("reset-filters-btn");

  let currentSearch = "";
  let currentCategory = "all";
  let currentYear = "all";

  // Search input handler
  if (searchInput) {
    searchInput.addEventListener("input", function() {
      currentSearch = searchInput.value.toLowerCase().trim();
      if (clearSearchBtn) {
        clearSearchBtn.style.display = currentSearch ? "flex" : "none";
      }
      filterBlogs();
    });
  }

  // Clear search button handler
  if (clearSearchBtn) {
    clearSearchBtn.addEventListener("click", function() {
      searchInput.value = "";
      currentSearch = "";
      clearSearchBtn.style.display = "none";
      filterBlogs();
    });
  }

  // Category selection handler
  categoryBtns.forEach(btn => {
    btn.addEventListener("click", function() {
      categoryBtns.forEach(b => b.classList.remove("active"));
      this.classList.add("active");
      currentCategory = this.getAttribute("data-category");
      filterBlogs();
    });
  });

  // Year selection handler
  yearChips.forEach(chip => {
    chip.addEventListener("click", function() {
      yearChips.forEach(c => c.classList.remove("active"));
      this.classList.add("active");
      currentYear = this.getAttribute("data-year");
      filterBlogs();
    });
  });

  // View style toggle handler
  if (gridViewBtn && listViewBtn && container) {
    gridViewBtn.addEventListener("click", function() {
      gridViewBtn.classList.add("active");
      listViewBtn.classList.remove("active");
      container.classList.add("grid-layout");
      container.classList.remove("list-layout");
      localStorage.setItem("blogs-layout", "grid");
    });

    listViewBtn.addEventListener("click", function() {
      listViewBtn.classList.add("active");
      gridViewBtn.classList.remove("active");
      container.classList.add("list-layout");
      container.classList.remove("grid-layout");
      localStorage.setItem("blogs-layout", "list");
    });

    // Load user view style preference
    const savedLayout = localStorage.getItem("blogs-layout");
    if (savedLayout === "list") {
      listViewBtn.click();
    } else {
      gridViewBtn.click();
    }
  }

  // Main filter function
  function filterBlogs() {
    let visibleCount = 0;

    blogCards.forEach(card => {
      const title = card.getAttribute("data-title") || "";
      const desc = card.getAttribute("data-desc") || "";
      const category = card.getAttribute("data-category") || "";
      const year = card.getAttribute("data-year") || "";

      const matchesSearch = currentSearch === "" || title.includes(currentSearch) || desc.includes(currentSearch);
      const matchesCategory = currentCategory === "all" || category.includes(currentCategory);
      const matchesYear = currentYear === "all" || year === currentYear;

      if (matchesSearch && matchesCategory && matchesYear) {
        card.classList.remove("hidden");
        visibleCount++;
      } else {
        card.classList.add("hidden");
      }
    });

    if (emptyState) {
      emptyState.style.display = visibleCount === 0 ? "block" : "none";
    }
  }

  // Reset controls callback
  if (resetBtn) {
    resetBtn.addEventListener("click", function() {
      if (searchInput) searchInput.value = "";
      currentSearch = "";
      if (clearSearchBtn) clearSearchBtn.style.display = "none";

      categoryBtns.forEach((b, idx) => {
        if (idx === 0) b.classList.add("active");
        else b.classList.remove("active");
      });
      currentCategory = "all";

      yearChips.forEach((c, idx) => {
        if (idx === 0) c.classList.add("active");
        else c.classList.remove("active");
      });
      currentYear = "all";

      filterBlogs();
    });
  }
});
</script>
