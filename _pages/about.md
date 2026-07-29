---
layout: about
title: About
permalink: /
subtitle: ECE PhD Researcher | Georgia Institute of Technology

profile:
  align: right
  image: PersonalPhoto.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>School of Electrical & Computer Engineering</p>
    <p>Georgia Institute of Technology</p>
    <p>Atlanta, GA 30332</p>

selected_papers: false # rendered inline below instead, so the contact block sits after the evidence
social: false # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder
---

I spent eight years inside an EDA vendor watching which parts of the semiconductor stack actually break in a fab. I am now an ECE PhD Researcher at the **Georgia Institute of Technology**, advised by Prof. Ali Adibi, working on the same problems from the physics side.

My research direction is **hardware-aware machine learning**, and I am moving toward **quantum error correction** as a longer-term target. Both rest on the same conviction: models that respect the physics of the device they run on beat models that treat it as an abstraction.

Before the PhD, I was at **Siemens Digital Industries Software** from 2017 to 2025, first as an IC Design Consultant based in Shanghai and then as a Principal Product Architect. I built OPC model-building automation and Resolution Enhancement Technique (RET) flows, developed computational models and test masks for technology ramps spanning nodes from 90 nm KrF to 5 nm ArF immersion, and led delivery across China, Europe, and the US, including one engagement with a Chinese fab that began as a one-month scope and became a six-year partnership. In the last stretch I architected LLM tooling for physical verification, which became my first publication.

I hold an MSc in Computer Science (Machine Learning specialization) from Georgia Tech and a BSc in Communication Systems Engineering with an Optics specialization from Ain Shams University, where I ranked first in the Optics track.

<div class="row justify-content-sm-center">
  <div class="col-sm-11 mt-4 mt-md-3">
    {% include figure.liquid loading="eager" path="assets/img/figures/research_venn.svg" alt="Venn diagram of three overlapping fields: machine learning, quantum computing, and semiconductor design. The machine learning and semiconductor overlap is labelled AI for EDA; the machine learning and quantum overlap is labelled ML for quantum error correction; the centre where all three meet is labelled as the PhD objective." title="Research positioning: machine learning, quantum computing, and semiconductor design" class="img-fluid" zoomable=true caption="My work sits across three fields. Only one pairwise area is work I have actually built: AI for EDA at Siemens. Machine learning for quantum error correction is the direction I am moving toward, not a record I can point at yet, and the centre where all three meet is the PhD objective." %}
  </div>
</div>

---

## Selected Work

- **[SVRF Copilot]({{ '/projects/1_dsl_copilot/' | relative_url }})**: AST-guided fine-tuning and retrieval-augmented generation for synthesizing physical verification code. Published at IEEE ICLAD 2025, where AST guidance improved code generation accuracy by up to 40% over text-based fine-tuning on a 741-example DRC benchmark.
- **[OPC and Inverse Lithography]({{ '/projects/7_opc_inverse_lithography/' | relative_url }})**: GPU-accelerated inverse lithography and model-based OPC for sub-14 nm nodes, formulated so that edge placement, process window, and mask manufacturability are optimized together rather than traded silently.
- **[ML TCAD Process Modeling]({{ '/projects/8_process_modeling/' | relative_url }})**: Fourier Neural Operator surrogates for etch and deposition simulation, built to make process-window exploration interactive rather than overnight.

The full set is on the [projects page]({{ '/projects/' | relative_url }}), and my [CV]({{ '/cv/' | relative_url }}) has the complete record.

## Publication

<div class="publications">
{% bibliography --query @*[key=abdelmalak2025ast]* %}
</div>

---

## Contact Me

If you would like to discuss research, collaborations, or consulting opportunities, please feel free to reach out.

<div class="contact-grid">
  <a class="contact-card" href="mailto:abanoub_abdelmalak@gatech.edu">
    <div class="contact-icon"><i class="fa-solid fa-envelope"></i></div>
    <div class="contact-details">
      <strong>Email</strong>
      <span>abanoub_abdelmalak@gatech.edu</span>
    </div>
  </a>
  <a class="contact-card" href="https://linkedin.com/in/abanoub-wahib" target="_blank">
    <div class="contact-icon"><i class="fa-brands fa-linkedin"></i></div>
    <div class="contact-details">
      <strong>LinkedIn</strong>
      <span>abanoub-wahib</span>
    </div>
  </a>
  <a class="contact-card" href="https://scholar.google.com/citations?user=BI9VvmkAAAAJ" target="_blank">
    <div class="contact-icon"><i class="ai ai-google-scholar"></i></div>
    <div class="contact-details">
      <strong>Google Scholar</strong>
      <span>Publications</span>
    </div>
  </a>
  <a class="contact-card" href="https://github.com/AbanoubElkess" target="_blank">
    <div class="contact-icon"><i class="fa-brands fa-github"></i></div>
    <div class="contact-details">
      <strong>GitHub</strong>
      <span>AbanoubElkess</span>
    </div>
  </a>
  <div class="contact-card">
    <div class="contact-icon"><i class="fa-solid fa-location-dot"></i></div>
    <div class="contact-details">
      <strong>Office</strong>
      <span>School of ECE, Georgia Tech</span>
    </div>
  </div>
</div>
