from pathlib import Path
from urllib.parse import quote
import hashlib
import json
import re

ROOT = Path('.')

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fff7ed"/>
      <stop offset="1" stop-color="#fed7aa"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#g)"/>
  <circle cx="260" cy="230" r="132" fill="#f59e0b" opacity="0.22"/>
  <circle cx="1010" cy="520" r="180" fill="#d97706" opacity="0.16"/>
  <rect x="116" y="104" width="1048" height="512" rx="48" fill="#fffaf0" stroke="#d97706" stroke-width="8" opacity="0.94"/>
  <text x="640" y="260" text-anchor="middle" font-family="system-ui, Segoe UI, Arial" font-size="104" font-weight="900">🍕</text>
  <text x="640" y="378" text-anchor="middle" font-family="system-ui, Segoe UI, Arial" font-size="58" font-weight="900" fill="#7c2d12">Minipizzas de garbanzos</text>
  <text x="640" y="456" text-anchor="middle" font-family="system-ui, Segoe UI, Arial" font-size="38" font-weight="800" fill="#92400e">cottage · jamón cocido · queso</text>
  <text x="640" y="530" text-anchor="middle" font-family="system-ui, Segoe UI, Arial" font-size="30" font-weight="700" fill="#6d645b">Cena saciante y proteica</text>
</svg>'''

THUMB = "data:image/svg+xml;charset=utf-8," + quote(svg)

RECIPE = {
    "id": "07",
    "emoji": "🍕",
    "title": "Minipizzas de garbanzos, cottage, jamón y queso",
    "short": "Minipizzas proteicas y saciantes con base de garbanzos, huevo y queso cottage.",
    "type": "Cena / airfryer",
    "need": "Quiero una cena saciante y proteica",
    "category": "Cenas proteicas rápidas",
    "video": "",
    "thumb": THUMB,
    "confidence": "Media-alta: en el vídeo se distinguen 150 g de garbanzos cocidos, huevo, 2 cucharadas de queso cottage, sal, formación de minibases, cocción 12 minutos a 190 ºC, tomate, queso rallado y jamón cocido. El segundo golpe de calor no muestra un tiempo exacto, así que se indica de forma orientativa.",
    "ingredients": [
        "150 g de garbanzos cocidos.",
        "1 huevo.",
        "2 cucharadas de queso cottage.",
        "Sal.",
        "Tomate o salsa de tomate para cubrir las bases.",
        "Queso rallado.",
        "Jamón cocido extra en lonchas.",
        "Opcional: orégano u otras hierbas al gusto."
    ],
    "steps": [
        "Pon 150 g de garbanzos cocidos en una picadora o procesador.",
        "Añade el huevo.",
        "Añade 2 cucharadas de queso cottage.",
        "Añade sal en este momento, antes de triturar la base.",
        "Tritura hasta conseguir una masa densa y manejable.",
        "Coloca papel de horno en una bandeja o en la cubeta de la airfryer.",
        "Forma minibases redondas con ayuda de una cuchara, intentando que queden de grosor parecido.",
        "Cocina las bases 12 minutos a 190 ºC, en horno o airfryer, hasta que estén firmes y ligeramente doradas.",
        "Saca las bases con cuidado.",
        "Pon tomate o salsa de tomate sobre cada base.",
        "Añade queso rallado.",
        "Añade jamón cocido extra en trozos o lonchas pequeñas.",
        "Termina con un poco más de queso rallado por encima.",
        "Da otro golpe de calor hasta que el queso se funda y se gratine ligeramente. Como referencia, empieza revisando a los 3-5 minutos.",
        "Sirve caliente."
    ],
    "seasoning": "La sal se añade a la mezcla de garbanzos, huevo y queso cottage antes de triturar, para que la base quede sazonada por dentro. Si usas orégano u otras hierbas, añádelas sobre el tomate y el queso antes del segundo golpe de calor, o al final al servir.",
    "when_use": "Como cena rápida, saciante y proteica, especialmente cuando quieres algo tipo pizza sin hacer una masa tradicional.",
    "when_not": "No es la mejor opción si ese día ya has metido muchas legumbres, queso o embutido cocido. Tampoco conviene si buscas una cena muy ligera.",
    "tips": [
        "Escurre bien los garbanzos para que la masa no quede demasiado líquida.",
        "Haz las bases finas y similares entre sí para que se cocinen de forma uniforme.",
        "Si la masa queda muy blanda, déjala reposar unos minutos antes de formar las bases.",
        "El segundo golpe de calor es solo para fundir el queso y calentar el jamón; revisa pronto para que no se resequen.",
        "Puedes variar el topping con atún, pavo, verduras muy finas o champiñones laminados."
    ],
    "tags": [
        "garbanzos",
        "cottage",
        "huevo",
        "pizza",
        "jamón cocido",
        "queso",
        "airfryer",
        "proteica"
    ],
    "version": "v3.4",
    "timers": [
        {
            "label": "Cocción de minibases",
            "minutes": 12,
            "note": "A 190 ºC, hasta que estén firmes y ligeramente doradas."
        },
        {
            "label": "Golpe final de calor",
            "minutes": 4,
            "note": "Orientativo: el vídeo no muestra tiempo exacto; busca queso fundido y algo gratinado."
        }
    ],
    "difficulty": "Fácil",
    "menu_fit": "Sí, si encaja con la semana"
}

MD_TEXT = """# 🍕 Minipizzas de garbanzos, cottage, jamón y queso

Minipizzas proteicas y saciantes con base de garbanzos, huevo y queso cottage.

- **Tipo:** Cena / airfryer
- **Necesidad:** Quiero una cena saciante y proteica
- **Categoría:** Cenas proteicas rápidas
- **Dificultad:** Fácil
- **Vídeo local:** no incluido en el repo
- **Miniatura:** generada como marcador visual interno
- **Versión:** v3.4

## Confianza de extracción

Media-alta: en el vídeo se distinguen 150 g de garbanzos cocidos, huevo, 2 cucharadas de queso cottage, sal, formación de minibases, cocción 12 minutos a 190 ºC, tomate, queso rallado y jamón cocido. El segundo golpe de calor no muestra un tiempo exacto, así que se indica de forma orientativa.

## Ingredientes / material

- 150 g de garbanzos cocidos.
- 1 huevo.
- 2 cucharadas de queso cottage.
- Sal.
- Tomate o salsa de tomate para cubrir las bases.
- Queso rallado.
- Jamón cocido extra en lonchas.
- Opcional: orégano u otras hierbas al gusto.

## Paso a paso

1. Pon 150 g de garbanzos cocidos en una picadora o procesador.
2. Añade el huevo.
3. Añade 2 cucharadas de queso cottage.
4. Añade sal en este momento, antes de triturar la base.
5. Tritura hasta conseguir una masa densa y manejable.
6. Coloca papel de horno en una bandeja o en la cubeta de la airfryer.
7. Forma minibases redondas con ayuda de una cuchara, intentando que queden de grosor parecido.
8. Cocina las bases 12 minutos a 190 ºC, en horno o airfryer, hasta que estén firmes y ligeramente doradas.
9. Saca las bases con cuidado.
10. Pon tomate o salsa de tomate sobre cada base.
11. Añade queso rallado.
12. Añade jamón cocido extra en trozos o lonchas pequeñas.
13. Termina con un poco más de queso rallado por encima.
14. Da otro golpe de calor hasta que el queso se funda y se gratine ligeramente. Como referencia, empieza revisando a los 3-5 minutos.
15. Sirve caliente.

## 🧂 Cuándo añadir especias o sazonadores

La sal se añade a la mezcla de garbanzos, huevo y queso cottage antes de triturar, para que la base quede sazonada por dentro. Si usas orégano u otras hierbas, añádelas sobre el tomate y el queso antes del segundo golpe de calor, o al final al servir.

## Cuándo usarla

Como cena rápida, saciante y proteica, especialmente cuando quieres algo tipo pizza sin hacer una masa tradicional.

## Cuándo NO usarla

No es la mejor opción si ese día ya has metido muchas legumbres, queso o embutido cocido. Tampoco conviene si buscas una cena muy ligera.

## Consejos y ajustes

- Escurre bien los garbanzos para que la masa no quede demasiado líquida.
- Haz las bases finas y similares entre sí para que se cocinen de forma uniforme.
- Si la masa queda muy blanda, déjala reposar unos minutos antes de formar las bases.
- El segundo golpe de calor es solo para fundir el queso y calentar el jamón; revisa pronto para que no se resequen.
- Puedes variar el topping con atún, pavo, verduras muy finas o champiñones laminados.

## Temporizadores útiles

- **Cocción de minibases:** 12 min. A 190 ºC, hasta que estén firmes y ligeramente doradas.
- **Golpe final de calor:** 4 min. Orientativo: el vídeo no muestra tiempo exacto; busca queso fundido y algo gratinado.

## Etiquetas

`garbanzos` · `cottage` · `huevo` · `pizza` · `jamón cocido` · `queso` · `airfryer` · `proteica`
"""


def update_recipe_json(path: Path) -> None:
    recipes = json.loads(path.read_text(encoding='utf-8'))
    recipes = [r for r in recipes if r.get('id') != RECIPE['id']]
    recipes.append(RECIPE)
    path.write_text(json.dumps(recipes, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def update_index(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    pattern = re.compile(r'(<script id="recipes-data" type="application/json">)(.*?)(</script>)', re.S)
    match = pattern.search(text)
    if not match:
        raise RuntimeError('No se encontró el bloque recipes-data en index.html')
    recipes = json.loads(match.group(2))
    recipes = [r for r in recipes if r.get('id') != RECIPE['id']]
    recipes.append(RECIPE)
    inline_json = json.dumps(recipes, ensure_ascii=False, separators=(',', ':'))
    text = pattern.sub(lambda m: m.group(1) + inline_json + m.group(3), text)
    text = text.replace('Recetario Video Lab — Itu v3.3', 'Recetario Video Lab — Itu v3.4')
    text = text.replace('Recetario local · v3.3', 'Recetario local · v3.4')
    text = text.replace('Recetario Video Lab — v3.3 · vídeos locales y recetas manuales', 'Recetario Video Lab — v3.4 · vídeos locales y recetas manuales')
    path.write_text(text, encoding='utf-8')


def update_service_worker(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    text = re.sub(r"recetario-video-lab-v3-\d+", 'recetario-video-lab-v3-4', text)
    path.write_text(text, encoding='utf-8')


def update_readme(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    text = text.replace('# Recetario Video Lab — Itu v3.3', '# Recetario Video Lab — Itu v3.4')
    block = """## Qué cambia en v3.4

- Añadida receta 07: `Minipizzas de garbanzos, cottage, jamón y queso`.
- Receta extraída del vídeo adjunto y registrada en los datos del recetario.
- Añadida ficha Markdown completa con temporizadores y modo cocinar.
- Actualizada la caché PWA/offline a `recetario-video-lab-v3-4`.

"""
    if '## Qué cambia en v3.4' not in text:
        text = text.replace('## Qué cambia en v3.3\n', block + '## Qué cambia en v3.3\n')
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
    lines = ['# MANIFEST SHA256 — Recetario Video Lab v3.4', '', '| Archivo | SHA256 | Tamaño bytes |', '|---|---:|---:|']
    seen = set()
    for file_path in candidates:
        if not file_path.exists() or file_path in seen:
            continue
        seen.add(file_path)
        rel = file_path.relative_to(ROOT).as_posix()
        lines.append(f"| `{rel}` | `{sha256_file(file_path)}` | {file_path.stat().st_size} |")
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def validate() -> None:
    data = json.loads((ROOT / 'data' / 'recetas_video_lab_v3.json').read_text(encoding='utf-8'))
    assert any(r.get('id') == '07' for r in data), 'receta 07 ausente en JSON externo'
    index_text = (ROOT / 'index.html').read_text(encoding='utf-8')
    match = re.search(r'<script id="recipes-data" type="application/json">(.*?)</script>', index_text, re.S)
    assert match, 'bloque recipes-data ausente'
    embedded = json.loads(match.group(1))
    assert any(r.get('id') == '07' for r in embedded), 'receta 07 ausente en index.html'
    assert 'v3.4' in index_text, 'index.html no marca v3.4'


def main() -> None:
    update_recipe_json(ROOT / 'data' / 'recetas_video_lab_v3.json')
    update_index(ROOT / 'index.html')
    update_service_worker(ROOT / 'service-worker.js')
    update_readme(ROOT / 'README.md')
    md_path = ROOT / 'recetas_md' / '07_minipizzas_de_garbanzos_cottage_jamon_y_queso.md'
    md_path.write_text(MD_TEXT, encoding='utf-8')
    update_manifest(ROOT / 'MANIFEST_SHA256.md')
    validate()
    print('OK: receta 07 añadida al recetario.')


if __name__ == '__main__':
    main()
