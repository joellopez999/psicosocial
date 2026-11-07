# Documento maestro del proyecto

Revisión sistemática "Tendencias de los procesos evolutivos psicosociales".
Última actualización: 7 de noviembre de 2026.

## 1. Para qué sirve este documento

Este documento es la guía común de todos los agentes y miembros del proyecto. Dice cuáles son los documentos formales, dónde viven, en qué estado están y quién responde por ellos. Lo que está en la rama `main` está aceptado por el equipo. Lo que no está en `main` es trabajo en curso.

Este documento trata solo de este proyecto. No contiene reglas ni configuraciones particulares de los agentes de cada miembro.

## 2. El proyecto

Revisión sistemática sobre los factores psicosociales y organizacionales que influyen en el bienestar, el compromiso y la permanencia de los voluntarios, el papel de las tecnologías digitales y las bases de un modelo de gobernanza del voluntariado.

Proceso en Parsifal: https://parsif.al/jaime.meza/tendencias-de-los-procesos-evolutivos-psicosociales/

## 3. Documentos formales

Estados posibles: **Vigente** (aceptado por el equipo), **Borrador** (en trabajo o en revisión) y **Sin iniciar**.

| Documento | Ubicación en el repositorio | Copia en Drive | Estado | Responsable |
| --- | --- | --- | --- | --- |
| Protocolo de la revisión | `protocolo/protocolo.md` | `protocolo.md` | Borrador. Manda lo registrado en Parsifal | Jaime Meza |
| Registro de decisiones | `decisiones/registro-de-decisiones.md` | `registro-de-decisiones.md` | Vigente | Joel López |
| Acta de reunión del 07-11-2026 | `decisiones/acta-2026-11-07.md` | Acta en Word | Borrador, pendiente de fechas y firmas | Cristina Chancay |
| Reglas del cribado | `cribado/README.md` | No aplica | Borrador | Joel López |
| Calidad y extracción | `calidad-y-extraccion/README.md` | No aplica | Sin iniciar | Por confirmar |
| Manuscrito | `manuscrito/` | Estado del arte en Drive | Borrador | Ana Vélez |

Cuando un documento cambia de estado, se actualiza esta tabla en el mismo cambio.

## 4. Equipo y responsabilidades

**Equipo coordinador:** Joel López, Ana Vélez, Jaime Meza y Cristina Chancay (asistente de investigación). Solo el equipo coordinador incorpora cambios a `main`.

| Persona | Responsabilidad |
| --- | --- |
| Joel López | Coordinación general, repositorio, uso de Claude y cribado de estudios |
| Ana Vélez | Responsable del manuscrito |
| Margarita Carbó | Apoyo en el manuscrito (pendiente de confirmar) |
| Cristina Chancay | Importación, duplicados, Drive, matriz de extracción y reuniones |
| Jaime Meza | Autor principal en Parsifal, metodología, cadenas de búsqueda y NotebookLM |
| Diego Intriago, Vivian Bumbila, Ander Suárez | Miembros formales, funciones sin cambios por ahora |
| Wilson Rivas, Joseph López, Andrés Tumbaco | Estudiantes, apoyo supervisado |

Pendiente de confirmar: quién tiene la evaluación de calidad.

## 5. Herramientas y qué vive en cada una

| Herramienta | Qué guarda |
| --- | --- |
| Parsifal | Fuente de verdad del proceso: protocolo, cadenas, importación, cribado, calidad y extracción |
| Google Drive | Archivos y seguimiento: PDFs de texto completo, exportaciones, matrices, actas y cronograma |
| GitHub | Versiones del texto en Markdown. `main` guarda lo aceptado por el equipo |
| Claude | Apoyo de IA de cada miembro. No decide inclusiones ni exclusiones |
| NotebookLM (Google) | Cuaderno compartido para analizar datos, documentos y fuentes. No sustituye a Parsifal |

Carpeta de Drive del proyecto: "Tendencias de los procesos evolutivos".

## 6. Cómo trabaja el equipo con el repositorio

- Cada miembro tiene su propio agente de IA y un archivo propio en `asistentes/` con los cambios de su titular.
- Cada agente trabaja en su rama `asistente/<nombre>` y no escribe en `main`.
- Cuando el titular está completamente seguro de un cambio, lo solicita al equipo coordinador, que lo revisa y lo incorpora a `main`.
- Toda decisión que cambie un documento formal se anota en el registro de decisiones.

El detalle está en `instrucciones-para-asistentes-ia.md`.

## 7. Estado al 7-11-2026

- 250 estudios importados: Scopus 222, IEEE 14, ScienceDirect 14, Web of Science 0.
- Cribado en curso en Parsifal, con duplicados por cerrar.
- Evaluación de calidad y extracción de datos sin iniciar.
- Observaciones abiertas sobre la cadena de búsqueda: es muy amplia, falta registrar cadenas por fuente y "procesos evolutivos" necesita una definición operativa.

## 8. Pendientes

- Modalidad de las reuniones de la próxima semana (presencial o virtual). Fechas ya fijadas: oficiales martes 10, miércoles 11 y jueves 12 de noviembre a las 16:00, y respaldos las mañanas siguientes a las 07:30.
- Responsable de la evaluación de calidad.
- Confirmación de Margarita Carbó para apoyar el manuscrito.
- Cuaderno compartido en NotebookLM y fuentes que se cargan.
- Pasar el repositorio a privado.
