(function () {
  "use strict";
  const C = RecipeCore,
    e = C.escape,
    recipes = JSON.parse(document.getElementById("recipes-data").textContent);
  const $ = (id) => document.getElementById(id),
    modal = $("cookModal");
  let toastHandle,
    selected = null,
    cookId = null,
    activator = null,
    importPreview = null,
    lastScroll = 0,
    routeKey = "",
    timers;
  function notify(message) {
    $("toast").textContent = message;
    $("toast").hidden = false;
    clearTimeout(toastHandle);
    toastHandle = setTimeout(() => ($("toast").hidden = true), 6000);
  }
  const storageError = (message) => {
    $("storageWarning").textContent = message;
    $("storageWarning").hidden = false;
  };
  let storage;
  try {
    storage = localStorage;
  } catch {
    storage = {
      getItem() {
        throw Error();
      },
      setItem() {
        throw Error();
      },
    };
  }
  const store = RecipeState.create(storage, recipes, storageError);
  const filters = {
    q: "",
    category: "",
    subcategory: "",
    need: "",
    status: "",
    favorite: false,
  };
  function readFilters() {
    const p = new URLSearchParams(location.search);
    filters.q = p.get("q") || "";
    filters.subcategory = p.get("subcategoria") || "";
    filters.category = C.categories.some((c) => c.id === p.get("categoria"))
      ? p.get("categoria")
      : "";
    filters.need = p.get("necesidad") || "";
    filters.status = Object.hasOwn(C.statuses, p.get("estado"))
      ? p.get("estado")
      : "";
    filters.favorite = p.get("favoritas") === "1";
    $("search").value = filters.q;
    $("needFilter").value = filters.need;
    $("stateFilter").value = filters.status;
    $("favoriteFilter").checked = filters.favorite;
  }
  function saveFilters() {
    const url = new URL(location.href);
    for (const [key, value] of Object.entries({
      q: filters.q,
      categoria: filters.category,
      subcategoria: filters.subcategory,
      necesidad: filters.need,
      estado: filters.status,
      favoritas: filters.favorite ? "1" : "",
    })) {
      value ? url.searchParams.set(key, value) : url.searchParams.delete(key);
    }
    history.replaceState(history.state, "", url);
  }
  const categoryName = (id) =>
    C.categories.find((c) => c.id === id)?.label || "";
  function options(id) {
    return Object.entries(C.statuses)
      .map(
        ([key, label]) =>
          `<option value="${key}" ${store.entry(id).status === key ? "selected" : ""}>${label}</option>`,
      )
      .join("");
  }
  function stateControls(r, context = "card") {
    const entry = store.entry(r.id),
      controlId = `state-${context}-${r.id}`;
    return `<div class="card-actions">
      ${context === "card" ? `<a href="#receta-${r.id}">Ver receta →</a>` : ""}
      <button class="favorite" data-action="favorite" data-id="${r.id}" aria-pressed="${entry.favorite}"
        aria-label="${entry.favorite ? "Quitar de favoritas" : "Marcar como favorita"}: ${e(r.title)}">${entry.favorite ? "★" : "☆"}</button>
      </div><label class="sr-only" for="${controlId}">Estado de ${e(r.title)}</label>
      <select class="state-select" id="${controlId}" data-status="${r.id}">${options(r.id)}</select>`;
  }
  function meta(r) {
    return `<span class="chip">${e(r.equipment.join(" · "))}</span>${r.totalMinutes ? `<span class="chip">${r.totalMinutes} min</span>` : ""}${r.servings ? `<span class="chip">${r.servings} raciones</span>` : ""}`;
  }
  function card(r, index) {
    return `<article class="card" data-card="${r.id}"><a class="card-image" href="#receta-${r.id}" aria-label="Abrir ${e(r.title)}"><img src="${e(r.thumb)}" alt="" width="640" height="400" loading="${index < 2 ? "eager" : "lazy"}" decoding="async"></a><div class="card-body"><p class="eyebrow">${e(categoryName(r.categoryId))} · ${e(r.subcategory)}</p><h3><a href="#receta-${r.id}">${e(r.title)}</a></h3><p>${e(r.short)}</p><div class="recipe-meta">${meta(r)}</div><p class="muted"><small>${r.totalMinutes ? "" : "Tiempo total por confirmar · "}${r.servings ? "" : "Raciones por confirmar"}</small></p>${stateControls(r)}</div></article>`;
  }
  function renderCategories() {
    const groups = [{ id: "", icon: "", label: "Todo" }, ...C.categories];
    $("categories").innerHTML = groups
      .map(
        (c) =>
          `<button type="button" data-category="${c.id}" aria-pressed="${filters.category === c.id}">${c.icon} ${e(c.label)} <span aria-hidden="true">${c.id ? recipes.filter((r) => r.categoryId === c.id).length : recipes.length}</span></button>`,
      )
      .join("");
  }
  function renderCatalog() {
    const visible = recipes.filter((r) =>
      C.matches(r, filters, store.entry(r.id)),
    );
    $("cards").innerHTML = visible.map(card).join("");
    $("count").textContent = `${visible.length} de ${recipes.length}`;
    $("emptyState").hidden = visible.length > 0;
    $("catalogTitle").textContent = filters.category
      ? categoryName(filters.category)
      : "Todas las recetas";
    const active = [
      filters.q ? `«${filters.q}»` : "",
      filters.need ? $("needFilter").selectedOptions[0]?.textContent : "",
      filters.favorite ? "Favoritas" : "",
      filters.status ? C.statuses[filters.status] : "",
    ].filter(Boolean);
    $("activeFilters").textContent = active.join(" · ") || "TU COLECCIÓN";
    for (const b of $("categories").querySelectorAll("button"))
      b.setAttribute(
        "aria-pressed",
        String(b.dataset.category === filters.category),
      );
    const sub = $("subcategories"),
      values = filters.category
        ? [
            ...new Set(
              recipes
                .filter((r) => r.categoryId === filters.category)
                .map((r) => r.subcategory),
            ),
          ]
        : [];
    const signature = filters.category + "|" + filters.subcategory;
    sub.hidden = values.length < 2;
    if (sub.dataset.signature !== signature) {
      sub.dataset.signature = signature;
      sub.innerHTML = ["", ...values]
        .map(
          (value) =>
            `<button data-subcategory="${e(value)}" aria-pressed="${filters.subcategory === value}">${e(value || "Todas las subsecciones")}</button>`,
        )
        .join("");
    }
  }
  function clear() {
    Object.assign(filters, {
      q: "",
      category: "",
      subcategory: "",
      need: "",
      status: "",
      favorite: false,
    });
    saveFilters();
    readFilters();
    renderCatalog();
    $("search").focus();
  }
  function updateStateControls(id) {
    const r = recipes.find((r) => r.id === id),
      entry = store.entry(id);
    for (const b of document.querySelectorAll(
      `[data-action="favorite"][data-id="${id}"]`,
    )) {
      b.textContent = entry.favorite ? "★" : "☆";
      b.setAttribute("aria-pressed", String(entry.favorite));
      b.setAttribute(
        "aria-label",
        `${entry.favorite ? "Quitar de favoritas" : "Marcar como favorita"}: ${r.title}`,
      );
    }
    for (const s of document.querySelectorAll(`[data-status="${id}"]`))
      s.value = entry.status;
    if (!selected && !C.matches(r, filters, entry)) {
      const card = document.querySelector(`[data-card="${id}"]`),
        hadFocus = card?.contains(document.activeElement),
        focusTarget =
          card?.nextElementSibling?.querySelector("a") ||
          card?.previousElementSibling?.querySelector("a");
      card?.remove();
      if (hadFocus) (focusTarget || $("catalogTitle")).focus();
      const count = $("cards").children.length;
      $("count").textContent = `${count} de ${recipes.length}`;
      $("emptyState").hidden = count > 0;
    }
  }
  function renderDetail(r) {
    selected = r.id;
    $("recipeDetail").innerHTML =
      `<header class="detail-heading"><p class="eyebrow">${e(categoryName(r.categoryId))} · ${e(r.subcategory)}</p><h1 id="detailTitle" tabindex="-1">${e(r.emoji)} ${e(r.title)}</h1><p>${e(r.short)}</p><div class="recipe-meta">${meta(r)}</div></header><div class="detail-layout"><div><div class="detail-media">${r.video ? `<video controls playsinline preload="none" poster="${e(r.thumb)}" aria-label="Vídeo de ${e(r.title)}"><source src="${e(C.mediaUrl(r, location.href))}" type="video/mp4">Abre el enlace al vídeo para reproducirlo.</video>` : `<img src="${e(r.thumb)}" alt="Ilustración de ${e(r.title)}" width="640" height="400">`}</div><div class="detail-actions"><button class="primary" data-action="cook" data-id="${r.id}">Cocinar paso a paso</button><button data-action="copy" data-id="${r.id}">Copiar ficha</button><button data-action="print">Imprimir receta</button></div>${stateControls(r, "detail")}<div class="offline-tools" id="downloadTools" data-id="${r.id}"></div><div class="notice"><strong>Antes de empezar</strong><p>${e(r.review.note)}</p><p>Raciones: ${r.servings || "por confirmar"}. Tiempo total: ${r.totalMinutes ? r.totalMinutes + " min" : "por confirmar"}.</p></div><details class="disclosure"><summary>Origen y detalles de la receta</summary><p>Origen: vídeo. ${r.video ? "Vídeo disponible en este recetario." : "El archivo de vídeo no está disponible en este recetario."}</p><p>${e(r.confidence)}</p></details>${r.video ? `<p><a href="${e(r.video)}" target="_blank" rel="noopener">Abrir vídeo original ↗</a></p><p class="muted"><small>Las instrucciones escritas recogen el método documentado. La transcripción audiovisual completa está pendiente de revisión.</small></p>` : ""}</div><div><section class="box"><h2>Ingredientes y material</h2><ul>${r.ingredients.map((i) => `<li>${e(i.text)}</li>`).join("")}</ul></section><section class="box"><h2>Preparación</h2><ol>${r.steps.map((i) => `<li>${e(i.text)}</li>`).join("")}</ol></section><section class="box"><h2>Cuándo sazonar</h2><p>${e(r.seasoning)}</p></section><section class="box"><h2>Consejos</h2><ul>${r.tips.map((x) => `<li>${e(x)}</li>`).join("")}</ul></section><details class="disclosure"><summary>Cómo encaja en tu menú</summary><p>${e(r.when_use)}</p><p>${e(r.when_not)}</p></details></div></div>`;
    renderDownloads();
    $("detailTitle").focus();
  }
  function route() {
    const id = /^#receta-(\d{2})$/.exec(location.hash)?.[1],
      r = recipes.find((x) => x.id === id);
    const next = id || "catalog";
    if (next === routeKey) return;
    routeKey = next;
    if (r) {
      $("catalogView").hidden = true;
      $("detailView").hidden = false;
      renderDetail(r);
      window.scrollTo(0, 0);
    } else {
      if (id) notify("Esa receta no existe. Aquí tienes el catálogo.");
      selected = null;
      $("catalogView").hidden = false;
      $("detailView").hidden = true;
      $("recipeDetail").innerHTML = "";
      readFilters();
      renderCatalog();
      if (location.hash) {
        $("catalogTitle").focus({ preventScroll: true });
        window.scrollTo(0, lastScroll);
      }
    }
  }
  function checkList(r, key) {
    const checked = store.entry(r.id)[key];
    return `<div class="checklist">${r[key].map((item, i) => `<label class="checkitem"><input type="checkbox" data-check="${key}" data-item="${item.id}" ${checked.includes(item.id) ? "checked" : ""}><span>${key === "steps" ? `${i + 1}. ` : ""}${e(item.text)}</span></label>`).join("")}</div>`;
  }
  function timerRow(r, t, context) {
    const key = `${r.id}-${t.id}`;
    return `<section class="timer-row" data-timer="${key}"><h3>${e(context === "active" ? r.title + " · " : "")}${e(t.label)}</h3><p class="muted">${e(t.note)}</p><div class="timer-time" aria-live="off"></div><span class="timer-state sr-only"></span><div class="timer-actions" data-id="${r.id}" data-clock="${t.id}"></div></section>`;
  }
  function openCook(id, button) {
    const r = recipes.find((r) => r.id === id);
    activator = button;
    cookId = id;
    $("cookTitle").textContent = r.title;
    $("cookBody").innerHTML =
      `<h3>Ingredientes</h3>${checkList(r, "ingredients")}<h3>Pasos</h3>${checkList(r, "steps")}<section class="box"><h3>Sazonadores</h3><p>${e(r.seasoning)}</p></section><h3>Temporizadores</h3>${r.timers.map((t) => timerRow(r, t, "cook")).join("")}<label class="toggle"><input id="timerSound" type="checkbox" ${store.state.sound ? "checked" : ""}> Sonido al terminar (con esta página abierta)</label><p class="muted"><small>El tiempo se recupera al volver. Con la aplicación cerrada o el dispositivo suspendido no se garantiza una alarma.</small></p><button data-action="resetRecipe" data-id="${id}">Reiniciar checks de esta receta</button>`;
    if (store.entry(id).status === "pendiente") {
      store.entry(id).status = "vista";
      store.save();
      updateStateControls(id);
    }
    renderTimers();
    modal.showModal();
  }
  function renderTimers() {
    const active = Object.keys(store.state.timers).filter(
        (k) => !store.state.timers[k].acknowledged,
      ),
      signature = active.join(",");
    if ($("activeTimers").dataset.signature !== signature) {
      $("activeTimers").dataset.signature = signature;
      $("activeTimers").innerHTML =
        "<h2>En la cocina</h2>" +
        recipes
          .flatMap((r) =>
            r.timers
              .filter((t) => active.includes(`${r.id}-${t.id}`))
              .map((t) => timerRow(r, t, "active")),
          )
          .join("");
    }
    $("activeTimers").hidden = !active.length;
    for (const row of document.querySelectorAll("[data-timer]")) {
      const key = row.dataset.timer,
        r = recipes.find((r) => key.startsWith(r.id + "-")),
        t = r.timers.find((t) => `${r.id}-${t.id}` === key),
        timer = store.state.timers[key],
        state = timer?.state || "idle";
      row.querySelector(".timer-time").textContent = C.formatTime(
        timer ? C.remaining(timer) : t.minutes * 60,
      );
      row.classList.toggle("timer-done", state === "done");
      row.querySelector(".timer-state").textContent =
        state === "done"
          ? "Terminado"
          : state === "paused"
            ? "En pausa"
            : state === "running"
              ? "En marcha"
              : "Sin iniciar";
      const actions = row.querySelector(".timer-actions");
      if (actions.dataset.state !== state) {
        const focusAction = actions.contains(document.activeElement)
          ? document.activeElement.dataset.timerAction
          : null;
        actions.dataset.state = state;
        const buttons =
          state === "idle"
            ? [["start", "Iniciar"]]
            : state === "running"
              ? [
                  ["pause", "Pausar"],
                  ["cancel", "Cancelar"],
                ]
              : state === "paused"
                ? [
                    ["resume", "Continuar"],
                    ["reset", "Reiniciar"],
                    ["cancel", "Cancelar"],
                  ]
                : [
                    ["ack", "Entendido"],
                    ["reset", "Preparar de nuevo"],
                  ];
        actions.innerHTML = buttons
          .map(
            ([action, label]) =>
              `<button data-timer-action="${action}" ${action === "start" || action === "resume" ? 'class="primary"' : ""}>${label}</button>`,
          )
          .join("");
        if (focusAction)
          actions
            .querySelector(`[data-timer-action="${focusAction}"]`)
            ?.focus() || actions.querySelector("button")?.focus();
      }
    }
  }
  const offline = createRecipeOffline(recipes, notify, () => {
    renderDownloads();
    $("offlineStatus").textContent =
      location.protocol === "file:"
        ? "Uso local · las descargas offline requieren localhost o HTTPS."
        : offline.shellReady
          ? "Recetas disponibles sin conexión en este navegador."
          : "Recetas sin conexión aún no preparadas. Mantén la conexión.";
  });
  function renderDownloads() {
    const el = $("downloadTools");
    if (!el) return;
    const r = recipes.find((r) => r.id === el.dataset.id);
    if (!r.video) {
      el.textContent = "Esta receta no tiene vídeo local.";
      return;
    }
    const downloading = offline.downloads.get(r.id),
      saved = offline.available.has(r.id),
      state = downloading ? "loading" : saved ? "saved" : "empty";
    if (el.dataset.state !== state) {
      el.dataset.state = state;
      el.innerHTML = `<p>${saved ? "✓ Vídeo descargado" : downloading ? "Descargando vídeo…" : `Vídeo sin descargar · ${(r.videoBytes / 1e6).toFixed(1)} MB`}</p><p class="download-progress" aria-live="off"></p>${offline.supported ? `<button data-action="${downloading ? "cancelDownload" : saved ? "removeDownload" : "download"}" data-id="${r.id}">${downloading ? "Cancelar descarga" : saved ? "Eliminar descarga" : "Descargar vídeo sin conexión"}</button>` : "<p>Abre la web en HTTPS o localhost para gestionar descargas.</p>"}`;
    }
    const progress = el.querySelector(".download-progress");
    if (progress)
      progress.textContent = downloading
        ? `${(downloading.loaded / 1e6).toFixed(1)} de ${(downloading.total / 1e6).toFixed(1)} MB`
        : "";
  }
  async function copy(id) {
    const r = recipes.find((r) => r.id === id),
      text = [
        r.title,
        "",
        r.short,
        "",
        "Ingredientes:",
        ...r.ingredients.map((i) => "- " + i.text),
        "",
        "Preparación:",
        ...r.steps.map((x, i) => `${i + 1}. ${x.text}`),
        "",
        "Sazonadores: " + r.seasoning,
        ...(r.video
          ? ["", "Vídeo: " + new URL(r.video, location.href).href]
          : []),
      ].join("\n");
    try {
      if (navigator.clipboard?.writeText)
        await navigator.clipboard.writeText(text);
      else {
        const area = document.createElement("textarea");
        area.value = text;
        document.body.append(area);
        area.select();
        const ok = document.execCommand("copy");
        area.remove();
        if (!ok) throw Error();
      }
      notify("Ficha copiada.");
    } catch {
      notify(
        "No se pudo copiar. Puedes seleccionar el texto de la ficha o imprimirla.",
      );
    }
  }
  document.addEventListener("click", async (event) => {
    const b = event.target.closest("button,[data-action]"),
      action = b?.dataset.action,
      id = b?.dataset.id;
    const link = event.target.closest('a[href^="#receta-"]');
    if (link && !selected) {
      lastScroll = scrollY;
      history.replaceState({ ...history.state, scroll: lastScroll }, "");
    }
    if (b?.hasAttribute("data-category")) {
      const focusedCategory = b.dataset.category;
      filters.category = focusedCategory;
      filters.subcategory = "";
      saveFilters();
      renderCatalog();
    }
    if (b?.hasAttribute("data-subcategory")) {
      filters.subcategory = b.dataset.subcategory;
      saveFilters();
      renderCatalog();
      $("subcategories").querySelector(`[aria-pressed="true"]`)?.focus();
    }
    if (b?.dataset.timerAction) {
      const parent = b.closest(".timer-actions"),
        r = recipes.find((r) => r.id === parent.dataset.id),
        t = r.timers.find((t) => t.id === parent.dataset.clock);
      timers.act(`${r.id}-${t.id}`, b.dataset.timerAction, t.minutes * 60);
      if (b.dataset.timerAction === "cancel" || b.dataset.timerAction === "ack")
        notify(
          b.dataset.timerAction === "cancel"
            ? "Temporizador cancelado."
            : "Fin del temporizador confirmado.",
        );
    }
    if (action === "favorite") {
      const entry = store.entry(id);
      entry.favorite = !entry.favorite;
      store.save();
      updateStateControls(id);
      notify(entry.favorite ? "Añadida a favoritas." : "Quitada de favoritas.");
    }
    if (action === "cook") openCook(id, b);
    if (action === "clear") clear();
    if (action === "copy") await copy(id);
    if (action === "print") window.print();
    if (action === "download") await offline.download(id);
    if (action === "cancelDownload") offline.cancel(id);
    if (action === "removeDownload") await offline.remove(id);
    if (
      action === "resetRecipe" &&
      confirm("¿Desmarcar ingredientes y pasos de esta receta?")
    ) {
      const entry = store.entry(id);
      entry.ingredients = [];
      entry.steps = [];
      store.save();
      for (const c of $("cookBody").querySelectorAll("[data-check]"))
        c.checked = false;
      notify("Checks de esta receta reiniciados.");
    }
  });
  document.addEventListener("change", (event) => {
    const target = event.target;
    if (target.dataset.status) {
      store.entry(target.dataset.status).status = target.value;
      store.save();
      updateStateControls(target.dataset.status);
      notify("Estado actualizado.");
    }
    if (target.dataset.check && cookId) {
      const entry = store.entry(cookId),
        key = target.dataset.check;
      entry[key] = target.checked
        ? [...new Set([...entry[key], target.dataset.item])]
        : entry[key].filter((x) => x !== target.dataset.item);
      store.save();
    }
    if (target.id === "timerSound") timers.sound(target.checked);
  });
  $("filters").addEventListener("submit", (event) => event.preventDefault());
  for (const id of ["search", "needFilter", "stateFilter", "favoriteFilter"])
    $(id).addEventListener("input", () => {
      filters.q = $("search").value;
      filters.need = $("needFilter").value;
      filters.status = $("stateFilter").value;
      filters.favorite = $("favoriteFilter").checked;
      saveFilters();
      renderCatalog();
    });
  $("clearFilters").addEventListener("click", clear);
  $("closeCook").addEventListener("click", () => modal.close());
  modal.addEventListener("close", () => {
    cookId = null;
    const target = activator?.isConnected
      ? activator
      : document.querySelector(`[data-action="cook"]`) ||
        $("detailTitle") ||
        $("catalogTitle");
    target.focus();
  });
  $("backCatalog").addEventListener("click", () => {
    lastScroll = history.state?.scroll ?? lastScroll;
  });
  function theme(dark) {
    document.documentElement.dataset.theme = dark ? "dark" : "";
    $("themeBtn").textContent = dark ? "Modo claro" : "Modo oscuro";
    $("themeBtn").setAttribute(
      "aria-label",
      `Cambiar a modo ${dark ? "claro" : "oscuro"}`,
    );
  }
  try {
    theme(storage.getItem("itu_recetario_video_lab_theme") === "dark");
  } catch {
    theme(false);
  }
  $("themeBtn").addEventListener("click", () => {
    const dark = document.documentElement.dataset.theme !== "dark";
    theme(dark);
    try {
      storage.setItem("itu_recetario_video_lab_theme", dark ? "dark" : "light");
    } catch {
      storageError("No se ha podido guardar el tema.");
    }
  });
  $("exportBtn").addEventListener("click", () => {
    const url = URL.createObjectURL(
        new Blob([JSON.stringify(store.state, null, 2)], {
          type: "application/json",
        }),
      ),
      a = document.createElement("a");
    a.href = url;
    a.download = "recetario-progreso.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  $("importFile").addEventListener("change", async (event) => {
    try {
      const file = event.target.files[0];
      if (!file) return;
      if (file.size > 1e6) throw Error();
      importPreview = store.preview(await file.text());
      $("importSummary").textContent =
        `El archivo contiene progreso de ${Object.keys(importPreview.recipes).length} recetas y ${Object.keys(importPreview.timers).length} temporizadores.`;
      $("importModal").showModal();
    } catch {
      notify("El archivo no tiene un formato de progreso compatible.");
    }
    event.target.value = "";
  });
  $("confirmImport").addEventListener("click", () => {
    const saved = store.replace(importPreview);
    $("importModal").close();
    renderCatalog();
    if (selected) renderDetail(recipes.find((r) => r.id === selected));
    timers.tick();
    notify(
      saved
        ? "Progreso importado."
        : "Importado para esta sesión. Exporta una copia: no se pudo guardar.",
    );
  });
  $("cancelImport").addEventListener("click", () => $("importModal").close());
  $("resetBtn").addEventListener("click", () => {
    if (
      confirm(
        "¿Borrar favoritas, estados, checks y temporizadores? Exporta una copia antes si quieres conservarlos.",
      )
    ) {
      const saved = store.reset();
      renderCatalog();
      if (selected) renderDetail(recipes.find((r) => r.id === selected));
      renderTimers();
      notify(
        saved
          ? "Progreso reiniciado."
          : "Progreso reiniciado solo para esta sesión.",
      );
    }
  });
  $("printAll").addEventListener("click", () => {
    if (selected) {
      location.hash = "inicio";
      requestAnimationFrame(() => window.print());
    } else window.print();
  });
  $("updateNow").addEventListener("click", () => {
    store.save();
    if (modal.open) modal.close();
    offline.update();
  });
  $("updateLater").addEventListener(
    "click",
    () => ($("updateNotice").hidden = true),
  );
  document.addEventListener("recipe-timer-done", () =>
    notify(
      "Temporizador terminado. Revisa el panel «En la cocina» y confirma el aviso.",
    ),
  );
  window.addEventListener("storage", (event) => {
    if (event.key !== RecipeState.KEY || !event.newValue) return;
    try {
      store.sync(event.newValue);
      for (const r of recipes) updateStateControls(r.id);
      if (!selected && !modal.open) renderCatalog();
      if (cookId)
        for (const check of $("cookBody").querySelectorAll("[data-check]"))
          check.checked = store
            .entry(cookId)
            [check.dataset.check].includes(check.dataset.item);
      renderTimers();
    } catch {
      storageError(
        "No se pudo leer el progreso de otra pestaña. Exporta una copia de esta sesión.",
      );
    }
  });
  window.addEventListener("hashchange", route);
  window.addEventListener("popstate", () => {
    readFilters();
    routeKey = "";
    route();
  });
  timers = createRecipeTimers(store, renderTimers);
  readFilters();
  renderCategories();
  route();
  timers.tick();
  offline.init();
  offline.usage().then((text) => ($("storageUsage").textContent = text));
})();
