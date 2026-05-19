const ready = (fn) => {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn, { once: true });
  } else {
    fn();
  }
};

ready(() => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const next = !nav.classList.contains("is-open");
      nav.classList.toggle("is-open", next);
      toggle.setAttribute("aria-expanded", String(next));
    });
  }

  const observer = "IntersectionObserver" in window
    ? new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.18 })
    : null;

  document.querySelectorAll(".reveal").forEach((node) => {
    if (observer) {
      observer.observe(node);
    } else {
      node.classList.add("is-visible");
    }
  });

  const pills = Array.from(document.querySelectorAll(".filter-pill"));
  const cards = Array.from(document.querySelectorAll("[data-filter]"));

  if (pills.length && cards.length) {
    pills.forEach((pill) => {
      pill.addEventListener("click", () => {
        const filter = pill.getAttribute("data-filter");
        pills.forEach((item) => item.classList.toggle("is-active", item === pill));
        cards.forEach((card) => {
          const match = filter === "all" || card.getAttribute("data-filter") === filter;
          card.hidden = !match;
        });
      });
    });
  }
});
