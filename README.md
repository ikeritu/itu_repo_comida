# 🍳 Recetario Video Lab — Itu v2

Mini web local con recetas extraídas de los 4 vídeos.

## Cómo usar

1. Descomprime el ZIP.
2. Abre `index.html` con doble clic.
3. Si algún navegador no reproduce los vídeos desde archivo local, ejecuta `run_local.bat` y abre `http://localhost:8000`.

## Qué corrige esta versión

- Las fichas completas ya no dependen de que JavaScript construya todo el contenido.
- Los vídeos están incrustados directamente en cada ficha.
- Cada ficha tiene paso a paso más completo extraído del vídeo.
- Se indica explícitamente cuándo añadir sal, especias, vainilla, edulcorante u otros sazonadores.

## Estructura

- `index.html`: web local.
- `assets/videos/`: vídeos originales.
- `assets/thumbs/`: miniaturas/contact sheets.
- `recetas_md/`: fichas en Markdown.
- `data/recetas_video_lab_v2.json`: datos estructurados.
