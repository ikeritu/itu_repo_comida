from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path('.')

RECIPE = {
    "id": "06",
    "emoji": "🥔",
    "title": "Ensalada de patata con pollo, manzana verde y huevo",
    "short": "Plato frío, cremoso, saciante y proteico, con manzana verde en lugar de pepino.",
    "type": "Comida / cena fría",
    "need": "Quiero una comida saciante y proteica",
    "category": "Platos fríos y ensaladas completas",
    "video": "assets/videos/06_ensalada_patata.mp4",
    "thumb": "assets/thumbs/06_ensalada_patata.jpg",
    "confidence": "Media: se distinguen bien los ingredientes principales y el proceso general del vídeo. La versión final sustituye el pepino original por manzana verde por preferencia de Iker. Las cantidades exactas no se leen completas, así que se indican de forma operativa.",
    "ingredients": [
        "Patatas cocidas.",
        "Huevos cocidos.",
        "Manzana verde cortada en dados pequeños, en sustitución del pepino del vídeo.",
        "Pollo cocido desmenuzado o troceado.",
        "Zanahoria cocida en trozos.",
        "Yogur natural espeso o yogur griego natural.",
        "1 cucharada de mostaza.",
        "Un pequeño toque de mahonesa ligera.",
        "Opcional: sal y pimienta al gusto."
    ],
    "steps": [
        "Pon en un bol una base de yogur natural espeso o yogur griego.",
        "Añade una cucharada de mostaza.",
        "Añade un pequeño toque de mahonesa ligera.",
        "Mezcla bien hasta obtener una salsa cremosa y uniforme.",
        "Añade al bol las patatas cocidas.",
        "Añade huevo cocido.",
        "Añade manzana verde cortada en dados pequeños, mejor al final para que mantenga textura fresca y no se oxide demasiado.",
        "Añade pollo cocido.",
        "Añade también zanahoria cocida.",
        "Mezcla o corta ligeramente dentro del bol para integrar los ingredientes con la salsa.",
        "Ajusta la textura y remueve hasta que quede una ensalada cremosa.",
        "Sirve y decora con huevo cocido por encima."
    ],
    "seasoning": "La mostaza y la mahonesa ligera se añaden al inicio, mezcladas con el yogur para formar la salsa. Si decides añadir sal o pimienta, hazlo también en ese momento, antes de incorporar la patata, el pollo, la zanahoria y la manzana verde.",
    "when_use": "Como comida completa fría, cena saciante o plato de batch cooking para dejar hecho con antelación.",
    "when_not": "No es la mejor opción si buscas una cena muy ligera o si el menú de ese día ya lleva bastante patata, huevo o salsas cremosas.",
    "tips": [
        "La manzana verde sustituye al pepino del vídeo: aporta frescor, un punto ácido y textura crujiente.",
        "Añade la manzana en dados pequeños y mézclala al final para que mantenga mejor la textura.",
        "Si quieres una textura más ligera, usa yogur natural alto en proteína o yogur griego ligero.",
        "Puedes dejar algunos trozos grandes de patata o chafarlos un poco para que la salsa quede más integrada.",
        "Se puede guardar en nevera y servir fría."
    ],
    "tags": ["patata", "pollo", "huevo", "manzana verde", "ensalada", "fría", "proteica", "batch cooking"],
    "version": "v3.3",
    "timers": [
        {"label": "Cocción de patatas", "minutes": 20, "note": "Tiempo orientativo, según tamaño y tipo de patata."},
        {"label": "Cocción de huevos", "minutes": 10, "note": "Tiempo orientativo para huevo cocido."},
        {"label": "Enfriado en nevera", "minutes": 30, "note": "Opcional, si quieres tomarla bien fría."}
    ],
    "difficulty": "Fácil",
    "menu_fit": "Sí, si encaja con la semana"
}

MD_TEXT = """# 🥔 Ensalada de patata con pollo, manzana verde y huevo

Plato frío, cremoso, saciante y proteico, con manzana verde en lugar de pepino.

- **Tipo:** Comida / cena fría
- **Necesidad:** Quiero una comida saciante y proteica
- **Categoría:** Platos fríos y ensaladas completas
- **Dificultad:** Fácil
- **Vídeo local:** `assets/videos/06_ensalada_patata.mp4`
- **Miniatura:** `assets/thumbs/06_ensalada_patata.jpg`
- **Versión:** v3.3

## Confianza de extracción

Media: se distinguen bien los ingredientes principales y el proceso general del vídeo. La versión final sustituye el pepino original por manzana verde por preferencia de Iker. Las cantidades exactas no se leen completas, así que se indican de forma operativa.

## Ingredientes / material

- Patatas cocidas.
- Huevos cocidos.
- Manzana verde cortada en dados pequeños, en sustitución del pepino del vídeo.
- Pollo cocido desmenuzado o troceado.
- Zanahoria cocida en trozos.
- Yogur natural espeso o yogur griego natural.
- 1 cucharada de mostaza.
- Un pequeño toque de mahonesa ligera.
- Opcional: sal y pimienta al gusto.

## Paso a paso

1. Pon en un bol una base de yogur natural espeso o yogur griego.
2. Añade una cucharada de mostaza.
3. Añade un pequeño toque de mahonesa ligera.
4. Mezcla bien hasta obtener una salsa cremosa y uniforme.
5. Añade al bol las patatas cocidas.
6. Añade huevo cocido.
7. Añade manzana verde cortada en dados pequeños, mejor al final para que mantenga textura fresca y no se oxide demasiado.
8. Añade pollo cocido.
9. Añade también zanahoria cocida.
10. Mezcla o corta ligeramente dentro del bol para integrar los ingredientes con la salsa.
11. Ajusta la textura y remueve hasta que quede una ensalada cremosa.
12. Sirve y decora con huevo cocido por encima.

## 🧂 Cuándo añadir especias o sazonadores

La mostaza y la mahonesa ligera se añaden al inicio, mezcladas con el yogur para formar la salsa. Si decides añadir sal o pimienta, hazlo también en ese momento, antes de incorporar la patata, el pollo, la zanahoria y la manzana verde.

## Cuándo usarla

Como comida completa fría, cena saciante o plato de batch cooking para dejar hecho con antelación.

## Cuándo NO usarla

No es la mejor opción si buscas una cena muy ligera o si el menú de ese día ya lleva bastante patata, huevo o salsas cremosas.

## Consejos y ajustes

- La manzana verde sustituye al pepino del vídeo: aporta frescor, un punto ácido y textura crujiente.
- Añade la manzana en dados pequeños y mézclala al final para que mantenga mejor la textura.
- Si quieres una textura más ligera, usa yogur natural alto en proteína o yogur griego ligero.
- Puedes dejar algunos trozos grandes de patata o chafarlos un poco para que la salsa quede más integrada.
- Se puede guardar en nevera y servir fría.

## Temporizadores útiles

- **Cocción de patatas:** 20 min. Tiempo orientativo, según tamaño y tipo de patata.
- **Cocción de huevos:** 10 min. Tiempo orientativo para huevo cocido.
- **Enfriado en nevera:** 30 min. Opcional, si quieres tomarla bien fría.

## Etiquetas

`patata` · `pollo` · `huevo` · `manzana verde` · `ensalada` · `fría` · `proteica` · `batch cooking`
"""


def write_recipe_json(path: Path) -> None:
    recipes = json.loads(path.read_text(encoding='utf-8'))
    recipes = [r for r in recipes if r.get('id') != '06']
    recipes.append(RECIPE)
    path.write_text(json.dumps(recipes, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def update_index(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    pattern = re.compile(r'(<script id="recipes-data" type="application/json">)(.*?)(</script>)', re.S)
    match = pattern.search(text)
    if not match:
        raise RuntimeError('No se encontró recipes-data en index.html')
    recipes = json.loads(match.group(2))
    recipes = [r for r in recipes if r.get('id') != '06']
    recipes.append(RECIPE)
    inline_json = json.dumps(recipes, ensure_ascii=False, separators=(',', ':'))
    text = pattern.sub(lambda m: m.group(1) + inline_json + m.group(3), text)
    text = text.replace('Recetario Video Lab — Itu v3.2', 'Recetario Video Lab — Itu v3.3')
    text = text.replace('Recetario local · v3.2', 'Recetario local · v3.3')
    text = text.replace('Recetario Video Lab — v3.2 · vídeos locales y recetas manuales', 'Recetario Video Lab — v3.3 · vídeos locales y recetas manuales')
    path.write_text(text, encoding='utf-8')


def update_service_worker(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    text = re.sub(r"recetario-video-lab-v3-\d+", 'recetario-video-lab-v3-3', text)
    thumb_asset = "'./assets/thumbs/06_ensalada_patata.jpg'"
    video_asset = "'./assets/videos/06_ensalada_patata.mp4'"
    if thumb_asset not in text:
        text = text.replace("'./assets/thumbs/05_tartitas_infantiles_yogur_frambuesas.jpg'", "'./assets/thumbs/05_tartitas_infantiles_yogur_frambuesas.jpg', " + thumb_asset)
    if video_asset not in text:
        text = text.replace("'./assets/videos/05_tartitas_infantiles_yogur_frambuesas.mp4'", "'./assets/videos/05_tartitas_infantiles_yogur_frambuesas.mp4', " + video_asset)
    path.write_text(text, encoding='utf-8')


def update_readme(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    text = text.replace('# Recetario Video Lab — Itu v3.2', '# Recetario Video Lab — Itu v3.3')
    block = """## Qué cambia en v3.3

- Añadida receta 06: `Ensalada de patata con pollo, manzana verde y huevo`.
- Enlazado el vídeo local: `06_ensalada_patata.mp4`.
- Añadida miniatura propia de la receta.
- Actualizados datos, ficha Markdown y caché PWA/offline.
- Adaptada la receta sustituyendo el pepino del vídeo por manzana verde.

"""
    if '## Qué cambia en v3.3' not in text:
        text = text.replace('## Qué cambia en v3.2\n', block + '## Qué cambia en v3.2\n')
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
        *sorted((ROOT / 'assets' / 'thumbs').glob('*.jpg')),
        *sorted((ROOT / 'assets' / 'videos').glob('*.mp4')),
        *sorted((ROOT / 'data').glob('*.json')),
        ROOT / 'index.html',
        ROOT / 'manifest.webmanifest',
        *sorted((ROOT / 'recetas_md').glob('*.md')),
        ROOT / 'run_local.bat',
        ROOT / 'run_local.ps1',
        ROOT / 'service-worker.js',
    ]
    lines = ['# MANIFEST SHA256 — Recetario Video Lab v3.3', '', '| Archivo | SHA256 | Tamaño bytes |', '|---|---:|---:|']
    seen = set()
    for file_path in candidates:
        if not file_path.exists() or file_path in seen:
            continue
        seen.add(file_path)
        rel = file_path.relative_to(ROOT).as_posix()
        lines.append(f"| `{rel}` | `{sha256_file(file_path)}` | {file_path.stat().st_size} |")
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    video_path = ROOT / 'assets' / 'videos' / '06_ensalada_patata.mp4'
    if not video_path.exists():
        raise FileNotFoundError(video_path)

    thumb_path = ROOT / 'assets' / 'thumbs' / '06_ensalada_patata.jpg'
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-ss', '00:00:20', '-i', str(video_path), '-frames:v', '1', '-q:v', '3', str(thumb_path)], check=True)

    write_recipe_json(ROOT / 'data' / 'recetas_video_lab_v3.json')
    update_index(ROOT / 'index.html')
    update_service_worker(ROOT / 'service-worker.js')
    update_readme(ROOT / 'README.md')

    md_path = ROOT / 'recetas_md' / '06_ensalada_de_patata_con_pollo_manzana_verde_y_huevo.md'
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(MD_TEXT, encoding='utf-8')

    update_manifest(ROOT / 'MANIFEST_SHA256.md')

    embedded = re.search(r'<script id="recipes-data" type="application/json">(.*?)</script>', (ROOT / 'index.html').read_text(encoding='utf-8'), re.S)
    assert embedded, 'No recipes-data en index.html'
    assert any(r.get('id') == '06' for r in json.loads(embedded.group(1))), 'Receta 06 no embebida en index.html'
    assert any(r.get('id') == '06' for r in json.loads((ROOT / 'data' / 'recetas_video_lab_v3.json').read_text(encoding='utf-8'))), 'Receta 06 no está en data JSON'
    assert thumb_path.exists(), 'No se creó la miniatura'


if __name__ == '__main__':
    main()
