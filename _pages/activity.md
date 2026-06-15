---
layout: page
permalink: /activity/
title: Activity
nav: false
nav_order: 4
description: Recent professional updates, academic milestones, and research presentations.
---

<div class="activity-feed">
  <div class="activity-header">
    <p class="activity-subtitle">Stay updated with my latest research, speaking engagements, and academic milestones.</p>
    <a href="https://linkedin.com/in/abanoub-wahib" target="_blank" class="linkedin-follow-btn">
      <i class="fa-brands fa-linkedin"></i> Follow on LinkedIn
    </a>
  </div>

  <div class="timeline">
    <!-- Timeline Item 1: ICLAD 2025 Stanford Presentation -->
    <div class="timeline-item">
      <div class="timeline-badge"><i class="fa-solid fa-person-chalkboard"></i></div>
      <div class="timeline-card">
        <div class="timeline-card-header">
          <div class="timeline-meta">
            <span class="timeline-date"><i class="fa-solid fa-calendar-day fa-sm"></i> June 2025</span>
            <span class="timeline-category-tag conference">Research Presentation</span>
          </div>
          <h3 class="timeline-title">Research Presentation at Stanford University (ICLAD 2025)</h3>
        </div>
        <div class="timeline-image-wrapper">
          <img src="{{ '/assets/images/2025_stanford_disucssion.jpg' | relative_url }}" alt="Abanoub E. Abdelmalak presenting at ICLAD 2025, Stanford University" class="timeline-image" loading="lazy">
        </div>
        <div class="timeline-card-body">
          <p>I presented our paper, <strong>“An AST-Guided Approach for SVRF Code Synthesis,”</strong> at the inaugural <strong>IEEE International Conference on LLM-Aided Design (ICLAD 2025)</strong>, hosted at <strong>Stanford University</strong>.</p>
          <p>The work began with a simple question: why are we still hand-writing SVRF rules? We combined Abstract Syntax Trees (AST) with LLM reasoning to generate verification-ready SVRF code in minutes, cutting development cycle time by roughly 40% at Siemens EDA. Presenting the approach and discussing it with peers afterward was a genuine highlight.</p>
          <p>Thanks to my debugging partner Mohamed Adel Elsayed, and to Ilhami Torunoglu, Ivan Kissiov, Scott Thompson, and David Abercrombie for their support of this project from the start.</p>
          <div class="timeline-footer">
            <div class="timeline-tags">
              <span class="timeline-tag">#ICLAD2025</span>
              <span class="timeline-tag">#Stanford</span>
              <span class="timeline-tag">#LargeLanguageModels</span>
              <span class="timeline-tag">#EDA</span>
              <span class="timeline-tag">#SiemensEDA</span>
            </div>
            <a href="https://www.linkedin.com/feed/update/urn:li:activity:7345635450084036608/?" target="_blank" class="timeline-link-btn">
              <i class="fa-solid fa-up-right-from-square"></i> View Post
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Timeline Item 2: GT OMSCS Graduation -->
    <div class="timeline-item">
      <div class="timeline-badge"><i class="fa-solid fa-graduation-cap"></i></div>
      <div class="timeline-card">
        <div class="timeline-card-header">
          <div class="timeline-meta">
            <span class="timeline-date"><i class="fa-solid fa-calendar-day fa-sm"></i> December 2024</span>
            <span class="timeline-category-tag academic">Academic Milestone</span>
          </div>
          <h3 class="timeline-title">Graduated from Georgia Institute of Technology (MSc in Computer Science)</h3>
        </div>
        <div class="timeline-image-wrapper">
          <img src="{{ '/assets/img/gt_graduation.png' | relative_url }}" alt="Georgia Tech OMSCS Graduation" class="timeline-image" loading="lazy">
        </div>
        <div class="timeline-card-body">
          <p>Graduated with my <strong>Master of Science in Computer Science</strong> (Machine Learning specialization) from the <strong>Georgia Institute of Technology (OMSCS)</strong>, earning a 3.8 GPA while working full-time.</p>
          <p>During the program I also led the Shanghai student chapter, supporting incoming students and organizing local meetings. Grateful for the support of family, friends, and colleagues along the way.</p>
          <div class="timeline-footer">
            <div class="timeline-tags">
              <span class="timeline-tag">#OMSCS</span>
              <span class="timeline-tag">#GeorgiaTech</span>
              <span class="timeline-tag">#Graduation</span>
              <span class="timeline-tag">#MachineLearning</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>

<style>
/* Activity Dashboard Styling */
.activity-feed {
  margin-top: 2rem;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2.5rem;
  border-bottom: 1px solid var(--global-divider-color);
  padding-bottom: 1.5rem;
}

.activity-subtitle {
  color: var(--global-text-color-light);
  font-size: 1.05rem;
  margin: 0;
  flex: 1;
  min-width: 280px;
}

.linkedin-follow-btn {
  background: #0077b5;
  color: #fff !important;
  border: none;
  padding: 0.55rem 1.25rem;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none !important;
  box-shadow: 0 4px 10px rgba(0, 119, 181, 0.2);
  transition: all 0.2s ease;
}

.linkedin-follow-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(0, 119, 181, 0.3);
  background: #006396;
}

/* Timeline Layout */
.timeline {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem 0;
}

/* Vertical line */
.timeline::after {
  content: '';
  position: absolute;
  width: 2px;
  background: var(--global-divider-color);
  top: 0;
  bottom: 0;
  left: 2rem;
  margin-left: -1px;
}

.timeline-item {
  position: relative;
  margin-bottom: 3rem;
  padding-left: 4.5rem;
}

/* Timeline Badge/Circle */
.timeline-badge {
  position: absolute;
  width: 2.75rem;
  height: 2.75rem;
  left: 0.65rem;
  top: 0;
  border-radius: 50%;
  background: var(--global-card-bg-color);
  border: 2px solid var(--global-theme-color);
  color: var(--global-theme-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  z-index: 1;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

/* Timeline Card */
.timeline-card {
  background: var(--global-card-bg-color);
  border: 1px solid var(--global-divider-color);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  overflow: hidden;
  transition: all 0.25s ease;
}

.timeline-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  border-color: var(--global-theme-color);
}

.timeline-card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--global-divider-color);
}

.timeline-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.timeline-date {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--global-text-color-light);
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.timeline-category-tag {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
}

.timeline-category-tag.conference {
  background: rgba(131, 56, 236, 0.08);
  color: var(--global-theme-color);
}

.timeline-category-tag.academic {
  background: rgba(15, 157, 88, 0.08);
  color: #0f9d58;
}

.timeline-title {
  font-size: 1.25rem;
  font-weight: 750;
  color: var(--global-text-color);
  margin: 0;
  line-height: 1.4;
}

.timeline-image-wrapper {
  max-height: 380px;
  overflow: hidden;
  background: var(--global-bg-color);
  border-bottom: 1px solid var(--global-divider-color);
  display: flex;
  justify-content: center;
  align-items: center;
}

.timeline-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.timeline-card:hover .timeline-image {
  transform: scale(1.02);
}

.timeline-card-body {
  padding: 1.5rem;
}

.timeline-card-body p {
  font-size: 0.925rem;
  line-height: 1.6;
  color: var(--global-text-color-light);
  margin-bottom: 1.25rem;
}

.timeline-card-body p strong {
  color: var(--global-text-color);
}

.timeline-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  border-top: 1px solid var(--global-divider-color);
  padding-top: 1rem;
  margin-top: 1.5rem;
}

.timeline-tags {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.timeline-tag {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--global-text-color-light);
  background: var(--global-bg-color);
  border: 1px solid var(--global-divider-color);
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
}

.timeline-link-btn {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--global-theme-color);
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  text-decoration: none !important;
  transition: color 0.15s ease;
}

.timeline-link-btn:hover {
  color: var(--global-text-color);
}

/* Mobile Responsiveness */
@media (max-width: 576px) {
  .timeline::after {
    left: 1.25rem;
  }
  
  .timeline-item {
    padding-left: 3rem;
  }
  
  .timeline-badge {
    width: 2.25rem;
    height: 2.25rem;
    left: 0.15rem;
    font-size: 0.95rem;
  }
}
</style>
