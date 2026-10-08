from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path.cwd()
INDEX = ROOT / 'index.html'
SW = ROOT / 'service-worker.js'
README = ROOT / 'README.md'
MANIFEST = ROOT / 'MANIFEST_SHA256.md'


def fail(msg):
    print(f'ERROR: {msg}', file=sys.stderr)
    sys.exit(1)


def write(path, text):
    path.write_text(text, encoding='utf-8')


def bump_versions(text):
    text = text.replace('v3.5', 'v3.6')
    text = text.replace('v3-5', 'v3-6')
    return text


CSS = r'''
    .block-home{padding:22px;margin:26px 0 8px}.block-home .section-head{margin:0 0 14px}.block-intro{margin:.35rem 0 0;color:var(--muted);line-height:1.45}.recipe-blocks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.recipe-block{border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.42);padding:16px;display:grid;gap:12px}[data-theme="dark"] .recipe-block{background:rgba(255,255,255,.04)}.recipe-block-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}.recipe-block-head h3{margin:0;font-size:22px;line-height:1.05;letter-spacing:-.03em}.recipe-block-head p{margin:5px 0 0;color:var(--muted);font-size:14px;line-height:1.35}.block-count{border:1px solid var(--line);border-radius:999px;padding:6px 9px;color:var(--muted);font-size:12px;font-weight:900;white-space:nowrap}.block-items{display:grid;gap:8px}.block-item{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;text-decoration:none;border:1px solid var(--line);border-radius:16px;padding:10px;background:rgba(255,255,255,.46);transition:transform .15s ease,background .15s ease}[data-theme="dark"] .block-item{background:rgba(255,255,255,.04)}.block-item:hover{transform:translateY(-1px);background:var(--paper)}.block-emoji{font-size:26px}.block-item b{display:block;line-height:1.15}.block-item small{display:block;color:var(--muted);line-height:1.3;margin-top:3px}.block-status{font-size:12px;font-weight:950;color:var(--brand2);white-space:nowrap}.block-actions{display:flex;gap:8px;flex-wrap:wrap}.block-actions .btn{box-shadow:none}
'''

HTML = r'''
    <section class="panel block-home" aria-labelledby="bloques-title">
      <div class="section-head">
        <div>
          <h2 id="bloques-title">🧩 Elegir por bloques</h2>
          <p class="block-intro">Agrupación rápida para decidir sin recorrer todas las tarjetas: comidas frías, cenas proteicas, postres, guarniciones, técnicas y cenas informales.</p>
        </div>
        <div class="count" id="blockCount">Vista agrupada</div>
      </div>
      <div class="recipe-blocks" id="recipeBlocks"></div>
    </section>
'''

JS = r'''
    const HOME_BLOCKS = [
      {
        title: '🥗 Comidas frías y batch cooking',
        hint: 'Platos completos para dejar hechos o tomar fríos.',
        match: r => /ensalada|fr[ií]a|batch cooking/.test(blockText(r))
      },
      {
        title: '💪 Cenas proteicas rápidas',
        hint: 'Ideas saciantes con proteína como base.',
        match: r => /proteic|cottage|pollo|huevo|airfryer/.test(blockText(r))
      },
      {
        title: '🍫 Postres y meriendas',
        hint: 'Dulces, meriendas y recetas infantiles.',
        match: r => /postre|merienda|dulce|infantil/.test(blockText(r))
      },
      {
        title: '🍟 Guarniciones y bases',
        hint: 'Acompañamientos o bases para completar platos.',
        match: r => /guarnici[oó]n|patatas fritas/.test(blockText(r))
      },
      {
        title: '🧄 Cenas informales y entrantes',
        hint: 'Recetas más de capricho, compartir o fin de semana.',
        match: r => /cena informal|entrante|pan de ajo|trenza/.test(blockText(r))
      },
      {
        title: '🥑 Técnicas y trucos',
        hint: 'Conservación, trucos y preparaciones auxiliares.',
        match: r => /t[eé]cnica|truco|conservaci[oó]n|guacamole/.test(blockText(r))
      }
    ];
    const FALLBACK_BLOCK = { title:'🍽️ Otras recetas', hint:'Recetas que no encajan claramente en los bloques anteriores.' };
    function blockText(r) { return normalizeText([r.title, r.short, r.type, r.need, r.category, ...(r.tags||[])].join(' ')); }
    function blockStatus(r) {
      const entry = getEntry(r.id);
      if (entry.favorite) return '★ favorita';
      return STATE_LABELS[entry.status] || 'Pendiente';
    }
    function renderRecipeBlocks() {
      if (!els.recipeBlocks) return;
      const groups = HOME_BLOCKS.map(block => ({...block, recipes: []}));
      const other = {...FALLBACK_BLOCK, recipes: []};
      RECIPES.forEach(recipe => {
        const group = groups.find(block => block.match(recipe));
        (group || other).recipes.push(recipe);
      });
      const visibleGroups = [...groups, other].filter(group => group.recipes.length);
      const total = visibleGroups.reduce((sum, group) => sum + group.recipes.length, 0);
      const blockCount = document.getElementById('blockCount');
      if (blockCount) blockCount.textContent = `${visibleGroups.length} bloques · ${total} recetas`;
      els.recipeBlocks.innerHTML = visibleGroups.map(group => `
        <article class="recipe-block">
          <div class="recipe-block-head">
            <div><h3>${escapeHtml(group.title)}</h3><p>${escapeHtml(group.hint)}</p></div>
            <span class="block-count">${group.recipes.length}</span>
          </div>
          <div class="block-items">
            ${group.recipes.map(r => `<a class="block-item" href="#${slugFor(r)}">
              <span class="block-emoji">${escapeHtml(r.emoji)}</span>
              <span><b>${escapeHtml(r.title)}</b><small>${escapeHtml(r.short)}</small></span>
              <span class="block-status">${escapeHtml(blockStatus(r))}</span>
            </a>`).join('')}
          </div>
          <div class="block-actions"><a class="btn small" href="#rapidas-title">Ver tarjetas</a><a class="btn small primary" href="#fichas-completas">Ver fichas</a></div>
        </article>`).join('');
    }
'''


def update_index():
    text = INDEX.read_text(encoding='utf-8')
    text = bump_versions(text)

    if '.recipe-blocks{' not in text:
        marker = '    .toolbar{position:sticky;top:0;z-index:20;'
        if marker not in text:
            fail('No encuentro el marcador CSS de .toolbar')
        text = text.replace(marker, CSS + '\n' + marker)

    if 'id="recipeBlocks"' not in text:
        marker = '\n\n    <section class="panel toolbar" aria-label="Búsqueda y filtros">'
        if marker not in text:
            fail('No encuentro el punto de inserción HTML antes de toolbar')
        text = text.replace(marker, '\n' + HTML + marker, 1)

    if 'recipeBlocks: document.getElementById' not in text:
        old = "cards: document.getElementById('cards'), recipeList: document.getElementById('recipeList'), needList: document.getElementById('needList'),"
        new = "cards: document.getElementById('cards'), recipeList: document.getElementById('recipeList'), needList: document.getElementById('needList'), recipeBlocks: document.getElementById('recipeBlocks'),"
        if old not in text:
            fail('No encuentro el bloque de els para añadir recipeBlocks')
        text = text.replace(old, new, 1)

    if 'function renderRecipeBlocks()' not in text:
        marker = '    function renderAll() {\n'
        if marker not in text:
            fail('No encuentro renderAll')
        text = text.replace(marker, JS + '\n' + marker, 1)

    if 'renderRecipeBlocks();\n      const visible = filteredRecipes();' not in text:
        old = '    function renderAll() {\n      const visible = filteredRecipes();'
        new = '    function renderAll() {\n      renderRecipeBlocks();\n      const visible = filteredRecipes();'
        if old not in text:
            fail('No encuentro cabecera de renderAll para llamar a renderRecipeBlocks')
        text = text.replace(old, new, 1)

    write(INDEX, text)


def update_service_worker():
    text = SW.read_text(encoding='utf-8')
    text = bump_versions(text)
    write(SW, text)


def update_readme():
    if not README.exists():
        return
    text = README.read_text(encoding='utf-8')
    text = bump_versions(text)
    block = '''## Qué cambia en v3.6\n\n- Añadida sección inicial **Elegir por bloques** para agrupar recetas por uso: comidas frías, cenas proteicas, postres/meriendas, guarniciones, cenas informales y técnicas/trucos.\n- Cada bloque muestra recetas enlazadas a su ficha completa y conserva estado/favoritos.\n- Actualizada caché PWA a v3.6 para forzar refresco en móvil.\n\n'''
    if '## Qué cambia en v3.6' not in text:
        idx = text.find('## Qué cambia en v3.5')
        if idx != -1:
            text = text[:idx] + block + text[idx:]
        else:
            text += '\n\n' + block
    write(README, text)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def update_manifest():
    candidates = []
    for path in [ROOT / 'README.md']:
        if path.exists(): candidates.append(path)
    for folder, pattern in [('assets/thumbs', '*'), ('assets/videos', '*'), ('data', '*.json')]:
        d = ROOT / folder
        if d.exists(): candidates.extend(sorted([p for p in d.glob(pattern) if p.is_file()]))
    for path in [ROOT / 'index.html', ROOT / 'manifest.webmanifest']:
        if path.exists(): candidates.append(path)
    d = ROOT / 'recetas_md'
    if d.exists(): candidates.extend(sorted(d.glob('*.md')))
    for path in [ROOT / 'run_local.bat', ROOT / 'run_local.ps1', ROOT / 'service-worker.js']:
        if path.exists(): candidates.append(path)

    seen, ordered = set(), []
    for path in candidates:
        if path not in seen:
            ordered.append(path); seen.add(path)

    lines = ['# MANIFEST SHA256 — Recetario Video Lab v3.6', '', '| Archivo | SHA256 | Tamaño bytes |', '|---|---:|---:|']
    for path in ordered:
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f'| `{rel}` | `{sha256_file(path)}` | {path.stat().st_size} |')
    write(MANIFEST, '\n'.join(lines) + '\n')


def validate():
    text = INDEX.read_text(encoding='utf-8')
    for needle in ['Recetario Video Lab — Itu v3.6', 'id="recipeBlocks"', 'function renderRecipeBlocks()', "recetario-video-lab-v3-6"]:
        if needle not in text and needle not in SW.read_text(encoding='utf-8'):
            fail(f'Validación fallida: falta {needle}')
    m = re.search(r'<script id="recipes-data" type="application/json">(.*?)</script>', text, re.S)
    if not m:
        fail('No encuentro recipes-data')
    json.loads(m.group(1))
    data_path = ROOT / 'data' / 'recetas_video_lab_v3.json'
    if data_path.exists():
        json.loads(data_path.read_text(encoding='utf-8'))


def main():
    update_index()
    update_service_worker()
    update_readme()
    update_manifest()
    validate()
    print('OK: inicio agrupado por bloques aplicado y versión v3.6 generada.')


if __name__ == '__main__':
    main()
