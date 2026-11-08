# Registro de búsquedas

## Scopus, 07-11-2026
- Cadena ejecutada (búsqueda avanzada, versión reducida): TITLE(volunteer* OR volunteering OR volunteerism) AND TITLE-ABS-KEY(psychosocial OR "social support" OR burnout OR "compassion fatigue" OR resilience OR stress OR motivation OR "social cohesion") AND TITLE-ABS-KEY("well-being" OR wellbeing OR "mental health" OR retention OR turnover OR dropout OR commitment) AND PUBYEAR > 2015 AND PUBYEAR < 2027, con filtros de idioma (inglés, español) y tipo de documento (artículo, congreso, revisión).
- Resultados: 696 documentos (686 artículos y 10 de congreso; 694 con resumen).
- Archivo: scopus-2026-11-07.bib (BibTeX con resumen y palabras clave de autor).
- Parsifal: importó 675. Diferencia de 21 por revisar; 3 claves de cita repetidas en el archivo (Russo-Netzer2026, Williams2024, Sharma2026).
- Búsqueda amplia de control (sin exigir voluntari* en el título, con "psychological"): 3.459 documentos, no exportada.
- Scopus AI (consulta exploratoria, no se importa): 11 referencias, varias fuera de voluntariado.

## Otras fuentes, 07-11-2026 (conteos, sin exportar)
- IEEE Xplore: 29 resultados. Cadena adaptada: ("Document Title":volunteer* OR "Document Title":volunteering) AND (well-being, mental health, retention, burnout, resilience, social support, psychosocial, motivation en All Metadata), 2016 a 2026.
- ScienceDirect: 859 resultados. Título: volunteer OR volunteering OR volunteerism; palabras clave: "well-being" OR "mental health" OR retention OR burnout OR resilience OR "social support" OR psychosocial OR motivation; 2016 a 2026; artículos de investigación y revisiones.
- OpenAlex (vía API pública, fuente complementaria): 893 resultados con volunteer/volunteering/volunteerism en título, un factor psicosocial y un resultado en título o resumen, 2016 a 2026, artículo o revisión, inglés o español. La API gratuita tiene presupuesto diario compartido por IP; para exportar el total conviene una clave gratuita.
- Web of Science: sin acceso (requiere suscripción institucional). Pendiente gestionar acceso o dejar como limitación.

## Consolidación 07-11-2026
- Base en carpeta base (script consolidar.py). Scopus 696 + OpenAlex 893 = 1.589 registros; 1.063 únicos y 526 duplicados (513 por DOI, 13 por título). OpenAlex aporta 367 únicos frente a Scopus.
- OpenAlex exportado completo con clave de API (893; 826 con resumen), archivo openalex-2026-11-07.json.
- Archivo RIS con los 367 nuevos de OpenAlex: openalex-nuevos-vs-scopus-367.bib

## Scopus, versión amplia con exclusiones, 07-11-2026 (conteo, sin exportar)
- Cadena: (TITLE(volunteer* OR volunteering OR volunteerism) AND TITLE-ABS-KEY(todos los factores y resultados en un solo bloque OR) AND PUBYEAR > 2015 AND PUBYEAR < 2027, inglés o español, artículo, congreso o revisión) AND NOT (TITLE("healthy volunteer*" OR "healthy adult*" OR pharmacokinetic* OR "clinical trial" OR randomi*)).
- Resultado: 2.802 documentos. Sin las exclusiones: 3.366 (incluyendo 2015). Nota de sintaxis: AND NOT debe ir al final y entre paréntesis; con la exclusión en medio de la cadena Scopus devolvió 36.141 (todo lo que tiene volunteer en el título).

## Scopus amplia exportada y consolidación, 07-11-2026
- Archivo: scopus-amplia-2026-11-07.bib (2.802 registros).
- Base consolidada (Scopus reducida 696, OpenAlex 893, Scopus amplia 2.802): 4.391 registros, 3.191 únicos, 1.200 duplicados. La amplia aporta 2.128 únicos; 661 de sus registros ya estaban en la reducida (35 de la reducida no están en la amplia por las exclusiones).
- Aceptados del proyecto anterior recuperados con la base completa: 33 de 77 (antes 17).

## ScienceDirect, exportación RIS (2026-11-08)
859 registros exportados en 9 archivos RIS (bloques de 100) en `busquedas/sciencedirect/`. Aportaron 571 registros únicos a la base, que pasa a 3,762. Prelectura aplicada solo a los nuevos: 261 para cribar (59 A, 202 B, de ellos 100 restaurados de X por lectura manual) y 310 excluidos propuestos. Lote extra: `cribado/rayyan/rayyan-lote-5.csv` y `cribado/sheets/Cribado-*-lote-extra.xlsx`.
