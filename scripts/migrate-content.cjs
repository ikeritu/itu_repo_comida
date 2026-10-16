// One-time conversion of the audited data. Future edits belong in data/recipes.json.
const fs = require("node:fs");
if (fs.existsSync("data/recipes.json"))
  throw Error("La fuente editorial ya existe");
const recipes = JSON.parse(
  fs.readFileSync("data/recetas_video_lab_v3.json", "utf8"),
);
const groups = {
  "01": ["postres", "Postres proteicos", ["dulce", "frio"]],
  "02": ["guarniciones", "Airfryer", ["rapido"]],
  "03": ["cenas", "Informales y entrantes", ["compartir"]],
  "04": ["tecnicas", "Conservación", ["conservar"]],
  "05": ["postres", "Infantil", ["dulce", "infantil"]],
  "06": ["comidas", "Ensaladas completas", ["frio", "cena", "batch"]],
  "07": ["cenas", "Proteicas rápidas", ["cena", "rapido"]],
  "08": ["comidas", "Ensaladas completas", ["frio", "cena", "batch"]],
};
for (const r of recipes) {
  [r.categoryId, r.subcategory, r.facets] = groups[r.id];
  r.legacyIds = {};
  for (const key of ["ingredients", "steps"]) {
    r[key] = r[key].map((text, index) => ({
      id: `${key === "steps" ? "paso" : "ing"}-${String(index + 1).padStart(2, "0")}`,
      text,
    }));
    r.legacyIds[key] = r[key].map((x) => x.id);
  }
  r.timers = (r.timers || []).map((t, i) => ({ ...t, id: `reloj-${i + 1}` }));
  r.servings = null;
  r.activeMinutes = null;
  r.totalMinutes = null;
  r.equipment = {
    "01": ["Cazo", "Nevera"],
    "02": ["Microondas", "Airfryer"],
    "03": ["Horno"],
    "04": ["Nevera"],
    "05": ["Airfryer u horno"],
    "06": ["Cazo", "Nevera"],
    "07": ["Procesador", "Airfryer u horno"],
    "08": ["Cazo"],
  }[r.id];
  r.review = {
    date: "2026-10-16",
    status: "partial",
    note: "Método documentado. Raciones y cantidades incompletas: pendientes de confirmar.",
  };
  r.origin = {
    kind: "video",
    note: "Receta documentada a partir de un vídeo; algunas cantidades son orientativas.",
  };
  r.transcript = null;
}
fs.writeFileSync("data/recipes.json", JSON.stringify(recipes, null, 2) + "\n");
