from pathlib import Path
import re

root = Path('.')
index_path = root / 'index.html'
sw_path = root / 'service-worker.js'
readme_path = root / 'README.md'
manifest_path = root / 'MANIFEST_SHA256.md'

index = index_path.read_text(encoding='utf-8')

# Version bump to force PWA/mobile refresh
index = index.replace('v3.6', 'v3.7')
index = index.replace('recetario-video-lab-v3-6', 'recetario-video-lab-v3-7')

index = index.replace(
    'Agrupación rápida para decidir sin recorrer todas las tarjetas: comidas frías, cenas proteicas, postres, guarniciones, técnicas y cenas informales.',
    'Agrupación rápida para decidir sin recorrer todas las tarjetas. Cenas es ahora un bloque principal con subsecciones, para no duplicar categorías de cena.'
)

old_css_re = re.compile(r"\n    \.block-home\{padding:22px.*?\.block-actions \.btn\{box-shadow:none\}\n", re.S)
new_css = """
    .block-home{padding:22px;margin:26px 0 8px}.block-home .section-head{margin:0 0 14px}.block-intro{margin:.35rem 0 0;color:var(--muted);line-height:1.45}.recipe-blocks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.recipe-block{border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.42);padding:16px;display:grid;gap:12px}[data-theme="dark"] .recipe-block{background:rgba(255,255,255,.04)}.recipe-block-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}.recipe-block-head h3{margin:0;font-size:22px;line-height:1.05;letter-spacing:-.03em}.recipe-block-head p{margin:5px 0 0;color:var(--muted);font-size:14px;line-height:1.35}.block-count{border:1px solid var(--line);border-radius:999px;padding:6px 9px;color:var(--muted);font-size:12px;font-weight:900;white-space:nowrap}.block-items{display:grid;gap:8px}.block-item{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;text-decoration:none;border:1px solid var(--line);border-radius:16px;padding:10px;background:rgba(255,255,255,.46);transition:transform .15s ease,background .15s ease}[data-theme="dark"] .block-item{background:rgba(255,255,255,.04)}.block-item:hover{transform:translateY(-1px);background:var(--paper)}.block-emoji{font-size:26px}.block-item b{display:block;line-height:1.15}.block-item small{display:block;color:var(--muted);line-height:1.3;margin-top:3px}.block-status{font-size:12px;font-weight:950;color:var(--brand2);white-space:nowrap}.block-actions{display:flex;gap:8px;flex-wrap:wrap}.block-actions .btn{box-shadow:none}.recipe-subblocks{display:grid;gap:12px}.recipe-subblock{border:1px dashed var(--line);border-radius:18px;padding:12px;background:rgba(255,255,255,.26)}[data-theme="dark"] .recipe-subblock{background:rgba(255,255,255,.03)}.recipe-subblock-head{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;margin-bottom:9px}.recipe-subblock-head b{font-size:15px}.recipe-subblock-head small{display:block;color:var(--muted);line-height:1.3;margin-top:3px}.recipe-subblock .block-items{margin-top:8px}
"""
index, n_css = old_css_re.subn('\n' + new_css, index)
if n_css != 1:
    raise RuntimeError(f'CSS block replacement failed: {n_css}')

new_home_blocks = """
    const HOME_BLOCKS = [
      {
        title: '🥗 Comidas frías y batch cooking',
        hint: 'Platos completos para dejar hechos o tomar fríos.',
        match: r => /ensalada|fr[ií]a|batch cooking/.test(blockText(r))
      },
      {
        title: '🍽️ Cenas',
        hint: 'Todas las cenas agrupadas en un único bloque, con subsecciones internas.',
        match: r => /cena/.test(blockText(r)),
        fallbackChild: { title:'🍽️ Otras cenas', hint:'Cenas que no encajan claramente en las subsecciones anteriores.' },
        children: [
          {
            title: '💪 Proteicas rápidas',
            hint: 'Ideas saciantes con proteína como base.',
            match: r => /proteic|cottage|minipizza|pizza|pollo|huevo|airfryer/.test(blockText(r))
          },
          {
            title: '🧄 Informales y entrantes',
            hint: 'Recetas más de capricho, compartir o fin de semana.',
            match: r => /cena informal|entrante|pan de ajo|trenza/.test(blockText(r))
          }
        ]
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
        title: '🥑 Técnicas y trucos',
        hint: 'Conservación, trucos y preparaciones auxiliares.',
        match: r => /t[eé]cnica|truco|conservaci[oó]n|guacamole/.test(blockText(r))
      }
    ];
"""
index, n_blocks = re.subn(r"\n    const HOME_BLOCKS = \[.*?\n    \];\n", "\n" + new_home_blocks, index, count=1, flags=re.S)
if n_blocks != 1:
    raise RuntimeError(f'HOME_BLOCKS replacement failed: {n_blocks}')

new_render = r'''
    function renderRecipeBlocks() {
      if (!els.recipeBlocks) return;
      const groups = HOME_BLOCKS.map(block => ({
        ...block,
        recipes: [],
        children: (block.children || []).map(child => ({...child, recipes: []})),
        fallbackChild: block.fallbackChild ? {...block.fallbackChild, recipes: []} : null
      }));
      const other = {...FALLBACK_BLOCK, recipes: []};

      RECIPES.forEach(recipe => {
        let assigned = false;
        for (const group of groups) {
          if (group.children && group.children.length) {
            const child = group.children.find(sub => sub.match(recipe));
            if (child) {
              child.recipes.push(recipe);
              assigned = true;
              break;
            }
            if (group.match && group.match(recipe)) {
              (group.fallbackChild || group).recipes.push(recipe);
              assigned = true;
              break;
            }
          } else if (group.match(recipe)) {
            group.recipes.push(recipe);
            assigned = true;
            break;
          }
        }
        if (!assigned) other.recipes.push(recipe);
      });

      function groupTotal(group) {
        const childrenTotal = (group.children || []).reduce((sum, child) => sum + child.recipes.length, 0);
        const fallbackTotal = group.fallbackChild ? group.fallbackChild.recipes.length : 0;
        return group.recipes.length + childrenTotal + fallbackTotal;
      }
      function renderBlockItems(recipes) {
        return `<div class="block-items">
          ${recipes.map(r => `<a class="block-item" href="#${slugFor(r)}">
            <span class="block-emoji">${escapeHtml(r.emoji)}</span>
            <span><b>${escapeHtml(r.title)}</b><small>${escapeHtml(r.short)}</small></span>
            <span class="block-status">${escapeHtml(blockStatus(r))}</span>
          </a>`).join('')}
        </div>`;
      }
      function renderSubblock(sub) {
        if (!sub.recipes.length) return '';
        return `<section class="recipe-subblock">
          <div class="recipe-subblock-head">
            <span><b>${escapeHtml(sub.title)}</b><small>${escapeHtml(sub.hint || '')}</small></span>
            <span class="block-count">${sub.recipes.length}</span>
          </div>
          ${renderBlockItems(sub.recipes)}
        </section>`;
      }

      const visibleGroups = [...groups, other].filter(group => groupTotal(group));
      const total = visibleGroups.reduce((sum, group) => sum + groupTotal(group), 0);
      const blockCount = document.getElementById('blockCount');
      if (blockCount) blockCount.textContent = `${visibleGroups.length} bloques · ${total} recetas`;
      els.recipeBlocks.innerHTML = visibleGroups.map(group => {
        const totalInGroup = groupTotal(group);
        const nested = group.children && group.children.length
          ? `<div class="recipe-subblocks">${group.children.map(renderSubblock).join('')}${group.fallbackChild ? renderSubblock(group.fallbackChild) : ''}</div>`
          : renderBlockItems(group.recipes);
        return `<article class="recipe-block">
          <div class="recipe-block-head">
            <div><h3>${escapeHtml(group.title)}</h3><p>${escapeHtml(group.hint)}</p></div>
            <span class="block-count">${totalInGroup}</span>
          </div>
          ${nested}
          <div class="block-actions"><a class="btn small" href="#rapidas-title">Ver tarjetas</a><a class="btn small primary" href="#fichas-completas">Ver fichas</a></div>
        </article>`;
      }).join('');
    }

    function renderAll()'''
index, n_render = re.subn(r"\n    function renderRecipeBlocks\(\) \{.*?\n\n    function renderAll\(\)", "\n" + new_render, index, count=1, flags=re.S)
if n_render != 1:
    raise RuntimeError(f'renderRecipeBlocks replacement failed: {n_render}')

index_path.write_text(index, encoding='utf-8')

if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = sw.replace('recetario-video-lab-v3-6', 'recetario-video-lab-v3-7')
    sw_path.write_text(sw, encoding='utf-8')

if readme_path.exists():
    readme = readme_path.read_text(encoding='utf-8')
    readme = readme.replace('v3.6', 'v3.7')
    note = """## Qué cambia en v3.7\n\n- Reorganizada la vista de inicio: `Cenas` pasa a ser un bloque principal.\n- Las cenas se separan dentro del bloque en subsecciones, por ejemplo proteicas rápidas e informales/entrantes.\n- Se evita duplicar bloques de cena al mismo nivel.\n\n"""
    if '## Qué cambia en v3.7' not in readme:
        readme = note + readme
    readme_path.write_text(readme, encoding='utf-8')

if manifest_path.exists():
    manifest = manifest_path.read_text(encoding='utf-8')
    manifest = manifest.replace('v3.6', 'v3.7')
    manifest_path.write_text(manifest, encoding='utf-8')

print('OK: Cenas reorganizado como bloque principal con subsecciones. v3.7')
