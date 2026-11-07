#!/usr/bin/env python3
"""Pre-lectura asistida (propuesta, no sustituye el cribado humano). v2: puntaje por constructos distintos.
Entrada: base/unicos.csv  Salida: cribado/prelectura.csv"""
import csv, re, collections
C = {  # constructo -> patron
 'bienestar': r'well-?being|bienestar|quality of life|life satisfaction',
 'salud_mental': r'mental health|salud mental|depress\w*|anxiety|psychological distress|mental illness|trauma\w*|ptsd|loneliness',
 'motivacion': r'motivat\w*|motivaci[oó]n|intrinsic|self-determination',
 'permanencia': r'retention|retain\w*|turnover|drop-?out|attrition|intention to (stay|continue|quit|leave)|sustain(ed|ing)? (participation|volunteer\w*|engagement)|permanencia|rotaci[oó]n|deserci[oó]n',
 'compromiso': r'commitment|compromiso|engagement|involvement|satisfaction',
 'burnout_estres': r'burnout|compassion fatigue|emotional exhaustion|stress\w*|estr[eé]s|moral distress|secondary trauma',
 'apoyo_social': r'social support|peer support|support network\w*|support group|apoyo social|social network\w*|social capital|connectedness|belonging|social cohesion|cohesi[oó]n|loneliness',
 'resiliencia': r'resilien\w*|coping|self-efficacy|self-compassion|empowerment',
 'organizacion': r'organi[sz]ational support|supervision|leadership|volunteer management|recognition|training|mentor\w*',
 'tecnologia': r'digital|online|mobile app|platform|technolog\w*|social media|e-volunteer\w*|virtual volunteer\w*|app-based|gamification',
 'psicosocial': r'psychosocial|psychological|psicosocial|psicol[oó]g\w*',
}
CP = {k: re.compile(v, re.I) for k, v in C.items()}
VOL = re.compile(r'volunt\w*', re.I)
CLIN = re.compile(r'healthy (adult |young |male |female |older )?volunteers?|normal volunteers?|volunteers? (were|was) (recruited|enrolled|randomi[sz]ed)|pharmacokinetic|bioavailab\w*|phase i\b', re.I)
rows = list(csv.DictReader(open('base/unicos.csv', encoding='utf8')))
BIO = re.compile(r'human volunteers|volunteer (canola|vegetation|plants?|crops?|wheat|corn|seedlings?|weeds?)|propofol|anesthe\\w*|sedation|cigarette\\w*|tobacco|inhal\\w*|ingest\\w*|oxidative|glutathione|cytokine|metabolic|lipid\\w*|pharmac\\w*|\bMRI\b|serum|plasma|blood|biomarker|cognitive function|lumbar|kidney|diffusion capacity|hydration|monoamine|pharmac\w*|vaccin\w*|clinical trial|healthy (adult|young|elderly|older|male|female|subjects|participants|volunteers)|physiolog\w*|exhal\w*|bioavailab\w*|placebo|dose|supplement\w*|nutrition\w*|\bPET\b|fMRI|EEG', re.I)
ACT = re.compile(r'volunteering|volunteerism|volunteer (work|program|programme|service|role|organi[sz]ation|management|activit\w+|experience)|voluntary (work|service|sector)|nonprofit|non-profit|charit\w+|ngo\b|volunteers? (in|at|for|with) |community volunteer\w*|hospice|helpline|red cross|firefight\w*|disaster', re.I)
C2 = {'bienestar','salud_mental','motivacion','apoyo_social','resiliencia','burnout_estres','organizacion','psicosocial','permanencia','compromiso'}
C3 = {'permanencia','compromiso','tecnologia','apoyo_social','organizacion'}
for r in rows:
    t, a, k = r['titulo'], r['resumen'], r['palabras']
    tt = {c for c, p in CP.items() if p.search(t)}
    aa = {c for c, p in CP.items() if p.search(a + ' ' + k)}
    allc = aa | tt
    vt = len(VOL.findall(t)); va = len(VOL.findall(a + ' ' + k))
    r['constructos_titulo'] = ';'.join(sorted(tt)); r['constructos_resumen'] = ';'.join(sorted(aa))
    r['n_constructos'] = len(allc); r['vol_titulo'] = vt; r['vol_resumen'] = va
    c2 = bool(allc & C2); c3 = bool(allc & C3) and (len(allc) >= 2 or 'permanencia' in allc or 'tecnologia' in allc)
    r['prioridad_factor'] = int(bool(allc & {'bienestar','salud_mental','motivacion','apoyo_social','resiliencia','burnout_estres','organizacion','psicosocial'}))
    r['cumple_criterio2'] = int(c2); r['cumple_criterio3'] = int(c3)
    texto = t + ' ' + a
    if not a.strip():
        cat, mot = ('B_duda', 'sin resumen: decidir por titulo') if (tt & C2) else ('X_excluir', 'sin resumen y sin constructo psicosocial en el titulo')
    elif BIO.search(texto) and not ACT.search(texto):
        cat, mot = 'X_excluir', 'E1 voluntarios como sujetos de estudio biomedico o experimental, sin voluntariado como actividad'
    elif vt == 0 and va < 3:
        cat, mot = 'X_excluir', 'E2 voluntariado tangencial'
    elif not c2:
        cat, mot = 'X_excluir', 'sin ningun constructo psicosocial, de permanencia, compromiso o tecnologia'
    elif c3:
        cat, mot = 'A_cribar', 'muestra factor psicosocial y resultado, red de apoyo o tecnologia: cribar con prioridad alta'
    else:
        cat, mot = 'B_duda', 'muestra un factor o un resultado, pero no ambos: cribar con prioridad menor'
    r['categoria'] = cat; r['motivo'] = mot
cols = list(rows[0].keys())
with open('cribado/prelectura.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(collections.Counter(r['categoria'] for r in rows))
print(collections.Counter(r['motivo'] for r in rows if r['categoria'] == 'X_excluir'))
