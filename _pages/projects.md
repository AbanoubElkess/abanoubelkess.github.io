---
layout: page
title: Projects
permalink: /projects/
description: "Research, industrial, and academic work in EDA, machine learning, and systems. Ordered by how much of each project a reader can independently check: published work first, then industrial deployment by depth, then academic work whose results trace to a cited report, then work with no results to report, and finally work that was designed but never built."
nav: true
nav_order: 1
dashboard: true # loads assets/js/dashboard.js via _includes/scripts.liquid
---

<div class="projects-dashboard" data-dashboard="projects">
  <div class="controls-panel">
    <div class="search-and-view">
      <div class="search-wrapper">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input type="text" class="search-input" aria-label="Search projects by title or description" placeholder="Search projects by title or description..." autocomplete="off">
        <button class="clear-search-btn" aria-label="Clear search" style="display: none;">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div class="view-toggle-container">
        <button class="view-btn active" data-view="grid" aria-pressed="true" title="Grid view">
          <i class="fa-solid fa-table-cells"></i> Grid
        </button>
        <button class="view-btn" data-view="list" aria-pressed="false" title="List view">
          <i class="fa-solid fa-list"></i> List
        </button>
      </div>
    </div>

    <div class="filter-group" data-filter="category">
      <span class="filter-label" id="filter-label-category">Category</span>
      <div class="filter-buttons" role="group" aria-labelledby="filter-label-category">
        <button class="filter-btn active" data-category="all">All</button>
        <button class="filter-btn" data-category="work">Work</button>
        <button class="filter-btn" data-category="academic">Academic</button>
      </div>
    </div>

    <div class="filter-group" data-filter="area">
      <span class="filter-label" id="filter-label-area">Area</span>
      <div class="filter-buttons" role="group" aria-labelledby="filter-label-area">
        <button class="filter-btn active" data-area="all">All areas</button>
        {% assign areas = site.projects | map: "area" | compact | uniq | sort %}
        {% for area in areas %}
          <button class="filter-btn" data-area="{{ area }}">{{ area }}</button>
        {% endfor %}
      </div>
    </div>

    <div class="filter-group">
      <button class="reset-filters-btn">Reset filters</button>
    </div>

  </div>

  <div class="sr-only" role="status" aria-live="polite"></div>

{% assign sorted_projects = site.projects | sort: "importance" %}

  <div class="projects-container grid-layout" data-dashboard-items>
    {% for project in sorted_projects %}
      <div class="project-card" data-card data-title="{{ project.title | downcase }}" data-desc="{{ project.description | downcase }}" data-category="{{ project.category }}" data-area="{{ project.area }}">
        <a href="{% if project.redirect %}{{ project.redirect }}{% else %}{{ project.url | relative_url }}{% endif %}" class="project-link">
          <div class="project-card-inner">
            {% if project.img %}
              <div class="project-image-wrapper">
                {%
                  include figure.liquid
                  path=project.img
                  alt=project.title
                  class="project-image"
                  sizes="(min-width: 768px) 300px, 100vw"
                  loading="lazy"
                %}
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
                <span class="project-category-badge">{{ project.category }}</span>
              </div>
            </div>
          </div>
        </a>
      </div>
    {% endfor %}
  </div>

  <div class="empty-state">
    <div class="empty-state-icon">
      <i class="fa-solid fa-box-open"></i>
    </div>
    <div class="empty-state-title">No projects match the criteria</div>
    <div class="empty-state-desc">Try different search terms, or reset the filters above.</div>
  </div>
</div>
