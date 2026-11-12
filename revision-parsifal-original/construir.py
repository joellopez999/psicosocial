import json,openpyxl,os
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.worksheet.datavalidation import DataValidation
D=json.load(open('parsifal-250.json'))
TES=dict(l.rstrip('\n').split(' ',1) for l in open('titulos_es.txt',encoding='utf-8'))
EST={'A':'Aceptado','R':'Rechazado','D':'Duplicado'}
for i,x in enumerate(D,1): x['n']=i; x['tes']=TES[str(i)]
orden=sorted(D,key=lambda x:({'A':0,'R':1,'D':2}[x['status']],x['n']))
lotes=[orden[0::2],orden[1::2]]
INC=['Artículos en revistas científicas o actas de congreso con revisión por pares',
'Estudios centrados en bienestar social, salud mental, permanencia, sostenibilidad, modelo de gobernanza',
'Estudios disponibles en texto completo, en español e inglés','Estudios publicados entre 2016 al 2026',
'Estudios que aborden factores organizacionales','Estudios que aborden factores psicosociales (psicológicos, sociales)',
'Estudios que aborden procesos evolutivos','Estudios que aborden tecnologías digitales']
EXC=['Editoriales, opiniones o resúmenes de congreso sin datos completos','Estudios duplicados (se conserva solo la versión más completa)',
'Estudios en idiomas distintos a español o inglés','Estudios no relacionados con voluntariado o procesos de voluntariado',
'Estudios publicados antes de 2016','Estudios sin acceso a texto completo','Estudios sin revisión por pares']
H=Font(name='Arial',bold=True,color='FFFFFF');HF=PatternFill('solid',fgColor='1F3864');F=Font(name='Arial',size=10)
EJ=PatternFill('solid',fgColor='FFF2CC')
def hoja(wb,t,cols,w):
    ws=wb.create_sheet(t);ws.append(cols)
    for c,x in zip(ws[1],w):
        c.font=H;c.fill=HF;c.alignment=Alignment(wrap_text=True,vertical='center');ws.column_dimensions[c.column_letter].width=x
    ws.freeze_panes='B2';return ws
def criterios(wb):
    ws=wb.create_sheet('Criterios');ws.column_dimensions['A'].width=10;ws.column_dimensions['B'].width=100
    ws.append(['','Criterios tal como están en Parsifal (proyecto de jaime.meza), sin cambios']);ws.append([])
    ws.append(['','CRITERIOS DE INCLUSIÓN'])
    for i,c in enumerate(INC,1): ws.append([f'IN{i}',c])
    ws.append([]);ws.append(['','CRITERIOS DE EXCLUSIÓN (código para la columna MOTIVO)'])
    for i,c in enumerate(EXC,1): ws.append([f'EX{i}',c])
    for r in ws.iter_rows():
        for c in r: c.font=Font(name='Arial',size=10,bold=c.value in ('CRITERIOS DE INCLUSIÓN','CRITERIOS DE EXCLUSIÓN (código para la columna MOTIVO)'))
COLS=['n','estado actual en Parsifal','año','título (original)','título (español)','resumen (original)','¿traducir resumen? (elige Sí)','resumen (español, a pedido)','revista','doi','tipo de documento','DECISIÓN','MOTIVO (si excluye)','nota','¿coincide con Parsifal?']
W=[6,12,6,50,50,70,12,70,26,22,14,12,14,28,12]
def fila(ws,n,x):
    ws.append([x['n'],EST[x['status']],int(x['year']) if str(x['year']).isdigit() else x['year'],' '.join((x['title'] or '').split()),x['tes'],
      (x['abstract'] or '')[:4900],None,f'=IF(G{n}="Sí",IFERROR(GOOGLETRANSLATE(F{n},"en","es"),"no cargó: borra el Sí y vuelve a elegirlo"),"")',
      x['journal'],x['doi'],x['document_type'],None,None,None,
      f'=IF(L{n}="","",IF(OR(AND(L{n}="Incluir",B{n}="Aceptado"),AND(L{n}="Excluir",B{n}="Rechazado"),AND(L{n}="Duplicado",B{n}="Duplicado")),"Sí",IF(L{n}="Dudar","Duda","No")))'])
def valid(ws,last):
    v=DataValidation(type='list',formula1='"Incluir,Excluir,Dudar,Duplicado"',allow_blank=True);v.add(f'L2:L{last}');ws.add_data_validation(v)
    v2=DataValidation(type='list',formula1='"EX1,EX2,EX3,EX4,EX5,EX6,EX7"',allow_blank=True);v2.add(f'M2:M{last}');ws.add_data_validation(v2)
    v3=DataValidation(type='list',formula1='"Sí"',allow_blank=True);v3.add(f'G2:G{last}');ws.add_data_validation(v3)
    ws.auto_filter.ref=f'A1:O{last}'
    for c in 'LMN': ws[f'{c}1'].fill=PatternFill('solid',fgColor='C00000')
    ws['G1'].fill=PatternFill('solid',fgColor='548235')
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font=F;c.alignment=Alignment(vertical='top',wrap_text=c.column in (4,5))
def libro(nom,par,ids,lote):
    wb=openpyxl.Workbook();wb.remove(wb.active)
    ws=hoja(wb,'Revisión',COLS,W)
    for n,x in enumerate(ids,2): fila(ws,n,x)
    valid(ws,len(ids)+1)
    ins=wb.create_sheet('Instrucciones',0);ins.column_dimensions['A'].width=120
    for t in [f'Revisor: {nom}. Pareja: {nom} y {par} (lote {lote}, {len(ids)} estudios). Revisión de la bibliografía del proyecto original en Parsifal (jaime.meza, "Tendencias de los Procesos Evolutivos psicosociales").',
      'Se respeta lo que está en Parsifal: los mismos 250 estudios, los mismos criterios (hoja Criterios) y la decisión que cada estudio tiene hoy (columna B). Tu tarea es revisar si esa decisión es correcta.',
      'Solo llenas las columnas rojas: L DECISIÓN (Incluir, Excluir, Dudar o Duplicado), M MOTIVO si excluyes (EX1 a EX7) y N nota. La columna O se calcula sola e indica si coincides con Parsifal.',
      'Ejemplo de llenado: L = Excluir, M = EX4, N = "trata de turismo, no analiza al voluntario".',
      'La columna E trae el título en español. Para leer el resumen en español, elige Sí en la columna verde G de esa fila: la columna H lo traduce con Google en unos segundos. Hazlo fila por fila. La traducción es de apoyo: ante duda, manda el original.',
      'Trabaja SOLO en tu archivo y no mires el de tu pareja hasta terminar. Los desacuerdos entre la pareja, y con Parsifal, los resuelve un tercero. No se cambia nada en Parsifal hasta cerrar la revisión.',
      'No cambies el orden de las filas ni el número n.']:
        ins.append([t])
    for r in ins.iter_rows():
        for c in r: c.font=F;c.alignment=Alignment(wrap_text=True)
    ins['A4'].fill=EJ
    criterios(wb);wb.save(f'salida/Revision-Parsifal-original-{nom}.xlsx')
os.makedirs('salida',exist_ok=True)
for nom,par,m in [('Joel','Margarita',0),('Margarita','Joel',0),('Cristina','Anita',1),('Anita','Cristina',1)]: libro(nom,par,lotes[m],m+1)
# consolidado
wb=openpyxl.Workbook();wb.remove(wb.active)
ws=hoja(wb,'Los 250',['n','id Parsifal','estado en Parsifal','lote','año','título','título (español)','autores','revista','doi','fuente','clave bibtex'],[6,11,12,6,6,55,55,40,26,22,8,22])
lot={x['n']:(1 if x in lotes[0] else 2) for x in D}
SRC={'7':'Scopus','1':'IEEE','3':'ScienceDirect'}
for x in D: ws.append([x['n'],x['oid'],EST[x['status']],lot[x['n']],x['year'],' '.join((x['title'] or '').split()),x['tes'],x['author'],x['journal'],x['doi'],SRC.get(x['source'],x['source']),x['bibtex_key']])
for row in ws.iter_rows(min_row=2):
    for c in row: c.font=F
ws.auto_filter.ref=f'A1:L251'
criterios(wb);wb.save('salida/Consolidado-250-estudios-Parsifal-original.xlsx')
from collections import Counter
print([len(l) for l in lotes],[Counter(x['status'] for x in l) for l in lotes])
