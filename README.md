# Recetario de Itu — v4

Web estática para elegir recetas, guardar favoritas y cocinar paso a paso. Conserva los enlaces `#receta-01` a `#receta-08`.

## Uso

- Busca por nombre o ingrediente; combina categoría, necesidad, favoritas y progreso.
- Abre una receta y entra en «Cocinar paso a paso» para marcar ingredientes y pasos.
- Los temporizadores siguen contando al cerrar el diálogo y se recuperan al volver o recargar. Con la aplicación cerrada o el dispositivo suspendido no se garantiza una alarma. El sonido es opcional.
- El progreso se guarda en este navegador, sin cuenta ni sincronización remota. Ajustes permite exportarlo e importarlo con confirmación.
- Una nueva versión ofrece «Actualizar ahora / Más tarde». La interfaz esencial se guarda sin descargar todos los vídeos.
- Cada vídeo se descarga por separado, mostrando su tamaño y estado. Se puede cancelar, reintentar y eliminar sin borrar la receta. El navegador puede liberar almacenamiento: comprueba el estado antes de desconectarte.

## Abrir y desarrollar

Abrir `index.html` directamente permite consultar y cocinar con los archivos locales. Para PWA y descargas usa HTTPS o un servidor local:

```text
node scripts/serve.cjs
```

Después abre http://127.0.0.1:8000. También se mantienen los lanzadores de Python existentes. No se necesitan dependencias de npm para generar o ejecutar las pruebas (Node 22 o posterior).

## Una sola fuente editorial

Edita `data/recipes.json`. No edites a mano el HTML raíz, el worker raíz, el JSON v3 distribuido o las fichas Markdown: son salidas generadas.

- `templates/index.html`: estructura de la interfaz.
- `css/app.css`: diseño, temas, impresión y reflujo.
- `js/core.js`: taxonomía, búsqueda y utilidades puras.
- `js/state.js`: validación, migración y persistencia.
- `js/timers.js`: temporizadores con reloj absoluto.
- `js/offline.js`: descargas y ciclo de actualización.
- `js/app.js`: interfaz y navegación.
- `templates/service-worker.js`: precaché esencial y vídeo con Range/206.

```text
node scripts/build.cjs
node scripts/build.cjs --check
node --test tests/*.test.cjs
```

El build valida IDs, categorías, datos y rutas; genera versión a partir del contenido, fichas Markdown, JSON compatible v3 y huellas SHA256. Los archivos de texto se normalizan a LF. Se conserva el JSON v2 histórico por compatibilidad, congelado y sin uso en la interfaz v4.

Al añadir una receta, usa IDs estables para ingredientes y pasos: no renumeres los existentes al insertar otros. `legacyIds` conserva la correspondencia histórica de la v3 y no se reordena. Desconocidos de raciones y tiempos se expresan como `null`, no como cantidades inventadas. El build calcula tamaño y huella de cada vídeo automáticamente.

Las miniaturas actuales son WebP extraídas de los vídeos existentes, con encuadres revisados. Para regenerarlas se requiere FFmpeg y `node scripts/make-thumbs.cjs`. Los iconos se pueden regenerar con Pillow y `python scripts/make-icons.py`; esas herramientas no son dependencias de la web ni del build ordinario.

## Migración y publicación

La migración automática conserva favoritos, estados y checks de v3, manteniendo también la clave antigua como copia. La primera actualización desde v3.8 puede requerir cerrar todas las pestañas antiguas y reabrir: aquella versión no tiene aviso de actualización. No borres los datos del sitio.

Antes de publicar: generar, comprobar salidas y pasar pruebas. GitHub Pages puede servir directamente este repositorio. Mantén la configuración existente de Pages; no cambies el origen de publicación sin revisarlo. CI valida cada PR.

Para ensayar la transición local desde el commit auditado, ejecuta `node scripts/prepare-upgrade-test.cjs` y arranca el servidor con `PREVIEW_FIXTURE=.preview/legacy` y un puerto de prueba independiente. Quitar el archivo `.preview/legacy/active` cambia ese servidor a v4. La carpeta `.preview` está ignorada.

## Límites y validación

Consulta [docs/VALIDACION_V4.md](docs/VALIDACION_V4.md) para evidencias y pendientes. No se considera cerrada la revisión de dispositivos físicos, subtítulos/alternativas audiovisuales completas, cantidades aún desconocidas ni métricas de campo. La interfaz indica esos límites y conserva el contenido original sin inventar datos.
