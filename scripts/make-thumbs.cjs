const fs = require("node:fs"),
  cp = require("node:child_process");
const recipes = JSON.parse(fs.readFileSync("data/recipes.json", "utf8"));
// Sample near the end for a recognizable result, retaining original videos.
for (const r of recipes.filter((r) => r.video)) {
  const seconds = Number(
    cp.execFileSync(
      "ffprobe",
      [
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "csv=p=0",
        r.video,
      ],
      { encoding: "utf8" },
    ),
  );
  const file = `assets/thumbs/${r.id}_preview.webp`;
  const chosen = {
    "01": { time: 150, filter: "scale=640:-1,crop=640:400:0:260" },
    "02": { time: 105, filter: "scale=640:-1,crop=640:400:0:700" },
    "03": { time: 2 },
    "05": { time: 1 },
  }[r.id];
  cp.execFileSync("ffmpeg", [
    "-hide_banner",
    "-loglevel",
    "error",
    "-y",
    "-ss",
    String(chosen?.time ?? Math.max(0, seconds * 0.85)),
    "-i",
    r.video,
    "-frames:v",
    "1",
    "-vf",
    chosen?.filter ||
      "scale=640:400:force_original_aspect_ratio=increase,crop=640:400",
    "-quality",
    "80",
    file,
  ]);
  r.thumb = file;
}
fs.writeFileSync("data/recipes.json", JSON.stringify(recipes, null, 2) + "\n");
