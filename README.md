# Recetario Video Lab — Itu v3.2

Repositorio local de recetas extraídas de vídeos y añadidas manualmente, con fichas paso a paso, vídeos locales cuando existen y modo cocinar.

## Qué cambia en v3.2

- Incorporado el vídeo local subido para la receta infantil: `05_tartitas_infantiles_yogur_frambuesas.mp4`.
- Enlazado el vídeo en `index.html`, JSON de datos, ficha Markdown y caché PWA/offline.
- Actualizada la miniatura de la receta a partir del vídeo.

## Qué cambia en v3.1

- Añadida receta infantil: `Tartitas infantiles de yogur, queso crema y frambuesas`.
- Añadido soporte para recetas sin vídeo local, evitando enlaces rotos.
- Añadida miniatura propia para la receta manual.
- Añadidos temporizadores de precalentado, horneado y enfriado.

## Qué cambia en v3

- `index.html` genera tarjetas, fichas, filtros y navegación desde los datos de recetas.
- Búsqueda sin tildes: `video` encuentra `vídeo`.
- Filtros automáticos por tipo y necesidad.
- Estado vacío cuando no hay resultados.
- Labels accesibles para buscador y filtros.
- Botones descriptivos para lector de pantalla.
- Modo cocinar con checklist de ingredientes y pasos.
- Temporizadores útiles por receta.
- Favoritos y estado local: pendiente, vista, cocinada, la repetiría, dominada.
- Botón copiar con fallback si el portapapeles falla.
- PWA/offline básica cuando se abre con servidor local.

## Cómo abrir

Opción simple:

1. Abre `index.html` con doble clic.
2. Los vídeos deberían reproducirse si el navegador permite archivos locales.

Opción recomendada:

1. Ejecuta `run_local.bat` o `run_local.ps1`.
2. Abre la dirección local que indique Python, normalmente `http://localhost:8000`.

## Datos

La copia principal de datos de esta versión está en:

- `data/recetas_video_lab_v3.json`

Se conserva también el JSON v2 por compatibilidad.

## Nota

El progreso de favoritos, estados y checks se guarda solo en el navegador mediante `localStorage`. No se envía nada a internet.
