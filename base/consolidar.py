#!/usr/bin/env python3
"""Consolida exportaciones (BibTeX, RIS, CSV de Scopus, JSON de OpenAlex) en una base unica
y marca duplicados por DOI y por titulo normalizado.
Uso: python3 consolidar.py fuente1:archivo1 fuente2:archivo2 ...
Salida: base/maestro.csv (todos los registros), base/unicos.csv, base/duplicados.csv, base/resumen.txt"""
import sys, re, csv, json, collections, unicodedata, os

def norm_title(t):
    t = unicodedata.normalize('NFKD', t or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()

def norm_doi(d):
    d = (d or '').lower().strip()
    d = re.sub(r'^https?://(dx\.)?doi\.org/', '', d)
    return d

def clean(s):
    return re.sub(r'\s+', ' ', (s or '').replace('{', '').replace('}', '')).strip()

def parse_bib(path):
    t = open(path, encoding='utf8').read()
    for e in re.split(r'\n(?=@\w+\s*\{)', t):
        if not e.lstrip().startswith('@'): continue
        f = {}
        for m in re.finditer(r'^\s*(\w+)\s*=\s*\{(.*?)\},?\s*$', e, re.M | re.S):
            f[m.group(1).lower()] = m.group(2)
        yield dict(titulo=clean(f.get('title')), autores=clean(f.get('author')), anio=f.get('year', ''),
                   revista=clean(f.get('journal') or f.get('booktitle')), doi=norm_doi(f.get('doi')),
                   resumen=clean(f.get('abstract')), palabras=clean(f.get('author_keywords') or f.get('keywords')))

def parse_ris(path):
    rec = {}; au = []
    for line in open(path, encoding='utf8-sig'):
        m = re.match(r'^([A-Z][A-Z0-9])  - ?(.*)$', line.rstrip('\n'))
        if not m: continue
        k, v = m.groups()
        if k == 'TY': rec = {}; au = []
        elif k in ('AU', 'A1'): au.append(v)
        elif k in ('TI', 'T1'): rec['titulo'] = v
        elif k in ('PY', 'Y1'): rec['anio'] = v[:4]
        elif k in ('JO', 'T2', 'JF', 'JA'): rec.setdefault('revista', v)
        elif k == 'DO': rec['doi'] = norm_doi(v)
        elif k in ('AB', 'N2'): rec['resumen'] = v
        elif k == 'KW': rec['palabras'] = (rec.get('palabras', '') + '; ' + v).strip('; ')
        elif k == 'ER':
            rec['autores'] = ' and '.join(au); yield {x: clean(rec.get(x)) for x in ('titulo','autores','anio','revista','doi','resumen','palabras')}

def parse_csv(path):
    for r in csv.DictReader(open(path, encoding='utf-8-sig')):
        yield dict(titulo=clean(r.get('Title')), autores=clean(r.get('Authors')), anio=r.get('Year', ''),
                   revista=clean(r.get('Source title')), doi=norm_doi(r.get('DOI')),
                   resumen=clean(r.get('Abstract')), palabras=clean(r.get('Author Keywords')))

def parse_openalex(path):
    d = json.load(open(path, encoding='utf8'))
    for w in d.get('results', d if isinstance(d, list) else []):
        inv = w.get('abstract_inverted_index') or {}
        pos = sorted((p, word) for word, ps in inv.items() for p in ps)
        yield dict(titulo=clean(w.get('title')), autores=' and '.join(a['author']['display_name'] for a in w.get('authorships', [])),
                   anio=str(w.get('publication_year') or ''), revista=clean(((w.get('primary_location') or {}).get('source') or {}).get('display_name')),
                   doi=norm_doi(w.get('doi')), resumen=w.get('_abstract') or ' '.join(x for _, x in pos), palabras='')

P = {'.bib': parse_bib, '.ris': parse_ris, '.csv': parse_csv, '.json': parse_openalex}
rows = []
for arg in sys.argv[1:]:
    src, path = arg.split(':', 1)
    ext = os.path.splitext(path)[1].lower()
    for r in P[ext](path):
        r['fuente'] = src; r['archivo'] = os.path.basename(path); rows.append(r)

seen_doi = {}; seen_tit = {}
for i, r in enumerate(rows, 1):
    r['id'] = f'R{i:05d}'
    r['titulo_norm'] = norm_title(r['titulo'])
    r['duplicado_de'] = ''; r['criterio_dup'] = ''
    d, t = r['doi'], r['titulo_norm']
    if d and d in seen_doi: r['duplicado_de'], r['criterio_dup'] = seen_doi[d], 'DOI'
    elif t and t in seen_tit: r['duplicado_de'], r['criterio_dup'] = seen_tit[t], 'titulo'
    else:
        if d: seen_doi[d] = r['id']
        if t: seen_tit[t] = r['id']

cols = ['id','fuente','archivo','titulo','autores','anio','revista','doi','resumen','palabras','duplicado_de','criterio_dup']
def dump(name, data):
    with open(f'base/{name}', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(data)
dump('maestro.csv', rows)
dump('unicos.csv', [r for r in rows if not r['duplicado_de']])
dump('duplicados.csv', [r for r in rows if r['duplicado_de']])
c = collections.Counter(r['fuente'] for r in rows); cu = collections.Counter(r['fuente'] for r in rows if not r['duplicado_de'])
res = [f'Total registros: {len(rows)}', f'Unicos: {sum(cu.values())}', f'Duplicados: {len(rows)-sum(cu.values())}', '']
res += [f'{s}: {c[s]} registros, {cu[s]} unicos aportados' for s in c]
res += ['', f'Sin DOI: {sum(1 for r in rows if not r["doi"])}', f'Sin resumen: {sum(1 for r in rows if not r["resumen"])}']
open('base/resumen.txt', 'w').write('\n'.join(res)); print('\n'.join(res))
