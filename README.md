# Revisión sistemática: Tendencias de los procesos evolutivos psicosociales

Repositorio de trabajo del equipo de la revisión sistemática sobre factores psicosociales, organizacionales y tecnológicos en el voluntariado.

## Herramientas del proyecto

| Herramienta | Uso |
| --- | --- |
| Parsifal | Fuente de verdad del proceso: protocolo, cadenas, importación, cribado, calidad y extracción |
| Google Drive | Archivos y seguimiento: PDFs de texto completo, exportaciones, matrices, actas y cronograma |
| GitHub (este repositorio) | Versiones del texto en Markdown: protocolo, decisiones y manuscrito |
| Claude | Apoyo de IA. No decide inclusiones ni exclusiones |
| NotebookLM (Google) | Cuaderno compartido para analizar datos, documentos y fuentes. No sustituye a Parsifal |

Proyecto en Parsifal: https://parsif.al/jaime.meza/tendencias-de-los-procesos-evolutivos-psicosociales/

## Estructura

- `master.md`: documento maestro con los documentos formales, su estado y los responsables.
- `instrucciones-para-asistentes-ia.md`: reglas obligatorias para el agente de IA de cada miembro.
- `asistentes/`: un archivo por titular con los cambios de su trabajo, más la plantilla.
- `protocolo/`: objetivos, PICOC, preguntas, criterios y cadena de búsqueda.
- `decisiones/`: actas y registro de decisiones.
- `cribado/`: reglas y resultados del cribado.
- `calidad-y-extraccion/`: formularios y matrices.
- `manuscrito/`: una sección por archivo.

## Reglas

- Cada dato tiene un solo lugar principal. El estado del cribado vive en Parsifal.
- Todo cambio al protocolo se registra primero en `decisiones/` y luego se refleja en Parsifal.
- Los nombres de archivo van en minúsculas, con guiones medios y sin guiones bajos.
- `main` guarda solo lo aceptado por el equipo. Cada agente trabaja en su rama `asistente/<nombre>` y solo el equipo coordinador incorpora cambios a `main`, cuando el titular lo solicita.
- Toda ayuda de Claude se anota en `decisiones/` para declarar el uso de IA en el manuscrito.
