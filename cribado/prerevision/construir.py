import csv,random,openpyxl,copy
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
d=dict(l.split() for l in open('decisiones.tsv'))
TES=dict(l.rstrip('\n').split('\t',1) for l in open('titulos_es.tsv',encoding='utf-8'))
P={r['id']:r for f in ('../para-cribar.csv','../excluidos-propuestos.csv') for r in csv.DictReader(open(f,encoding='utf-8-sig'))}
MOT={'E4':'No es voluntariado (voluntarios sanos de ensayos, donantes, otro sentido de "voluntario")',
 'V':'Voluntariado, pero sin factores ni resultados pertinentes en los voluntarios',
 'B':'Resultados medidos solo en beneficiarios o pacientes, no en los voluntarios',
 'E1':'Editorial, comentario, carta, protocolo sin datos o resumen de congreso',
 'E6':'Sin revisión por pares (tesis, informe, póster)','E3':'Idioma distinto de español o inglés'}
pas=[i for i,c in d.items() if c in 'PD']; exc=[i for i,c in d.items() if c not in 'PD']
def prio(i):
    if d[i]=='D': return 3
    return 1 if P[i]['categoria'].startswith('A') else 2
pas.sort(key=lambda i:(prio(i),i))
lotes=[pas[0::2],pas[1::2]]
H=Font(name='Arial',bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='1F3864'); F=Font(name='Arial',size=10)
EJ=PatternFill('solid',fgColor='FFF2CC')
NOTA={1:'Prioridad alta: cumple a primera vista',2:'Prioridad media: cumple, factor o resultado menos explícito',3:'Duda: revisar con cuidado, decidir con texto completo si hace falta'}
old=openpyxl.load_workbook('../sheets/Cribado-Joel-lote1.xlsx')
crit=[[c.value for c in r] for r in old['Criterios'].iter_rows()]
def hoja(wb,titulo,cols,widths):
    ws=wb.create_sheet(titulo); ws.append(cols)
    for c,w in zip(ws[1],widths):
        c.font=H;c.fill=HF;c.alignment=Alignment(wrap_text=True,vertical='center'); ws.column_dimensions[c.column_letter].width=w
    ws.freeze_panes='B2'; return ws
def criterios(wb):
    ws=wb.create_sheet('Criterios')
    for r in crit: ws.append(r)
    for r in ws.iter_rows():
        for c in r: c.font=F
    ws.column_dimensions['A'].width=110
def libro(nom,par,ids,lote):
    wb=openpyxl.Workbook(); wb.remove(wb.active)
    cols=['id','prioridad','año','título (original)','título (español)','resumen (original)','¿traducir resumen? (elige Sí)','resumen (español, a pedido)','revista','doi','nota de la prerevisión','DECISIÓN','MOTIVO (si excluye)','nota']
    ws=hoja(wb,'Cribado',cols,[9,9,6,50,50,70,12,70,26,22,34,12,14,28])
    for n,i in enumerate(ids,2):
        r=P[i]; pr=prio(i); nt=NOTA[pr]+('. Rescatado de la exclusión automática' if r['categoria']=='X_excluir' else '')
        ws.append([i,pr,int(r['anio']) if r['anio'].isdigit() else r['anio'],r['titulo'],TES[i],
                   r['resumen'][:4900],None,f'=IF(G{n}="Sí",IFERROR(GOOGLETRANSLATE(F{n},"en","es"),"no cargó: borra el Sí y vuelve a elegirlo"),"")',r['revista'],r['doi'],nt,None,None,None])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font=F; c.alignment=Alignment(vertical='top',wrap_text=c.column in (4,5,11))
    last=len(ids)+1
    v=DataValidation(type='list',formula1='"Incluir,Excluir,Dudar"',allow_blank=True); v.add(f'L2:L{last}'); ws.add_data_validation(v)
    v2=DataValidation(type='list',formula1='"E1,E2,E3,E4,E5,E6"',allow_blank=True); v2.add(f'M2:M{last}'); ws.add_data_validation(v2)
    v3=DataValidation(type='list',formula1='"Sí"',allow_blank=True); v3.add(f'G2:G{last}'); ws.add_data_validation(v3)
    ws.auto_filter.ref=f'A1:N{last}'
    for c in ('L','M','N'): ws[f'{c}1'].fill=PatternFill('solid',fgColor='C00000')
    ws['G1'].fill=PatternFill('solid',fgColor='548235')
    ins=wb.create_sheet('Instrucciones',0); ins.column_dimensions['A'].width=120
    for t in [f'Revisor: {nom}. Pareja: {nom} y {par} (lote {lote}, {len(ids)} registros, prerevisados). Cribado por título y resumen.',
      'Solo llenas las columnas rojas: L DECISIÓN (Incluir, Excluir o Dudar), M MOTIVO si excluyes (E1 a E6, ver hoja Criterios) y N nota libre.',
      'Ejemplo de llenado: L = Excluir, M = E4, N = "estudio de voluntarios sanos en un ensayo de fármacos".',
      'La columna E trae el título ya traducido al español. Para leer el resumen en español, elige Sí en la columna verde G de esa fila y la columna H lo traduce con Google en unos segundos. Hazlo fila por fila, solo cuando lo necesites: si se piden cientos a la vez, Google deja de responder. La traducción es de apoyo: ante duda, manda el original.',
      'Orden: primero prioridad 1 (alta), luego 2 (media) y al final 3 (duda). La prioridad y la nota vienen de una prerevisión asistida por IA y NO son una decisión: decide tú.',
      'Trabaja SOLO en tu archivo. No abras el de tu pareja hasta terminar (cribado ciego). Los desacuerdos los resuelve un tercero.',
      'No cambies el orden de las filas ni el id. Dudar pasa a texto completo; excluye solo cuando el título y el resumen lo muestran claramente.']:
        ins.append([t])
    for r in ins.iter_rows():
        for c in r: c.font=F; c.alignment=Alignment(wrap_text=True)
    ins['A3'].fill=EJ
    criterios(wb); wb.save(f'salida/Cribado-{nom}-prerevisado.xlsx')
import os; os.makedirs('salida',exist_ok=True)
for nom,par,m in [('Joel','Margarita',0),('Margarita','Joel',0),('Cristina','Anita',1),('Anita','Cristina',1)]: libro(nom,par,lotes[m],m+1)
# exclusiones
random.seed(2026); exc.sort(); mues=set(random.sample(exc,round(len(exc)*0.1)))
wb=openpyxl.Workbook(); wb.remove(wb.active)
ws=hoja(wb,'Exclusiones',['id','código','motivo','año','título (original)','¿traducir? (elige Sí)','título (español, a pedido)','resumen (original)','resumen (español, a pedido)','¿muestra de auditoría?','¿de acuerdo con excluir? (Sí/No)','nota del auditor'],[9,8,40,6,55,12,55,70,70,12,14,30])
for n,i in enumerate(exc,2):
    r=P[i]; ws.append([i,d[i],MOT[d[i]],r['anio'],r['titulo'],None,f'=IF(F{n}="Sí",IFERROR(GOOGLETRANSLATE(E{n},"auto","es"),"no cargó"),"")',r['resumen'][:4900],f'=IF(F{n}="Sí",IFERROR(GOOGLETRANSLATE(H{n},"auto","es"),"no cargó: borra el Sí y vuelve a elegirlo"),"")','SÍ' if i in mues else '',None,None])
for row in ws.iter_rows(min_row=2):
    for c in row:
        c.font=F; c.alignment=Alignment(vertical='top',wrap_text=c.column in (3,5,7))
        if row[9].value=='SÍ': c.fill=EJ
v=DataValidation(type='list',formula1='"Sí,No"',allow_blank=True); v.add(f'K2:K{len(exc)+1}'); ws.add_data_validation(v)
v3=DataValidation(type='list',formula1='"Sí"',allow_blank=True); v3.add(f'F2:F{len(exc)+1}'); ws.add_data_validation(v3)
ws['F1'].fill=PatternFill('solid',fgColor='548235')
ws.auto_filter.ref=f'A1:L{len(exc)+1}'
ins=wb.create_sheet('Instrucciones',0); ins.column_dimensions['A'].width=120
for t in [f'Exclusiones propuestas por la prerevisión: {len(exc)} registros, cada uno con su código y motivo.',
  f'Auditoría: revisar al menos las {len(mues)} filas marcadas SÍ (muestra aleatoria del 10 %, semilla 2026). Si el desacuerdo supera el 5 %, revisar todas.',
  'Llenar la columna K (Sí/No) y, si no estás de acuerdo, explicar en L. Lo que se rescate vuelve al cribado.',
  'Para leer título y resumen en español, elige Sí en la columna verde F de esa fila (traducción de Google a pedido, fila por fila).',
  'Códigos: E4 no es voluntariado; V voluntariado sin factores ni resultados pertinentes; B resultados solo en beneficiarios; E1 editorial, protocolo o resumen de congreso; E6 sin revisión por pares; E3 otro idioma.']:
    ins.append([t])
for r in ins.iter_rows():
    for c in r: c.font=F; c.alignment=Alignment(wrap_text=True)
wb.save('salida/Exclusiones-prerevision-auditoria.xlsx')
# rayyan
w=csv.writer(open('salida/rayyan-prerevisado.csv','w',newline='',encoding='utf-8'))
w.writerow(['key','title','authors','journal','year','abstract','doi','keywords','notes'])
for i in pas: r=P[i]; w.writerow([i,r['titulo'],r['autores'],r['revista'],r['anio'],r['resumen'],r['doi'],r['palabras'],f'prerevision {d[i]} prioridad {prio(i)}'])
import collections
print(len(pas),[len(l) for l in lotes],collections.Counter(prio(i) for i in pas),len(exc),len(mues))
