from pathlib import Path
import json
import re
import hashlib
import sys

ROOT = Path.cwd()
VIDEO = "assets/videos/08_ensalada_big_mac_pasta_pollo.mp4"
RECIPE_ID = "08"
VERSION = "v3.8"
CACHE = "recetario-video-lab-v3-8"
DATA_PATH = ROOT / "data" / "recetas_video_lab_v3.json"
INDEX_PATH = ROOT / "index.html"
SW_PATH = ROOT / "service-worker.js"
MD_PATH = ROOT / "recetas_md" / "08_ensalada_big_mac_de_pasta_y_pollo.md"
README_PATH = ROOT / "README.md"
MANIFEST_PATH = ROOT / "MANIFEST_SHA256.md"


def fail(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def update_json_data():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    found = False
    for recipe in data:
        if recipe.get("id") == RECIPE_ID:
            recipe["video"] = VIDEO
            recipe["version"] = VERSION
            found = True
            break
    if not found:
        fail("No encuentro la receta 08 en data/recetas_video_lab_v3.json")
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def update_index(data):
    text = INDEX_PATH.read_text(encoding="utf-8")
    pattern = re.compile(r'(<script id="recipes-data" type="application/json">)(.*?)(</script>)', re.S)
    if not pattern.search(text):
        fail("No encuentro el bloque recipes-data en index.html")
    inline = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    text = pattern.sub(lambda m: m.group(1) + inline + m.group(3), text)
    text = re.sub(r"Recetario Video Lab — Itu v\d+\.\d+", f"Recetario Video Lab — Itu {VERSION}", text)
    text = re.sub(r"Recetario local · v\d+\.\d+", f"Recetario local · {VERSION}", text)
    text = re.sub(r"Recetario Video Lab — v\d+\.\d+ ·", f"Recetario Video Lab — {VERSION} ·", text)
    INDEX_PATH.write_text(text, encoding="utf-8")


def update_service_worker():
    text = SW_PATH.read_text(encoding="utf-8")
    text = re.sub(r"const CACHE_NAME = 'recetario-video-lab-v\d+-\d+';", f"const CACHE_NAME = '{CACHE}';", text)
    asset = f"'./{VIDEO}'"
    if asset not in text:
        marker = "'./assets/videos/06_ensalada_patata.mp4'"
        if marker in text:
            text = text.replace(marker, marker + ", " + asset)
        else:
            # Inserta justo antes del cierre de la lista ASSETS.
            text = text.replace("\n];", f",\n  {asset}\n];")
    SW_PATH.write_text(text, encoding="utf-8")


def update_markdown():
    text = MD_PATH.read_text(encoding="utf-8")
    text = text.replace("- **Vídeo local:** no incluido en el repo", f"- **Vídeo local:** `{VIDEO}`")
    if VIDEO not in text:
        text = text.replace("- **Miniatura:**", f"- **Vídeo local:** `{VIDEO}`\n- **Miniatura:**")
    text = re.sub(r"- \*\*Versión:\*\* v\d+\.\d+", f"- **Versión:** {VERSION}", text)
    MD_PATH.write_text(text, encoding="utf-8")


def update_readme():
    text = README_PATH.read_text(encoding="utf-8")
    text = re.sub(r"# Recetario Video Lab — Itu v\d+\.\d+", f"# Recetario Video Lab — Itu {VERSION}", text)
    block = """## Qué cambia en v3.8\n\n- Enlazado el vídeo local de la receta 08: `assets/videos/08_ensalada_big_mac_pasta_pollo.mp4`.\n- Actualizada la caché PWA para que el reproductor local detecte el nuevo vídeo.\n\n"""
    if "## Qué cambia en v3.8" not in text:
        m = re.search(r"## Qué cambia en v\d+\.\d+", text)
        if m:
            text = text[:m.start()] + block + text[m.start():]
        else:
            text += "\n\n" + block
    README_PATH.write_text(text, encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def update_manifest():
    candidates = [
        ROOT / "README.md",
        *sorted((ROOT / "assets" / "thumbs").glob("*")),
        *sorted((ROOT / "assets" / "videos").glob("*.mp4")),
        *sorted((ROOT / "data").glob("*.json")),
        ROOT / "index.html",
        ROOT / "manifest.webmanifest",
        *sorted((ROOT / "recetas_md").glob("*.md")),
        ROOT / "run_local.bat",
        ROOT / "run_local.ps1",
        ROOT / "service-worker.js",
    ]
    seen = set()
    lines = [
        f"# MANIFEST SHA256 — Recetario Video Lab {VERSION}",
        "",
        "| Archivo | SHA256 | Tamaño bytes |",
        "|---|---:|---:|",
    ]
    for path in candidates:
        if path.exists() and path not in seen:
            seen.add(path)
            rel = path.relative_to(ROOT).as_posix()
            lines.append(f"| `{rel}` | `{sha256_file(path)}` | {path.stat().st_size} |")
    MANIFEST_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(data):
    video_path = ROOT / VIDEO
    if not video_path.exists():
        fail(f"No existe el vídeo esperado: {VIDEO}")
    recipe = next((r for r in data if r.get("id") == RECIPE_ID), None)
    if not recipe or recipe.get("video") != VIDEO:
        fail("La receta 08 no apunta al vídeo en data JSON")
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    if VIDEO not in index_text:
        fail("El vídeo no aparece en index.html")
    sw_text = SW_PATH.read_text(encoding="utf-8")
    if VIDEO not in sw_text or CACHE not in sw_text:
        fail("El service worker no quedó actualizado")


def main():
    data = update_json_data()
    update_index(data)
    update_service_worker()
    update_markdown()
    update_readme()
    update_manifest()
    validate(data)
    print("OK: receta 08 enlazada al vídeo local y caché actualizada.")


if __name__ == "__main__":
    main()
