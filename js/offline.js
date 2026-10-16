(function () {
  "use strict";
  window.createRecipeOffline = function (recipes, notify, onChange) {
    const MEDIA = "recetario-video-lab-media-v4",
      downloads = new Map(),
      available = new Set();
    let registration = null,
      shellReady = false;
    const supported =
      location.protocol !== "file:" &&
      "caches" in window &&
      "serviceWorker" in navigator;
    const urlOf = (r) => RecipeCore.mediaUrl(r, location.href);
    async function refresh() {
      if (!supported) {
        onChange();
        return;
      }
      try {
        const cache = await caches.open(MEDIA);
        available.clear();
        for (const r of recipes.filter((r) => r.video))
          if (await cache.match(urlOf(r))) available.add(r.id);
        const shell = await caches.open(
          "recetario-video-lab-shell-" + document.documentElement.dataset.build,
        );
        shellReady =
          !!navigator.serviceWorker.controller &&
          !!(await shell.match(
            new URL("index.html", location.href).href
              .split("#")[0]
              .split("?")[0],
          ));
      } catch {
        shellReady = false;
        notify("El almacenamiento sin conexión no está disponible.");
      }
      onChange();
    }
    async function download(id) {
      if (!supported) {
        notify(
          "Para descargar vídeos, abre la web con conexión segura o en localhost.",
        );
        return;
      }
      const r = recipes.find((x) => x.id === id);
      if (!r?.video || downloads.has(id)) return;
      const controller = new AbortController();
      downloads.set(id, { controller, loaded: 0, total: r.videoBytes || 0 });
      onChange();
      try {
        const response = await fetch(urlOf(r), {
          signal: controller.signal,
          cache: "no-store",
        });
        if (response.status !== 200)
          throw Error("No se recibió el vídeo completo");
        const total =
          Number(response.headers.get("Content-Length")) || r.videoBytes || 0;
        const reader = response.body.getReader(),
          chunks = [];
        let size = 0;
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          chunks.push(value);
          size += value.byteLength;
          downloads.set(id, { controller, loaded: size, total });
          onChange();
        }
        if (
          (total && size !== total) ||
          (r.videoBytes && size !== r.videoBytes)
        )
          throw Error("Descarga incompleta");
        const blob = new Blob(chunks, { type: "video/mp4" });
        const cache = await caches.open(MEDIA);
        if (controller.signal.aborted)
          throw new DOMException("Cancelada", "AbortError");
        await cache.put(
          urlOf(r),
          new Response(blob, {
            headers: {
              "Content-Type": "video/mp4",
              "Content-Length": String(size),
            },
          }),
        );
        available.add(id);
        notify("Vídeo descargado. Ya puedes abrirlo sin conexión.");
      } catch (error) {
        notify(
          error.name === "AbortError"
            ? "Descarga cancelada."
            : `No se ha descargado el vídeo. ${error.name === "QuotaExceededError" ? "Falta espacio: elimina otro vídeo y reintenta." : "Comprueba la conexión y reintenta."}`,
        );
      } finally {
        downloads.delete(id);
        await refresh();
      }
    }
    async function remove(id) {
      try {
        const r = recipes.find((x) => x.id === id);
        await (await caches.open(MEDIA)).delete(urlOf(r));
        available.delete(id);
        notify("Descarga eliminada. La receta y el progreso se conservan.");
      } catch {
        notify("No se pudo eliminar la descarga.");
      }
      onChange();
    }
    async function init() {
      if (!supported) {
        onChange();
        return;
      }
      try {
        registration =
          await navigator.serviceWorker.register("service-worker.js");
        const waiting = () => {
          document.getElementById("updateNotice").hidden = !(
            registration.waiting && navigator.serviceWorker.controller
          );
        };
        waiting();
        registration.addEventListener("updatefound", () =>
          registration.installing?.addEventListener("statechange", () => {
            waiting();
            refresh();
          }),
        );
        navigator.serviceWorker.addEventListener("controllerchange", () => {
          waiting();
          refresh();
          if (sessionStorage.getItem("itu_update_requested")) {
            sessionStorage.removeItem("itu_update_requested");
            location.reload();
          } else if (document.documentElement.dataset.build)
            notify("La versión sin conexión está lista.");
        });
        navigator.serviceWorker.ready.then(refresh);
        await refresh();
      } catch {
        notify(
          "No se ha preparado el modo sin conexión. Puedes consultar las recetas mientras tengas red.",
        );
      }
    }
    window.addEventListener("online", refresh);
    window.addEventListener("offline", refresh);
    document.addEventListener("visibilitychange", () => {
      if (!document.hidden) refresh();
    });
    return {
      init,
      refresh,
      download,
      remove,
      available,
      downloads,
      get supported() {
        return supported;
      },
      get shellReady() {
        return shellReady;
      },
      cancel(id) {
        downloads.get(id)?.controller.abort();
      },
      update() {
        if (!registration?.waiting) return;
        sessionStorage.setItem("itu_update_requested", "1");
        registration.waiting.postMessage({ type: "ACTIVATE" });
      },
      async usage() {
        try {
          const estimate = await navigator.storage?.estimate();
          return estimate
            ? `${(estimate.usage / 1e6).toFixed(1)} MB usados en este origen (incluye otras aplicaciones).`
            : "";
        } catch {
          return "";
        }
      },
    };
  };
})();
