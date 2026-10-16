(function (root) {
  "use strict";
  const categories = [
    { id: "comidas", label: "Comidas", icon: "🥗" },
    { id: "cenas", label: "Cenas", icon: "🍽️" },
    { id: "postres", label: "Postres y meriendas", icon: "🍫" },
    { id: "guarniciones", label: "Guarniciones", icon: "🥔" },
    { id: "tecnicas", label: "Técnicas y conservación", icon: "🥑" },
  ];
  const statuses = {
    pendiente: "Pendiente",
    vista: "Vista",
    cocinada: "Cocinada",
    repetiria: "La repetiría",
    dominada: "Dominada",
  };
  const normalize = (value) =>
    String(value || "")
      .toLocaleLowerCase("es")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  const escape = (value) =>
    String(value ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  function matches(recipe, filters, entry = {}) {
    const terms = normalize(filters.q).trim().split(/\s+/).filter(Boolean);
    // Exclude negative advice and extraction notes from positive search matches.
    const haystack = normalize(
      [
        recipe.title,
        recipe.short,
        categories.find((c) => c.id === recipe.categoryId)?.label,
        recipe.subcategory,
        ...(recipe.tags || []),
        ...(recipe.ingredients || []).map((i) => i.text),
      ].join(" "),
    );
    return (
      terms.every((t) => haystack.includes(t)) &&
      (!filters.category || recipe.categoryId === filters.category) &&
      (!filters.subcategory || recipe.subcategory === filters.subcategory) &&
      (!filters.need || recipe.facets.includes(filters.need)) &&
      (!filters.favorite || entry.favorite) &&
      (!filters.status || (entry.status || "pendiente") === filters.status)
    );
  }
  function remaining(timer, now = Date.now()) {
    if (timer.state === "running")
      return Math.max(0, Math.ceil((timer.endsAt - now) / 1000));
    return Math.max(0, timer.remaining || 0);
  }
  function formatTime(seconds) {
    const value = Math.max(0, Math.ceil(seconds));
    const h = Math.floor(value / 3600),
      m = Math.floor((value % 3600) / 60),
      s = value % 60;
    return (
      (h ? `${h}:${String(m).padStart(2, "0")}` : String(m)) +
      ":" +
      String(s).padStart(2, "0")
    );
  }
  function mediaUrl(recipe, base) {
    const url = new URL(recipe.video, base);
    if (recipe.videoRevision)
      url.searchParams.set("video", recipe.videoRevision);
    return url.href;
  }
  const api = {
    categories,
    statuses,
    normalize,
    escape,
    matches,
    remaining,
    formatTime,
    mediaUrl,
  };
  root.RecipeCore = api;
  if (typeof module !== "undefined") module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
