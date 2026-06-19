# Recetario Video Lab — Itu v3

Repositorio local de recetas extraídas de vídeos, con fichas paso a paso, vídeos locales y modo cocinar.

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
