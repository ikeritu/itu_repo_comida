const fs = require("node:fs"),
  path = require("node:path"),
  cp = require("node:child_process");
const root = path.resolve(__dirname, ".."),
  dir = path.join(root, ".preview", "legacy");
for (const file of [
  "index.html",
  "service-worker.js",
  "manifest.webmanifest",
  "data/recetas_video_lab_v3.json",
]) {
  const target = path.join(dir, file);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(
    target,
    cp.execFileSync(
      "git",
      ["show", "c1d665bb11b0747e4cca82d74902ddca16b0b63c:" + file],
      { cwd: root },
    ),
  );
}
fs.writeFileSync(path.join(dir, "active"), "legacy");
console.log(
  "Fixture v3.8 preparada. PREVIEW_FIXTURE=.preview/legacy activa el fixture. Quitar .preview/legacy/active cambia a v4.",
);
