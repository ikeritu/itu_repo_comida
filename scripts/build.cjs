const fs = require("node:fs"),
  path = require("node:path"),
  crypto = require("node:crypto");
const root = path.resolve(__dirname, "..");
process.chdir(root);
const core = require("../js/core.js");
const recipes = JSON.parse(fs.readFileSync("data/recipes.json", "utf8"));
const ids = new Set(),
  categories = new Set(core.categories.map((c) => c.id));
function assert(value, message) {
  if (!value) throw Error(message);
}
for (const r of recipes) {
  if (r.video) {
    const bytes = fs.readFileSync(r.video);
    r.videoBytes = bytes.length;
    r.videoRevision = crypto
      .createHash("sha256")
      .update(bytes)
      .digest("hex")
      .slice(0, 16);
  }
  assert(
    /^\d{2}$/.test(r.id) && !ids.has(r.id),
    "ID de receta inválido o duplicado",
  );
  ids.add(r.id);
  assert(categories.has(r.categoryId), `Categoría inválida: ${r.id}`);
  for (const key of ["title", "short", "subcategory", "confidence"])
    assert(
      typeof r[key] === "string" && r[key].trim(),
      `${key} vacío en ${r.id}`,
    );
  for (const key of ["steps", "ingredients"]) {
    assert(Array.isArray(r[key]) && r[key].length, `${key} vacío`);
    const seen = new Set();
    for (const item of r[key]) {
      assert(
        /^[a-z0-9-]+$/.test(item.id) && !seen.has(item.id) && item.text,
        `ID/texto de ${key} inválido`,
      );
      seen.add(item.id);
    }
  }
  assert(
    Array.isArray(r.facets) &&
      Array.isArray(r.tags) &&
      Array.isArray(r.equipment),
    "Etiquetas/equipo inválidos",
  );
  const timerIds = new Set();
  for (const t of r.timers) {
    assert(
      t.id &&
        !timerIds.has(t.id) &&
        Number.isFinite(t.minutes) &&
        t.minutes > 0 &&
        t.minutes <= 10080,
      "Temporizador inválido",
    );
    timerIds.add(t.id);
  }
  for (const file of [r.thumb, r.video, r.transcript].filter(Boolean))
    if (!file.startsWith("data:"))
      assert(
        !file.includes("..") && !path.isAbsolute(file) && fs.existsSync(file),
        `Archivo ausente o inválido: ${file}`,
      );
  for (const key of ["servings", "activeMinutes", "totalMinutes"])
    assert(
      r[key] === null || (Number.isFinite(r[key]) && r[key] > 0),
      `Dato no válido: ${key}`,
    );
}
const assets = [
  "css/app.css",
  "js/core.js",
  "js/state.js",
  "js/timers.js",
  "js/offline.js",
  "js/app.js",
  "manifest.webmanifest",
  "assets/icons/icon-192.png",
  "assets/icons/icon-512.png",
  "assets/icons/maskable-512.png",
];
const hash = crypto.createHash("sha256");
hash.update(JSON.stringify(recipes));
const thumbs = [
  ...new Set(recipes.map((r) => r.thumb).filter((t) => !t.startsWith("data:"))),
];
for (const file of [
  "data/recipes.json",
  "templates/index.html",
  "templates/service-worker.js",
  ...assets,
  ...thumbs,
]) {
  const bytes = fs.readFileSync(file);
  hash.update(
    /\.(png|jpg|webp)$/.test(file)
      ? bytes
      : Buffer.from(bytes.toString("utf8").replace(/\r\n/g, "\n")),
  );
}
const build = hash.digest("hex").slice(0, 12);
const output = new Map();
let html = fs
  .readFileSync("templates/index.html", "utf8")
  .replaceAll("__BUILD__", build)
  .replace("__RECIPES__", JSON.stringify(recipes).replace(/</g, "\\u003c"));
output.set("index.html", html);
const shell = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  ...assets
    .filter((x) => x !== "manifest.webmanifest")
    .map(
      (x) =>
        "./" +
        x +
        (x.startsWith("js/") || x.startsWith("css/") ? `?build=${build}` : ""),
    ),
  ...thumbs.map((x) => "./" + x),
];
output.set(
  "service-worker.js",
  fs
    .readFileSync("templates/service-worker.js", "utf8")
    .replace(
      "__CONFIG__",
      JSON.stringify({
        build,
        shell,
        videos: recipes
          .filter((r) => r.video)
          .map((r) => r.video + "?video=" + r.videoRevision),
      }),
    ),
);
// Compatibility output; never edit it by hand.
const legacy = recipes.map((r) => ({
  ...r,
  ingredients: r.ingredients.map((x) => x.text),
  steps: r.steps.map((x) => x.text),
}));
output.set(
  "data/recetas_video_lab_v3.json",
  JSON.stringify(legacy, null, 2) + "\n",
);
for (const r of recipes) {
  const existing = fs
    .readdirSync("recetas_md")
    .find((f) => f.startsWith(r.id + "_"));
  assert(existing, "Falta nombre de ficha Markdown");
  output.set(
    "recetas_md/" + existing,
    `<!-- Generado desde data/recipes.json. -->\n# ${r.emoji} ${r.title}\n\n${r.short}\n\nCategoría: ${core.categories.find((c) => c.id === r.categoryId).label} · ${r.subcategory}\n\n## Ingredientes\n\n${r.ingredients.map((x) => "- " + x.text).join("\n")}\n\n## Preparación\n\n${r.steps.map((x, i) => `${i + 1}. ${x.text}`).join("\n")}\n\n## Sazonadores\n\n${r.seasoning}\n\n## Temporizadores\n\n${r.timers.map((t) => `- ${t.label}: ${t.minutes} min. ${t.note}`).join("\n")}\n\n## Consejos\n\n${r.tips.map((t) => "- " + t).join("\n")}\n\n## Origen y límites\n\n${r.confidence}\n\n## Cuándo usarla\n\n${r.when_use}\n\n## Cuándo no usarla\n\n${r.when_not}\n\n${r.video ? "Vídeo: ../" + r.video : "Vídeo local no disponible."}\n`,
  );
}
const checking = process.argv.includes("--check");
for (const [file, content] of output) {
  if (checking)
    assert(
      fs.readFileSync(file, "utf8") === content,
      `Salida desactualizada: ${file}`,
    );
  else fs.writeFileSync(file, content);
}
const tracked = require("node:child_process")
  .execFileSync("git", ["ls-files"], { encoding: "utf8" })
  .trim()
  .split("\n");
const files = [
  ...new Set([...tracked, ...output.keys(), ...assets, "data/recipes.json"]),
]
  .filter((f) => f !== "MANIFEST_SHA256.md" && fs.existsSync(f))
  .sort();
const manifest =
  "# MANIFEST SHA256 — Recetario v4\n\nHuellas del contenido normalizado a LF para archivos de texto.\n\n| Archivo | SHA256 | Tamaño bytes |\n|---|---|---:|\n" +
  files
    .map((f) => {
      let data = fs.readFileSync(f);
      if (!/\.(png|jpg|mp4|webp)$/.test(f))
        data = Buffer.from(data.toString("utf8").replace(/\r\n/g, "\n"));
      return `| \`${f}\` | \`${crypto.createHash("sha256").update(data).digest("hex")}\` | ${data.length} |`;
    })
    .join("\n") +
  "\n";
if (checking) {
  assert(
    fs.readFileSync("MANIFEST_SHA256.md", "utf8").replace(/\r\n/g, "\n") === manifest,
    "MANIFEST_SHA256.md desactualizado: vuelve a generar las salidas",
  );
} else fs.writeFileSync("MANIFEST_SHA256.md", manifest);
console.log(
  `Datos válidos: ${recipes.length} recetas. Build ${build}. ${checking ? "Salidas verificadas." : "Salidas generadas."}`,
);
