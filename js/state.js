(function (root) {
  "use strict";
  const KEY = "itu_recetario_v4_state",
    OLD = "itu_recetario_video_lab_v3_state";
  const empty = () => ({ version: 4, recipes: {}, timers: {}, sound: false });
  function validate(value, recipes) {
    if (
      !value ||
      value.version !== 4 ||
      !value.recipes ||
      typeof value.recipes !== "object" ||
      Array.isArray(value.recipes)
    )
      throw Error("Formato de progreso no válido");
    const out = empty();
    for (const recipe of recipes) {
      const entry = value.recipes[recipe.id];
      if (!entry || typeof entry !== "object") continue;
      out.recipes[recipe.id] = {
        favorite: entry.favorite === true,
        status: Object.hasOwn(RecipeCore.statuses, entry.status)
          ? entry.status
          : "pendiente",
      };
      for (const key of ["ingredients", "steps"]) {
        const allowed = new Set(recipe[key].map((item) => item.id));
        out.recipes[recipe.id][key] = Array.isArray(entry[key])
          ? [...new Set(entry[key].filter((id) => allowed.has(id)))]
          : [];
      }
    }
    for (const [key, t] of Object.entries(value.timers || {})) {
      const recipe = recipes.find((r) =>
        r.timers.some((x) => `${r.id}-${x.id}` === key),
      );
      if (
        recipe &&
        t &&
        ["running", "paused", "done"].includes(t.state) &&
        Number.isFinite(t.remaining) &&
        t.remaining >= 0 &&
        t.remaining <= 604800 &&
        (t.state !== "running" ||
          (Number.isFinite(t.endsAt) &&
            t.endsAt > 0 &&
            t.endsAt <= Date.now() + 604800000))
      )
        out.timers[key] = {
          state: t.state,
          remaining: t.remaining,
          endsAt: t.endsAt || 0,
          acknowledged: t.acknowledged === true,
        };
    }
    out.sound = value.sound === true;
    return out;
  }
  function migrate(old, recipes) {
    const out = empty();
    if (!old || typeof old !== "object" || Array.isArray(old))
      throw Error("Progreso anterior no válido");
    for (const recipe of recipes) {
      const entry = old[recipe.id];
      if (!entry || typeof entry !== "object") continue;
      const migrated = {
        favorite: entry.favorite === true,
        status: entry.status,
        ingredients: [],
        steps: [],
      };
      for (const key of ["ingredients", "steps"]) {
        const checked =
          entry[key === "ingredients" ? "checkedIngredients" : "checkedSteps"];
        migrated[key] = (Array.isArray(checked) ? checked : [])
          .filter(Number.isInteger)
          .map((index) => recipe.legacyIds[key][index])
          .filter(Boolean);
      }
      out.recipes[recipe.id] = migrated;
    }
    return validate(out, recipes);
  }
  function create(storage, recipes, onError = () => {}) {
    let state = empty(),
      persistent = true;
    const warn = () => {
      persistent = false;
      onError(
        "No se ha podido guardar el progreso. Puedes seguir usando la web y exportar una copia.",
      );
    };
    const save = () => {
      try {
        storage.setItem(KEY, JSON.stringify(state));
        return true;
      } catch {
        warn();
        return false;
      }
    };
    try {
      const current = storage.getItem(KEY),
        old = storage.getItem(OLD);
      if (current) state = validate(JSON.parse(current), recipes);
      else if (old) {
        state = migrate(JSON.parse(old), recipes);
        save();
      }
    } catch {
      warn();
    }
    // Never erase the legacy key: it remains a recoverable pre-migration copy.
    return {
      get state() {
        return state;
      },
      get persistent() {
        return persistent;
      },
      save,
      entry(id) {
        return (state.recipes[id] ||= {
          favorite: false,
          status: "pendiente",
          ingredients: [],
          steps: [],
        });
      },
      preview(raw) {
        return validate(JSON.parse(raw), recipes);
      },
      sync(raw) {
        state = validate(JSON.parse(raw), recipes);
      },
      replace(next) {
        state = validate(next, recipes);
        return save();
      },
      reset() {
        state = empty();
        return save();
      },
    };
  }
  root.RecipeState = { create, validate, migrate, empty, KEY, OLD };
  if (typeof module !== "undefined") module.exports = root.RecipeState;
})(typeof window !== "undefined" ? window : globalThis);
