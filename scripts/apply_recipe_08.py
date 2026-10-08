# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib
import json
import re

ROOT = Path('.')
RECIPE = {
  "id": "08",
  "emoji": "🍔",
  "title": "Ensalada Big Mac de pasta y pollo",
  "short": "Ensalada fría tipo Big Mac, alta en proteína, con pasta, pollo, lechuga, pepinillos y salsa cremosa.",
  "type": "Comida / cena fría",
  "need": "Quiero una comida saciante y proteica",
  "category": "Ensaladas completas y cenas proteicas",
  "video": "",
  "thumb": "assets/thumbs/08_ensalada_big_mac_pasta_pollo.svg",
  "confidence": "Media-alta: el vídeo muestra con claridad la salsa tipo Big Mac y la mayoría de ingredientes. No aparecen cantidades exactas para todos los ingredientes, así que se dejan de forma operativa.",
  "ingredients": [
    "Yogur griego natural.",
    "Agua de pepinillos.",
    "Ketchup cero o ketchup ligero.",
    "Mostaza.",
    "Ajo en polvo.",
    "Pimentón.",
    "Sal.",
    "Pasta corta tipo tiburones, cocida y escurrida.",
    "Cebolla morada cortada fina.",
    "Pepinillos picados.",
    "Pollo cocido o cocinado, troceado o desmenuzado.",
    "Mucha lechuga troceada."
  ],
  "steps": [
    "Pon yogur griego natural en un bol grande.",
    "Añade un chorrito de agua de pepinillos para aligerar la salsa y darle sabor.",
    "Añade ketchup cero o ketchup ligero.",
    "Añade mostaza.",
    "Añade ajo en polvo, pimentón y sal.",
    "Remueve bien hasta obtener una salsa cremosa y uniforme tipo Big Mac.",
    "Añade la pasta corta cocida y escurrida.",
    "Añade cebolla morada cortada fina.",
    "Añade pepinillos picados.",
    "Añade pollo cocido o cocinado, troceado o desmenuzado.",
    "Añade mucha lechuga troceada.",
    "Mezcla todo muy bien hasta que la salsa cubra la pasta, el pollo y las verduras.",
    "Sirve fría o ligeramente templada, según prefieras."
  ],
  "seasoning": "La sal, el ajo en polvo y el pimentón se añaden al principio, dentro de la salsa de yogur, agua de pepinillos, ketchup y mostaza. Así el sabor queda repartido antes de incorporar la pasta, el pollo, la cebolla, los pepinillos y la lechuga.",
  "when_use": "Como comida fría completa, cena saciante o receta de batch cooking cuando quieres algo con sabor tipo hamburguesa pero en formato ensalada.",
  "when_not": "No es la mejor opción si no te gustan los pepinillos o si ese día ya has comido bastante pasta, salsas o pollo. Tampoco conviene dejarla muchas horas mezclada con la lechuga si quieres que siga crujiente.",
  "tips": [
    "Escurre bien la pasta antes de mezclar para que la salsa no se agüe.",
    "Si la vas a guardar, deja la lechuga aparte y añádela justo antes de comer.",
    "El agua de pepinillos es importante para el sabor Big Mac; añade poco a poco para no dejar la salsa líquida.",
    "Puedes usar pollo asado, pechuga cocida o pollo a la plancha troceado.",
    "Si quieres más sabor a hamburguesa, aumenta un poco la mostaza y el pepinillo."
  ],
  "tags": [
    "pasta",
    "pollo",
    "ensalada",
    "Big Mac",
    "yogur griego",
    "pepinillos",
    "lechuga",
    "proteica",
    "batch cooking"
  ],
  "version": "v3.5",
  "timers": [
    {
      "label": "Cocción de pasta",
      "minutes": 10,
      "note": "Tiempo orientativo: sigue el paquete y deja la pasta al dente."
    },
    {
      "label": "Reposo en nevera",
      "minutes": 20,
      "note": "Opcional, para tomarla más fría y asentada."
    }
  ],
  "difficulty": "Fácil",
  "menu_fit": "Sí, si encaja con la semana"
}
MD_TEXT = '# 🍔 Ensalada Big Mac de pasta y pollo\n\nEnsalada fría tipo Big Mac, alta en proteína, con pasta, pollo, lechuga, pepinillos y salsa cremosa.\n\n- **Tipo:** Comida / cena fría\n- **Necesidad:** Quiero una comida saciante y proteica\n- **Categoría:** Ensaladas completas y cenas proteicas\n- **Dificultad:** Fácil\n- **Vídeo local:** no incluido en el repo\n- **Miniatura:** `assets/thumbs/08_ensalada_big_mac_pasta_pollo.svg`\n- **Versión:** v3.5\n\n## Confianza de extracción\n\nMedia-alta: el vídeo muestra con claridad la salsa tipo Big Mac y la mayoría de ingredientes. No aparecen cantidades exactas para todos los ingredientes, así que se dejan de forma operativa.\n\n## Ingredientes / material\n\n- Yogur griego natural.\n- Agua de pepinillos.\n- Ketchup cero o ketchup ligero.\n- Mostaza.\n- Ajo en polvo.\n- Pimentón.\n- Sal.\n- Pasta corta tipo tiburones, cocida y escurrida.\n- Cebolla morada cortada fina.\n- Pepinillos picados.\n- Pollo cocido o cocinado, troceado o desmenuzado.\n- Mucha lechuga troceada.\n\n## Paso a paso\n\n1. Pon yogur griego natural en un bol grande.\n2. Añade un chorrito de agua de pepinillos para aligerar la salsa y darle sabor.\n3. Añade ketchup cero o ketchup ligero.\n4. Añade mostaza.\n5. Añade ajo en polvo, pimentón y sal.\n6. Remueve bien hasta obtener una salsa cremosa y uniforme tipo Big Mac.\n7. Añade la pasta corta cocida y escurrida.\n8. Añade cebolla morada cortada fina.\n9. Añade pepinillos picados.\n10. Añade pollo cocido o cocinado, troceado o desmenuzado.\n11. Añade mucha lechuga troceada.\n12. Mezcla todo muy bien hasta que la salsa cubra la pasta, el pollo y las verduras.\n13. Sirve fría o ligeramente templada, según prefieras.\n\n## 🧂 Cuándo añadir especias o sazonadores\n\nLa sal, el ajo en polvo y el pimentón se añaden al principio, dentro de la salsa de yogur, agua de pepinillos, ketchup y mostaza. Así el sabor queda repartido antes de incorporar la pasta, el pollo, la cebolla, los pepinillos y la lechuga.\n\n## Cuándo usarla\n\nComo comida fría completa, cena saciante o receta de batch cooking cuando quieres algo con sabor tipo hamburguesa pero en formato ensalada.\n\n## Cuándo NO usarla\n\nNo es la mejor opción si no te gustan los pepinillos o si ese día ya has comido bastante pasta, salsas o pollo. Tampoco conviene dejarla muchas horas mezclada con la lechuga si quieres que siga crujiente.\n\n## Consejos y ajustes\n\n- Escurre bien la pasta antes de mezclar para que la salsa no se agüe.\n- Si la vas a guardar, deja la lechuga aparte y añádela justo antes de comer.\n- El agua de pepinillos es importante para el sabor Big Mac; añade poco a poco para no dejar la salsa líquida.\n- Puedes usar pollo asado, pechuga cocida o pollo a la plancha troceado.\n- Si quieres más sabor a hamburguesa, aumenta un poco la mostaza y el pepinillo.\n\n## Temporizadores útiles\n\n- **Cocción de pasta:** 10 min. Tiempo orientativo: sigue el paquete y deja la pasta al dente.\n- **Reposo en nevera:** 20 min. Opcional, para tomarla más fría y asentada.\n\n## Etiquetas\n\n`pasta` · `pollo` · `ensalada` · `Big Mac` · `yogur griego` · `pepinillos` · `lechuga` · `proteica` · `batch cooking`\n'
SVG_TEXT = '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">\n  <defs>\n    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">\n      <stop offset="0" stop-color="#f59e0b"/>\n      <stop offset="0.55" stop-color="#d97706"/>\n      <stop offset="1" stop-color="#166534"/>\n    </linearGradient>\n    <filter id="s" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="12" stdDeviation="14" flood-opacity="0.25"/></filter>\n  </defs>\n  <rect width="1280" height="720" fill="url(#g)"/>\n  <circle cx="1050" cy="120" r="190" fill="rgba(255,255,255,.16)"/>\n  <circle cx="140" cy="620" r="230" fill="rgba(255,255,255,.14)"/>\n  <g filter="url(#s)">\n    <rect x="90" y="95" width="1100" height="530" rx="44" fill="#fff8ed" opacity="0.94"/>\n    <text x="150" y="230" font-size="116" font-family="system-ui,Segoe UI,Arial" font-weight="900">🍔🥗</text>\n    <text x="150" y="345" font-size="72" font-family="system-ui,Segoe UI,Arial" font-weight="900" fill="#24211e">Ensalada Big Mac</text>\n    <text x="150" y="430" font-size="52" font-family="system-ui,Segoe UI,Arial" font-weight="800" fill="#92400e">de pasta y pollo</text>\n    <text x="150" y="520" font-size="34" font-family="system-ui,Segoe UI,Arial" font-weight="700" fill="#6d645b">yogur · pepinillos · mostaza · lechuga</text>\n  </g>\n</svg>\n'


def update_recipes_json(path: Path) -> None:
    recipes = json.loads(path.read_text(encoding='utf-8'))
    recipes = [r for r in recipes if r.get('id') != RECIPE['id']]
    recipes.append(RECIPE)
    recipes.sort(key=lambda r: r.get('id', ''))
    path.write_text(json.dumps(recipes, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def update_index(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    pattern = re.compile(r'(<script id="recipes-data" type="application/json">)(.*?)(</script>)', re.S)
    match = pattern.search(text)
    if not match:
        raise RuntimeError('No se encontró recipes-data en index.html')
    recipes = json.loads(match.group(2))
    recipes = [r for r in recipes if r.get('id') != RECIPE['id']]
    recipes.append(RECIPE)
    recipes.sort(key=lambda r: r.get('id', ''))
    inline_json = json.dumps(recipes, ensure_ascii=False, separators=(',', ':'))
    text = pattern.sub(lambda m: m.group(1) + inline_json + m.group(3), text)
    text = re.sub(r'Recetario Video Lab — Itu v3\.\d+', 'Recetario Video Lab — Itu v3.5', text)
    text = re.sub(r'Recetario local · v3\.\d+', 'Recetario local · v3.5', text)
    text = re.sub(r'Recetario Video Lab — v3\.\d+ · vídeos locales y recetas manuales', 'Recetario Video Lab — v3.5 · vídeos locales y recetas manuales', text)
    path.write_text(text, encoding='utf-8')


def update_service_worker(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    text = re.sub(r"recetario-video-lab-v3-\d+", 'recetario-video-lab-v3-5', text)
    asset = "'./assets/thumbs/08_ensalada_big_mac_pasta_pollo.svg'"
    if asset not in text:
        anchor = "'./assets/videos/01_cremoso_chocolate_proteico.mp4'"
        if anchor in text:
            text = text.replace(anchor, asset + ",\n  " + anchor)
        else:
            text = text.replace('];', '  ' + asset + '\n];')
    path.write_text(text, encoding='utf-8')


def update_readme(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'# Recetario Video Lab — Itu v3\.\d+', '# Recetario Video Lab — Itu v3.5', text)
    block = """## Qué cambia en v3.5

- Añadida receta 08: `Ensalada Big Mac de pasta y pollo`.
- Añadida miniatura propia: `08_ensalada_big_mac_pasta_pollo.svg`.
- Actualizados datos, ficha Markdown y caché PWA/offline.
- La receta se ha extraído del vídeo subido; el vídeo local no se incluye en el repo.

"""
    if '## Qué cambia en v3.5' not in text:
        m = re.search(r'## Qué cambia en v3\.\d+', text)
        if m:
            text = text[:m.start()] + block + text[m.start():]
        else:
            text = text.rstrip() + '\n\n' + block
    path.write_text(text, encoding='utf-8')


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def update_manifest(path: Path) -> None:
    candidates = [
        ROOT / 'README.md',
        *sorted((ROOT / 'assets' / 'thumbs').glob('*')),
        *sorted((ROOT / 'assets' / 'videos').glob('*.mp4')),
        *sorted((ROOT / 'data').glob('*.json')),
        ROOT / 'index.html',
        ROOT / 'manifest.webmanifest',
        *sorted((ROOT / 'recetas_md').glob('*.md')),
        ROOT / 'run_local.bat',
        ROOT / 'run_local.ps1',
        ROOT / 'service-worker.js',
    ]
    lines = ['# MANIFEST SHA256 — Recetario Video Lab v3.5', '', '| Archivo | SHA256 | Tamaño bytes |', '|---|---:|---:|']
    seen = set()
    for file_path in candidates:
        if not file_path.exists() or file_path in seen or file_path.is_dir():
            continue
        seen.add(file_path)
        rel = file_path.relative_to(ROOT).as_posix()
        lines.append(f"| `{rel}` | `{sha256_file(file_path)}` | {file_path.stat().st_size} |")
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    thumb_path = ROOT / 'assets' / 'thumbs' / '08_ensalada_big_mac_pasta_pollo.svg'
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    thumb_path.write_text(SVG_TEXT, encoding='utf-8')
    md_path = ROOT / 'recetas_md' / '08_ensalada_big_mac_de_pasta_y_pollo.md'
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(MD_TEXT, encoding='utf-8')
    update_recipes_json(ROOT / 'data' / 'recetas_video_lab_v3.json')
    update_index(ROOT / 'index.html')
    update_service_worker(ROOT / 'service-worker.js')
    update_readme(ROOT / 'README.md')
    update_manifest(ROOT / 'MANIFEST_SHA256.md')
    data = json.loads((ROOT / 'data' / 'recetas_video_lab_v3.json').read_text(encoding='utf-8'))
    if not any(r.get('id') == '08' for r in data):
        raise RuntimeError('La receta 08 no se añadió al JSON externo')
    if 'Ensalada Big Mac de pasta y pollo' not in (ROOT / 'index.html').read_text(encoding='utf-8'):
        raise RuntimeError('La receta 08 no aparece en index.html')


if __name__ == '__main__':
    main()
