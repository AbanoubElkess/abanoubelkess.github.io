---
layout: page
title: Projects
permalink: /projects/
description: A curated dashboard of research, academic projects, and industrial automation solutions in EDA, Machine Learning, and Systems.
nav: true
nav_order: 3
---

<div class="projects-dashboard">
  <!-- Controls Panel -->
  <div class="controls-panel">
    <!-- Search and View Switcher -->
    <div class="search-and-view">
      <div class="search-wrapper">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input type="text" id="project-search" class="search-input" placeholder="Search projects by title or description..." autocomplete="off">
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
        <button class="filter-btn category-filter" data-category="work">Work</button>
        <button class="filter-btn category-filter" data-category="academic">Academic</button>
      </div>
    </div>

    <!-- Area Filters -->
    <div class="filter-group">
      <span class="filter-label">Area</span>
      <div class="area-chips">
        <button class="area-chip area-filter active" data-area="all">All Areas</button>
        <button class="area-chip area-filter" data-area="Electronic Design Automation (EDA)">Electronic Design Automation (EDA)</button>
        <button class="area-chip area-filter" data-area="Systems & Quantum Computing">Systems & Quantum Computing</button>
        <button class="area-chip area-filter" data-area="Machine Learning & Data Science">Machine Learning & Data Science</button>
      </div>
    </div>

  </div>

  <!-- Projects Grid/List Container -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <div class="projects-container grid-layout" id="projects-container">
    {% for project in sorted_projects %}
      <div class="project-card" data-title="{{ project.title | downcase }}" data-desc="{{ project.description | downcase }}" data-category="{{ project.category }}" data-area="{{ project.area }}">
        <a href="{% if project.redirect %}{{ project.redirect }}{% else %}{{ project.url | relative_url }}{% endif %}" class="project-link">
          <div class="project-card-inner">
            {% if project.img %}
              <div class="project-image-wrapper">
                <img src="{{ project.img | relative_url }}" alt="{{ project.title }}" class="project-image" loading="lazy">
              </div>
            {% endif %}
            <div class="project-details">
              <div class="project-header">
                <h3 class="project-title">{{ project.title }}</h3>
                {% if project.area %}
                  <span class="project-area-badge">{{ project.area }}</span>
                {% endif %}
              </div>
              <p class="project-description">{{ project.description }}</p>
              <div class="project-footer">
                {% if project.github %}
                  <span class="project-github-link" onclick="event.preventDefault(); window.open('{{ project.github }}', '_blank')">
                    <i class="fa-brands fa-github"></i> Code
                  </span>
                {% endif %}
                <span class="project-category-badge">{{ project.category }}</span>
              </div>
            </div>
          </div>
        </a>
      </div>
    {% endfor %}
  </div>

  <!-- Empty State -->
  <div class="empty-state" id="projects-empty-state">
    <div class="empty-state-icon">
      <i class="fa-solid fa-box-open"></i>
    </div>
    <div class="empty-state-title">No projects match the criteria</div>
    <div class="empty-state-desc">Try modifying your search keywords or resetting the filter categories.</div>
    <button id="reset-filters-btn" class="reset-filters-btn">Reset Filters</button>
  </div>
</div>

<style>
/* Custom styling for projects dashboard */
.projects-dashboard {
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

/* Area Chips */
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

/* Projects Layouts */
.projects-container {
  transition: all 0.3s ease;
}

/* Grid Layout */
.projects-container.grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* List Layout */
.projects-container.list-layout {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Card Styling */
.project-card {
  background: var(--global-card-bg-color);
  border: 1px solid var(--global-divider-color);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.01);
  transition: all 0.25s ease;
  display: flex;
}

.project-card.hidden {
  display: none !important;
}

.project-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  border-color: var(--global-theme-color);
}

.project-link {
  color: inherit !important;
  text-decoration: none !important;
  width: 100%;
  display: flex;
}

.project-card-inner {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.project-image-wrapper {
  position: relative;
  overflow: hidden;
  background: var(--global-bg-color);
}

.project-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.project-card:hover .project-image {
  transform: scale(1.03);
}

.project-details {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.project-header {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 0.75rem;
}

.project-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.3;
  color: var(--global-text-color);
}

.project-area-badge {
  font-size: 0.7rem;
  background: rgba(131, 56, 236, 0.08);
  color: var(--global-theme-color);
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-weight: 600;
  align-self: flex-start;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.project-description {
  font-size: 0.875rem;
  color: var(--global-text-color-light);
  line-height: 1.5;
  margin-bottom: 1.25rem;
  flex-grow: 1;
}

.project-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--global-divider-color);
  padding-top: 0.75rem;
  margin-top: auto;
}

.project-github-link {
  font-size: 0.8rem;
  color: var(--global-text-color);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  cursor: pointer;
  transition: color 0.15s ease;
}

.project-github-link:hover {
  color: var(--global-theme-color);
}

.project-category-badge {
  font-size: 0.7rem;
  color: var(--global-text-color-light);
  background: var(--global-bg-color);
  border: 1px solid var(--global-divider-color);
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

/* Layout Specific Overrides */
/* Grid overrides */
.grid-layout .project-image-wrapper {
  height: 180px;
}

/* List overrides */
@media (min-width: 768px) {
  .list-layout .project-card-inner {
    flex-direction: row;
  }
  
  .list-layout .project-image-wrapper {
    width: 250px;
    min-width: 250px;
    height: auto;
  }
  
  .list-layout .project-details {
    padding: 1.25rem 1.5rem;
  }
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
  const searchInput = document.getElementById("project-search");
  const clearSearchBtn = document.getElementById("clear-search");
  const categoryBtns = document.querySelectorAll(".category-filter");
  const areaChips = document.querySelectorAll(".area-filter");
  const gridViewBtn = document.getElementById("grid-view-btn");
  const listViewBtn = document.getElementById("list-view-btn");
  const container = document.getElementById("projects-container");
  const projectCards = document.querySelectorAll(".project-card");
  const emptyState = document.getElementById("projects-empty-state");
  const resetBtn = document.getElementById("reset-filters-btn");

  let currentSearch = "";
  let currentCategory = "all";
  let currentArea = "all";

  // Search input handler
  if (searchInput) {
    searchInput.addEventListener("input", function() {
      currentSearch = searchInput.value.toLowerCase().trim();
      if (clearSearchBtn) {
        clearSearchBtn.style.display = currentSearch ? "flex" : "none";
      }
      filterProjects();
    });
  }

  // Clear search button handler
  if (clearSearchBtn) {
    clearSearchBtn.addEventListener("click", function() {
      searchInput.value = "";
      currentSearch = "";
      clearSearchBtn.style.display = "none";
      filterProjects();
    });
  }

  // Category selection handler
  categoryBtns.forEach(btn => {
    btn.addEventListener("click", function() {
      categoryBtns.forEach(b => b.classList.remove("active"));
      this.classList.add("active");
      currentCategory = this.getAttribute("data-category");
      filterProjects();
    });
  });

  // Area selection handler
  areaChips.forEach(chip => {
    chip.addEventListener("click", function() {
      areaChips.forEach(c => c.classList.remove("active"));
      this.classList.add("active");
      currentArea = this.getAttribute("data-area");
      filterProjects();
    });
  });

  // View style toggle handler
  if (gridViewBtn && listViewBtn && container) {
    gridViewBtn.addEventListener("click", function() {
      gridViewBtn.classList.add("active");
      listViewBtn.classList.remove("active");
      container.classList.add("grid-layout");
      container.classList.remove("list-layout");
      localStorage.setItem("projects-layout", "grid");
    });

    listViewBtn.addEventListener("click", function() {
      listViewBtn.classList.add("active");
      gridViewBtn.classList.remove("active");
      container.classList.add("list-layout");
      container.classList.remove("grid-layout");
      localStorage.setItem("projects-layout", "list");
    });

    // Load user view style preference
    const savedLayout = localStorage.getItem("projects-layout");
    if (savedLayout === "list") {
      listViewBtn.click();
    } else {
      gridViewBtn.click();
    }
  }

  // Main filter function
  function filterProjects() {
    let visibleCount = 0;

    projectCards.forEach(card => {
      const title = card.getAttribute("data-title") || "";
      const desc = card.getAttribute("data-desc") || "";
      const category = card.getAttribute("data-category") || "";
      const area = card.getAttribute("data-area") || "";

      const matchesSearch = currentSearch === "" || title.includes(currentSearch) || desc.includes(currentSearch);
      const matchesCategory = currentCategory === "all" || category === currentCategory;
      const matchesArea = currentArea === "all" || area === currentArea;

      if (matchesSearch && matchesCategory && matchesArea) {
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

      areaChips.forEach((c, idx) => {
        if (idx === 0) c.classList.add("active");
        else c.classList.remove("active");
      });
      currentArea = "all";

      filterProjects();
    });
  }
});
</script>
