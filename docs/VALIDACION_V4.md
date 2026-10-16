# Validación y cierre del roadmap v4

Fecha de implementación: 17 de octubre de 2026. Base: v3.8 / c1d665b.

## Implementado

- F01–F03: categorías explícitas, Cenas con subsecciones, búsqueda temprana, navegación independiente de filtros y enlaces históricos de receta conservados.
- F04–F06: precaché esencial sin MP4, fallos de instalación no silenciados, limpieza limitada a cachés propias, versión generada y aviso de actualización.
- F07: temporizadores con hora de finalización, pausa/continuación, persistencia, panel fuera del diálogo, aviso persistente y sonido opcional. No se garantiza alarma con navegador cerrado o dispositivo suspendido.
- F08–F09: paleta con contraste, foco visible, actualización localizada de controles y devolución del foco al cerrar cocina.
- F10–F11, F18: portada breve, categorías/subsecciones contextuales, filtros combinables, estado vacío recuperable, URL con contexto y detalle bajo demanda.
- F12–F14: progreso validado y versionado, migración de checks por IDs estables, copia antigua conservada, importación/exportación, fuente editorial única y generación automática de HTML/JSON/Markdown. Checks en CI.
- F15: iconos e identidad PWA, descarga explícita por vídeo, cancelación/reintento/borrado y respuestas parciales 206. Las URLs de vídeo incluyen huella del archivo para no reutilizar otro contenido tras una sustitución.
- F16: landmarks, salto al contenido, semántica de controles, foco, movimiento reducido y anuncios de resultados. La revisión multimedia completa continúa pendiente.
- F17, F19: equipo visible y campos de raciones/tiempos con desconocidos explícitos, origen separado de disponibilidad, miniaturas WebP del vídeo y copia con resultado comprobado. No se han inventado cantidades.

## Evidencias realizadas

Pruebas automáticas reproducibles con `node --test tests/*.test.cjs`:

- Clasificación y búsquedas positivas sin usar contraindicaciones como coincidencias.
- Migración desde arrays de índices aunque cambie el orden actual de los pasos.
- Almacenamiento bloqueado, esquema de importación y filtrado de IDs desconocidos.
- Temporizadores con reloj absoluto, recuperación, pausa, finalización única y reinicio explícito.
- Instalación fallida que rechaza la nueva caché; conservación de cachés ajenas y de medios.
- Respuesta 206 a intervalos regulares y sufijos; respuesta 416 a intervalos inválidos.
- Navegación offline con query y exclusión de otros proyectos/peticiones no GET.

Pruebas manuales en Chromium integrado:

- Cenas devuelve trenza y minipizzas; patatas y tartitas ya no aparecen como cenas proteicas.
- Un enlace directo a patatas se abre con búsqueda `zzzz` y categoría Cenas activas.
- Favorito mantiene foco; cerrar cocina devuelve al botón de apertura.
- Tras recarga se conservan el check «Patatas», la favorita y el tiempo restante.
- Descarga real de vídeo de patatas y persistencia del estado «Vídeo descargado» tras recarga.
- La interfaz de una versión guardada siguió abriéndose con el servidor local detenido.
- Actualización 8a7e467e7c30 → 3903bdf377b0 mediante el aviso: favorita conservada y temporizador de 1:46 recuperado.
- Migración real de v3.8 a v4 en un origen local de prueba: minipizzas conserva favorita, «Cocinada» y check de 150 g de garbanzos. La primera transición se realizó cerrando la pestaña antigua tras instalar el nuevo worker.
- Sin desbordamiento del documento en catálogo a 320, 360, 390, 768 y 1440 px; ficha y diálogo también comprobados a 320 px. Buscador a unos 293 px de la parte superior a 390 px, frente a unos 3746 px en la auditoría.
- Subsección «Proteicas rápidas» de Cenas devuelve únicamente minipizzas. No se encontraron IDs duplicados en la ficha comprobada.
- Las siete miniaturas WebP suman 167.110 bytes. El catálogo no crea ningún elemento de vídeo; la ficha crea uno con `preload="none"`.
- Las pruebas automatizadas incluyen conservación íntegra de ingredientes, pasos y advertencias editoriales de las ocho recetas auditadas.
- Build d082529ac80d: tras descargar patatas con URL de vídeo versionada, se detuvo el servidor. La receta se recargó desde caché y el vídeo alcanzó `readyState=4`, reproduciendo sin error. Las respuestas parciales se cubren además en tests; esto no sustituye la validación en Safari.

## Pendiente de cierre integral

El código de las mejoras está preparado; estas comprobaciones no se dan por completadas:

1. Safari/iPhone y Android físicos: instalación, relanzamiento, reproducción offline y salto temporal, bloqueo de pantalla y reanudación.
2. Revisión manual con lector de pantalla real y evaluación completa WCAG; los controles semánticos y las pruebas de teclado no constituyen certificación.
3. Revisión audiovisual completa y creación/verificación de subtítulos o alternativas equivalentes de los siete vídeos. Los métodos escritos se mantienen, pero no se presentan como transcripción completa.
4. Confirmar editorialmente cantidades, raciones y tiempos totales que no constaban con certeza. Se mantienen pendientes en la interfaz.
5. Medición de LCP/CLS y transferencia en un perfil de red/dispositivo documentado. No se atribuyen puntuaciones ni métricas de campo sin medirlas.
6. Pruebas de cuota agotada y varias pestañas en navegadores físicos. Hay tolerancia de errores y sincronización local implementadas; sus límites de concurrencia deben revisarse antes de prometer resolución de conflictos simultáneos.
7. Despliegue de producción y actualización de una instalación real de GitHub Pages. Un PR preparado no equivale a publicación.

## Primera actualización desde v3.8

La versión antigua no tiene aviso de actualización. Tras publicar v4 puede ser necesario cerrar todas las pestañas/ventanas del recetario y volver a abrirlo para que el nuevo worker se active. No borrar datos del sitio: eso eliminaría también el progreso que se pretende migrar. Las siguientes versiones v4 presentan aviso «Actualizar ahora / Más tarde».

## Recuperación

- Se conserva la clave antigua `itu_recetario_video_lab_v3_state` como copia previa a la migración.
- Exportar progreso antes de importar/reemplazarlo o volver a una versión anterior.
- No revertir solo el HTML: el worker y el esquema persistido también deben ser compatibles. Preferir una versión correctora con nueva identidad de build y el mismo lector de progreso v4.
- No borrar cachés de otras aplicaciones del origen.
