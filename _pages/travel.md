---
layout: page
title: travel & fun
permalink: /travel/
description: Visual highlights and stories from my travels.
nav: true
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
      <img src="{{ '/assets/img/travel_swiss_alps.png' | relative_url }}" alt="Lauterbrunnen Valley, Switzerland" class="travel-img" loading="lazy">
    </div>
    <div class="travel-info">
      <span class="travel-location">Lauterbrunnen, Switzerland</span>
      <h3 class="travel-title">The Valley of 72 Waterfalls</h3>
      <p class="travel-description">A scenic look at the Lauterbrunnen valley in the Swiss Alps. Surrounded by towering rock faces and dramatic mountain peaks, a classic red alpine train winds through lush green meadows in the shadow of the Jungfrau massif.</p>
    </div>
  </div>

  <div class="travel-card">
    <div class="travel-img-container">
      <img src="{{ '/assets/img/travel_tokyo_night.png' | relative_url }}" alt="Tokyo Tower at night, Japan" class="travel-img" loading="lazy">
    </div>
    <div class="travel-info">
      <span class="travel-location">Tokyo, Japan</span>
      <h3 class="travel-title">Tokyo Tower Nightscape</h3>
      <p class="travel-description">The iconic Tokyo Tower glowing in warm orange and red hues against the deep indigo twilight of the city. Seen from a distance, the tower anchors a high-density skyline of skyscrapers, blending technological modernism with iconic landmarks.</p>
    </div>
  </div>

  <div class="travel-card">
    <div class="travel-img-container">
      <img src="{{ '/assets/img/travel_egypt_pyramids.png' | relative_url }}" alt="Giza Pyramids, Egypt" class="travel-img" loading="lazy">
    </div>
    <div class="travel-info">
      <span class="travel-location">Giza, Egypt</span>
      <h3 class="travel-title">Sunset at the Giza Plateau</h3>
      <p class="travel-description">The Great Pyramids of Giza rising above the desert sands during a golden sunset. A silhouette of camels crossing the dunes captures the historical heritage of this ancient site.</p>
    </div>
  </div>

</div>
