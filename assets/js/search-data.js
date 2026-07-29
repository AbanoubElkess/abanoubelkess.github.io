// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "About",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-projects",
          title: "Projects",
          description: "Research, industrial, and academic work in EDA, machine learning, and systems. Ordered by how much of each project a reader can independently check: published work first, then industrial deployment by depth, then academic work whose results trace to a cited report, then work with no results to report, and finally work that was designed but never built.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-publications",
          title: "Publications",
          description: "Publications by Abanoub E. Abdelmalak, grouped by category in reverse chronological order.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "Curriculum vitae of Abanoub E. Abdelmalak, ECE PhD Researcher at Georgia Tech working on hardware-aware machine learning and quantum error correction, and former Principal Product Architect at Siemens EDA.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "news-completed-my-msc-in-computer-science-machine-learning-specialization-at-georgia-tech",
          title: 'Completed my MSc in Computer Science (Machine Learning specialization) at Georgia Tech.',
          description: "",
          section: "News",},{id: "news-presented-an-ast-guided-llm-approach-for-svrf-code-synthesis-at-the-inaugural-ieee-international-conference-on-llm-aided-design-iclad-2025-stanford-university",
          title: 'Presented An AST-guided LLM Approach for SVRF Code Synthesis at the inaugural IEEE...',
          description: "",
          section: "News",},{id: "news-started-my-phd-in-electrical-amp-amp-computer-engineering-at-georgia-tech-advised-by-prof-ali-adibi",
          title: 'Started my PhD in Electrical &amp;amp;amp; Computer Engineering at Georgia Tech, advised by...',
          description: "",
          section: "News",},{id: "projects-tennis-match-winner-predictions",
          title: 'Tennis Match Winner Predictions',
          description: "Match-winner classifier for men&#39;s professional tennis, built on 16,049 filtered matches and 12 engineered features, deployed as an interactive Dash application.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/10_tennis_prediction/";
            },},{id: "projects-randomized-optimization-amp-clustering-benchmarks",
          title: 'Randomized Optimization &amp;amp; Clustering Benchmarks',
          description: "Two CS7641 studies benchmarking randomized search heuristics on discrete problems and neural network weights, and clustering with dimensionality reduction on stock and tennis datasets.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/11_randomized_optimization/";
            },},{id: "projects-online-fake-news-detection",
          title: 'Online Fake News Detection',
          description: "CS7643 Deep Learning team project combining pre-trained Transformer embeddings with convolutional feature extraction to classify news articles as reliable or fabricated.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/12_fake_news_detection/";
            },},{id: "projects-domain-specific-language-copilot",
          title: 'Domain Specific Language Copilot',
          description: "AST-guided fine-tuning and retrieval-augmented generation for synthesizing Standard Verification Rule Format (SVRF) code from natural language, evaluated on a 741-example DRC benchmark and published at IEEE ICLAD 2025.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_dsl_copilot/";
            },},{id: "projects-drc-amp-layout-verification-automation",
          title: 'DRC &amp;amp; Layout Verification Automation',
          description: "AI agentic flows and geometric engines to automate complex EDA physical verification and PDK validation.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_agent_solutions/";
            },},{id: "projects-sem-image-deep-learning-cleaning",
          title: 'SEM Image Deep Learning Cleaning',
          description: "Deep neural network pipelines and interactive dashboards to classify, filter, and clean Scanning Electron Microscope (SEM) data for chip metrology.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/3_sem_cleaning/";
            },},{id: "projects-big-data-quantum-mechanics",
          title: 'Big Data Quantum Mechanics',
          description: "High-throughput Density Functional Theory (DFT) simulations and equivariant GNN modeling for material adsorption energies.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/4_big_data_quantum/";
            },},{id: "projects-reinforcement-learning-for-stock-trading",
          title: 'Reinforcement Learning for Stock Trading',
          description: "Deep reinforcement learning models and non-stationary policy optimization engines for automated financial trading.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/5_rl_stock_trading/";
            },},{id: "projects-ai-kernel",
          title: 'AI Kernel',
          description: "Design study for an AI-first operating system: a polyglot microkernel with a Rust core and Python orchestration, specified around the scheduling problem that GPU-bound inference creates. Not yet built.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_ai_kernel/";
            },},{id: "projects-opc-amp-inverse-lithography",
          title: 'OPC &amp;amp; Inverse Lithography',
          description: "GPU-accelerated Inverse Lithography Technology (ILT) and model-based Optical Proximity Correction (OPC) optimization for sub-14nm semiconductor manufacturing nodes.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/7_opc_inverse_lithography/";
            },},{id: "projects-ml-tcad-process-modeling",
          title: 'ML TCAD Process Modeling',
          description: "Fourier Neural Operator surrogates for semiconductor process simulation (etch, deposition, CMP), built at Siemens EDA to make TCAD process-window exploration interactive rather than overnight.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/8_process_modeling/";
            },},{id: "projects-analog-ic-design-optimization",
          title: 'Analog IC Design Optimization',
          description: "Automated multi-objective optimization and geometric programming routines for analog integrated circuit sizing.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/9_analog_design/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%61%62%61%6E%6F%75%62_%61%62%64%65%6C%6D%61%6C%61%6B@%67%61%74%65%63%68.%65%64%75", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/AbanoubElkess", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=BI9VvmkAAAAJ", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/abanoub-wahib", "_blank");
        },
      },];
