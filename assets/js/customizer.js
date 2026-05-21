(function () {
  // 1. Immediately apply cached styles to prevent flash of unstyled content (FOUC)
  const cachedTheme = localStorage.getItem("user-theme");
  const cachedFont = localStorage.getItem("user-font") || "sans";
  const cachedAccent = localStorage.getItem("user-accent") || "default";

  if (cachedTheme) {
    document.documentElement.setAttribute("data-user-theme", cachedTheme);
  }
  document.documentElement.setAttribute("data-user-font", cachedFont);
  document.documentElement.setAttribute("data-user-accent", cachedAccent);

  // 2. Setup the UI creation and event handling on DOMContentLoaded
  document.addEventListener("DOMContentLoaded", () => {
    // Generate markup for floating widget button and settings panel
    const cogBtn = document.createElement("button");
    cogBtn.className = "customizer-cog-btn";
    cogBtn.id = "customizer-toggle";
    cogBtn.setAttribute("title", "Customize Page settings");
    cogBtn.setAttribute("aria-label", "Customize Page settings");
    cogBtn.innerHTML = '<i class="fa-solid fa-gear"></i>';

    const panel = document.createElement("div");
    panel.className = "customizer-panel";
    panel.id = "customizer-panel";
    panel.innerHTML = `
      <div class="customizer-section">
        <h6>Reading Mode</h6>
        <div class="customizer-options">
          <button class="customizer-opt-btn" data-theme="light" aria-label="Light mode">Light</button>
          <button class="customizer-opt-btn" data-theme="dark" aria-label="Dark mode">Dark</button>
          <button class="customizer-opt-btn" data-theme="sepia" aria-label="Sepia mode">Sepia</button>
          <button class="customizer-opt-btn" data-theme="nord" aria-label="Nord mode">Nord</button>
        </div>
      </div>
      <div class="customizer-section">
        <h6>Font Family</h6>
        <div class="customizer-options fonts-grid">
          <button class="customizer-opt-btn" data-font="sans" aria-label="Sans font">Sans</button>
          <button class="customizer-opt-btn" data-font="serif" aria-label="Serif font">Serif</button>
          <button class="customizer-opt-btn" data-font="mono" aria-label="Monospace font">Mono</button>
        </div>
      </div>
      <div class="customizer-section">
        <h6>Accent Color</h6>
        <div class="accent-options">
          <span class="accent-opt-dot dot-default" data-accent="default" title="Default accent" role="button" aria-label="Default accent"></span>
          <span class="accent-opt-dot dot-teal" data-accent="teal" title="Teal accent" role="button" aria-label="Teal accent"></span>
          <span class="accent-opt-dot dot-sapphire" data-accent="sapphire" title="Sapphire accent" role="button" aria-label="Sapphire accent"></span>
          <span class="accent-opt-dot dot-emerald" data-accent="emerald" title="Emerald accent" role="button" aria-label="Emerald accent"></span>
          <span class="accent-opt-dot dot-amber" data-accent="amber" title="Amber accent" role="button" aria-label="Amber accent"></span>
          <span class="accent-opt-dot dot-amethyst" data-accent="amethyst" title="Amethyst accent" role="button" aria-label="Amethyst accent"></span>
        </div>
      </div>
    `;

    document.body.appendChild(cogBtn);
    document.body.appendChild(panel);

    // Toggle panel visibility
    cogBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      panel.classList.toggle("open");
    });

    // Close panel when clicking outside
    document.addEventListener("click", (e) => {
      if (!panel.contains(e.target) && e.target !== cogBtn && !cogBtn.contains(e.target)) {
        panel.classList.remove("open");
      }
    });

    // Highlight current active options
    const updateActiveStates = () => {
      const activeTheme = localStorage.getItem("user-theme") || (document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light");
      const activeFont = localStorage.getItem("user-font") || "sans";
      const activeAccent = localStorage.getItem("user-accent") || "default";

      panel.querySelectorAll("[data-theme]").forEach((btn) => {
        btn.classList.toggle("active", btn.getAttribute("data-theme") === activeTheme);
      });

      panel.querySelectorAll("[data-font]").forEach((btn) => {
        btn.classList.toggle("active", btn.getAttribute("data-font") === activeFont);
      });

      panel.querySelectorAll("[data-accent]").forEach((dot) => {
        dot.classList.toggle("active", dot.getAttribute("data-accent") === activeAccent);
      });
    };

    updateActiveStates();

    // Theme Switcher handlers
    panel.querySelectorAll("[data-theme]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const theme = btn.getAttribute("data-theme");
        if (theme === "light" || theme === "dark") {
          localStorage.removeItem("user-theme");
          document.documentElement.removeAttribute("data-user-theme");
          if (typeof setThemeSetting === "function") {
            setThemeSetting(theme);
          } else {
            document.documentElement.setAttribute("data-theme", theme);
            localStorage.setItem("theme", theme);
          }
        } else {
          localStorage.setItem("user-theme", theme);
          document.documentElement.setAttribute("data-user-theme", theme);
          // Set primary theme-setting under-the-hood for matching component styles
          const companionTheme = theme === "nord" ? "dark" : "light";
          if (typeof setThemeSetting === "function") {
            setThemeSetting(companionTheme);
          } else {
            document.documentElement.setAttribute("data-theme", companionTheme);
            localStorage.setItem("theme", companionTheme);
          }
        }
        updateActiveStates();
      });
    });

    // Font Switcher handlers
    panel.querySelectorAll("[data-font]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const font = btn.getAttribute("data-font");
        localStorage.setItem("user-font", font);
        document.documentElement.setAttribute("data-user-font", font);
        updateActiveStates();
      });
    });

    // Accent Switcher handlers
    panel.querySelectorAll("[data-accent]").forEach((dot) => {
      dot.addEventListener("click", () => {
        const accent = dot.getAttribute("data-accent");
        localStorage.setItem("user-accent", accent);
        document.documentElement.setAttribute("data-user-accent", accent);
        updateActiveStates();
      });
    });

    // Sync state when built-in light-toggle changes
    const systemLightToggle = document.getElementById("light-toggle");
    if (systemLightToggle) {
      systemLightToggle.addEventListener("click", () => {
        // Clearing customizer's warm themes to align with toggle
        localStorage.removeItem("user-theme");
        document.documentElement.removeAttribute("data-user-theme");
        setTimeout(updateActiveStates, 50);
      });
    }
  });
})();
