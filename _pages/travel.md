---
layout: page
title: Travel & Fun
permalink: /travel/
description: Visual highlights and stories from my travels.
nav: false
nav_order: 6
---

<style>
  .travel-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }
  .travel-card {
    background: var(--global-card-bg-color, rgba(255, 255, 255, 0.05));
    border: 1px solid var(--global-divider-color, rgba(255, 255, 255, 0.1));
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    display: flex;
    flex-direction: column;
  }
  .travel-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
    border-color: var(--global-theme-color);
  }
  .travel-img-container {
    position: relative;
    width: 100%;
    height: 220px;
    overflow: hidden;
    background: #000;
  }
  .travel-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
    opacity: 0.9;
  }
  .travel-card:hover .travel-img {
    transform: scale(1.06);
    opacity: 1;
  }
  .travel-info {
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
  }
  .travel-location {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--global-theme-color);
    font-weight: 700;
    margin-bottom: 0.5rem;
  }
  .travel-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--global-text-color);
  }
  .travel-description {
    font-size: 0.85rem;
    line-height: 1.5;
    color: var(--global-text-color-light);
    margin: 0;
  }
</style>

<div class="travel-gallery">

  <div class="travel-card">
    <div class="travel-img-container">
      <img src="{{ '/assets/images/China_1.jpg' | relative_url }}" alt="Pudong skyline at night, Shanghai" class="travel-img" loading="lazy">
    </div>
    <div class="travel-info">
      <span class="travel-location">Shanghai, China</span>
      <h3 class="travel-title">Pudong Skyline from the Bund</h3>
      <p class="travel-description">The Pudong skyline glowing across the Huangpu River at night, with the Oriental Pearl Tower, Shanghai Tower, and the Shanghai World Financial Center lighting up the waterfront. A city I came to know well while leading the OMSCS Shanghai student chapter.</p>
    </div>
  </div>

  <div class="travel-card">
    <div class="travel-img-container">
      <img src="{{ '/assets/images/China_3.jpg' | relative_url }}" alt="At the base of the Oriental Pearl Tower, Shanghai" class="travel-img" loading="lazy">
    </div>
    <div class="travel-info">
      <span class="travel-location">Shanghai, China</span>
      <h3 class="travel-title">At the Oriental Pearl Tower</h3>
      <p class="travel-description">A clear-sky afternoon at the foot of the Oriental Pearl Tower in the Lujiazui financial district, one of Shanghai's most recognizable landmarks.</p>
    </div>
  </div>

  <div class="travel-card">
    <div class="travel-img-container">
      <img src="{{ '/assets/images/China_2.jpg' | relative_url }}" alt="Snow-covered ski resort in China" class="travel-img" loading="lazy">
    </div>
    <div class="travel-info">
      <span class="travel-location">China</span>
      <h3 class="travel-title">Winter on the Slopes</h3>
      <p class="travel-description">A crisp, sunny day at a snow-covered ski resort, with groomed runs carved into the mountainside and a lone sunflower brightening the railing in the foreground.</p>
    </div>
  </div>

</div>
