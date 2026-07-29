---
layout: default
permalink: /blog/
title: Blog
nav: true
nav_order: 4
dashboard: true # loads assets/js/dashboard.js via _includes/scripts.liquid
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

  <div class="blogs-dashboard" data-dashboard="posts">
    <div class="controls-panel">
      <div class="search-and-view">
        <div class="search-wrapper">
          <i class="fa-solid fa-magnifying-glass search-icon"></i>
          <input type="text" class="search-input" aria-label="Search posts by title or description" placeholder="Search posts by title or description..." autocomplete="off">
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

      <!-- Filter vocabularies are derived from the posts themselves. Hardcoding
           them meant a new category or year became silently unfilterable. -->
      <div class="filter-group" data-filter="category">
        <span class="filter-label" id="filter-label-category">Category</span>
        <div class="filter-buttons" role="group" aria-labelledby="filter-label-category">
          <button class="filter-btn active" data-category="all">All</button>
          {% assign cats = site.posts | map: "categories" | join: "," | split: "," | uniq | sort %}
          {% for c in cats %}
            <button class="filter-btn" data-category="{{ c }}">{{ c | replace: "-", " " | split: " " | map: "capitalize" | join: " " }}</button>
          {% endfor %}
        </div>
      </div>

      <div class="filter-group" data-filter="year">
        <span class="filter-label" id="filter-label-year">Year</span>
        <div class="filter-buttons" role="group" aria-labelledby="filter-label-year">
          <button class="filter-btn active" data-year="all">All years</button>
          {% assign year_groups = site.posts | group_by_exp: "p", "p.date | date: '%Y'" | sort: "name" | reverse %}
          {% for group in year_groups %}
            <button class="filter-btn" data-year="{{ group.name }}">{{ group.name }}</button>
          {% endfor %}
        </div>
      </div>

      <div class="filter-group">
        <button class="reset-filters-btn">Reset filters</button>
      </div>
    </div>

    <div class="sr-only" role="status" aria-live="polite"></div>

    <div class="blogs-container grid-layout" data-dashboard-items>
      {% for post in site.posts %}
        {% if post.external_source == blank %}
          {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
        {% else %}
          {% assign read_time = post.feed_content | strip_html | number_of_words | divided_by: 180 | plus: 1 %}
        {% endif %}
        {% assign year = post.date | date: "%Y" %}
        {% assign date_str = post.date | date: "%B %d, %Y" %}

        <div class="blog-card" data-card data-title="{{ post.title | downcase }}" data-desc="{{ post.description | downcase }}" data-category="{{ post.categories | join: ',' }}" data-year="{{ year }}">
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

    <div class="empty-state">
      <div class="empty-state-icon">
        <i class="fa-solid fa-box-open"></i>
      </div>
      <div class="empty-state-title">No posts match the criteria</div>
      <div class="empty-state-desc">Try different search terms, or reset the filters above.</div>
    </div>

  </div>
</div>
