const fluxAppReady = (fn) => {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn, { once: true });
  } else {
    fn();
  }
};

fluxAppReady(() => {
  const grid = document.querySelector("#app-menu-grid");
  const pills = document.querySelector("#app-category-pills");
  const search = document.querySelector("#app-menu-search");
  let categories = [];
  let active = "all";
  let query = "";

  const esc = (value) => String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;"
  }[char]));

  const render = () => {
    if (!grid || !pills) return;
    const items = categories.flatMap((category) =>
      category.items.map((item) => ({ ...item, category: category.title, slug: category.slug }))
    ).filter((item) => {
      const matchesCategory = active === "all" || item.slug === active;
      const haystack = `${item.name} ${item.description} ${item.category}`.toLowerCase();
      return matchesCategory && haystack.includes(query);
    });

    grid.innerHTML = items.map((item) => `
      <article class="app-menu-item">
        <span>${esc(item.category)}</span>
        <h3>${esc(item.name)}</h3>
        <p>${esc(item.description)}</p>
        <a href="/online-ordering/" aria-label="Order ${esc(item.name)}">Order this</a>
      </article>
    `).join("") || `<p class="app-empty">No menu items match that search yet. Try wings, wraps, bowl, lemonade, or Flux.</p>`;
  };

  fetch("/assets/data/menu.json")
    .then((response) => response.json())
    .then((data) => {
      categories = data.categories || [];
      if (pills) {
        pills.innerHTML = [`<button class="is-active" type="button" data-category="all">All</button>`]
          .concat(categories.map((category) => `<button type="button" data-category="${esc(category.slug)}">${esc(category.title)}</button>`))
          .join("");
        pills.addEventListener("click", (event) => {
          const button = event.target.closest("button[data-category]");
          if (!button) return;
          active = button.dataset.category;
          pills.querySelectorAll("button").forEach((node) => node.classList.toggle("is-active", node === button));
          render();
        });
      }
      render();
    })
    .catch(() => {
      if (grid) grid.innerHTML = `<p class="app-empty">Menu could not load. Use the full menu page or order link.</p>`;
    });

  if (search) {
    search.addEventListener("input", () => {
      query = search.value.trim().toLowerCase();
      render();
    });
  }
});
