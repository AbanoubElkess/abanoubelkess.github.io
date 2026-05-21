/**
 * Interactive Particle Network (Constellation) Background
 *
 * Creates a high-performance, responsive background canvas with drifting nodes and connecting lines.
 * Dynamically adapts color and opacity based on active customizer theme and accent colors.
 * Optimized with performance safeguards (visibility checks, prefers-reduced-motion).
 */

(function () {
  "use strict";

  // Check for prefers-reduced-motion
  const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (motionQuery.matches) {
    return; // Respect accessibility settings
  }

  // Create canvas element
  const canvas = document.createElement("canvas");
  canvas.id = "interactive-bg-canvas";
  document.body.prepend(canvas);

  const ctx = canvas.getContext("2d");
  let particles = [];
  let mouse = { x: null, y: null, active: false };
  let animationId = null;
  let width = 0;
  let height = 0;

  // Configuration limits
  const maxDistance = 110; // Max distance for lines
  const mouseRadius = 150; // Mouse attraction radius

  // Initialize and resize canvas
  function resizeCanvas() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    initParticles();
  }

  // Particle Class definition
  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.45; // Low velocity for subtle drift
      this.vy = (Math.random() - 0.5) * 0.45;
      this.radius = Math.random() * 1.5 + 0.8; // Subtle size
    }

    update() {
      // Gentle drift
      this.x += this.vx;
      this.y += this.vy;

      // Wrap around edges smoothly
      if (this.x < -10) this.x = width + 10;
      else if (this.x > width + 10) this.x = -10;

      if (this.y < -10) this.y = height + 10;
      else if (this.y > height + 10) this.y = -10;

      // Mouse influence (attract slightly)
      if (mouse.active && mouse.x !== null) {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < mouseRadius) {
          // Attract factor based on proximity
          const force = ((mouseRadius - dist) / mouseRadius) * 0.05;
          this.vx += (dx / dist) * force;
          this.vy += (dy / dist) * force;

          // Cap max speed under mouse influence
          const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
          if (speed > 0.8) {
            this.vx = (this.vx / speed) * 0.8;
            this.vy = (this.vy / speed) * 0.8;
          }
        } else {
          // Slowly decay velocity back to normal limits
          this.vx *= 0.98;
          this.vy *= 0.98;
        }
      }
    }

    draw(color) {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
    }
  }

  // Initialize particle pool based on screen size
  function initParticles() {
    particles = [];
    // Adjust density for mobile vs desktop
    const area = width * height;
    const particleCount = Math.min(80, Math.floor(area / 18000));

    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }
  }

  // Animation Loop
  function animate() {
    if (document.hidden) {
      // Pause updates if tab is backgrounded
      animationId = requestAnimationFrame(animate);
      return;
    }

    ctx.clearRect(0, 0, width, height);

    // Read active style values from documentElement (customizer-updated)
    const computedStyle = getComputedStyle(document.documentElement);
    const themeColor = computedStyle.getPropertyValue("--global-theme-color").trim() || "#007acc";
    const textColor = computedStyle.getPropertyValue("--global-text-color").trim() || "#333333";

    // Draw lines between nearby particles
    for (let i = 0; i < particles.length; i++) {
      const p1 = particles[i];
      p1.update();

      // Draw particle itself (semi-transparent text color)
      ctx.globalAlpha = 0.12;
      p1.draw(textColor);

      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < maxDistance) {
          // Draw connecting line
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);

          // Fade line out as distance increases (using active accent color)
          ctx.globalAlpha = (1 - dist / maxDistance) * 0.08;
          ctx.strokeStyle = themeColor;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }

      // Draw line to mouse
      if (mouse.active && mouse.x !== null) {
        const dx = p1.x - mouse.x;
        const dy = p1.y - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < mouseRadius) {
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.globalAlpha = (1 - dist / mouseRadius) * 0.12;
          ctx.strokeStyle = themeColor;
          ctx.lineWidth = 1.0;
          ctx.stroke();
        }
      }
    }

    ctx.globalAlpha = 1.0; // Reset alpha
    animationId = requestAnimationFrame(animate);
  }

  // Event Listeners
  window.addEventListener("resize", resizeCanvas);

  window.addEventListener("mousemove", (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    mouse.active = true;
  });

  window.addEventListener("mouseleave", () => {
    mouse.x = null;
    mouse.y = null;
    mouse.active = false;
  });

  // Handle touch events on mobile
  window.addEventListener(
    "touchmove",
    (e) => {
      if (e.touches.length > 0) {
        mouse.x = e.touches[0].clientX;
        mouse.y = e.touches[0].clientY;
        mouse.active = true;
      }
    },
    { passive: true }
  );

  window.addEventListener("touchend", () => {
    mouse.x = null;
    mouse.y = null;
    mouse.active = false;
  });

  // Fire up setup
  resizeCanvas();
  animate();
})();
