import csv
rest=set(open('restaurar.txt').read().split())
r=list(csv.DictReader(open('prelectura.csv',encoding='utf8')))
f=list(r[0].keys())
for x in r:
    if x['categoria']=='X_excluir' and x['id'] in rest:
        x['categoria']='B_duda'; x['motivo']='restaurado tras lectura manual de la exclusion'
para=[x for x in r if x['categoria']!='X_excluir']
exc=[x for x in r if x['categoria']=='X_excluir']
for n,rows in (('para-cribar.csv',para),('excluidos-propuestos.csv',exc)):
    w=csv.DictWriter(open(n,'w',newline='',encoding='utf-8-sig'),fieldnames=f);w.writeheader();w.writerows(rows)
w=csv.DictWriter(open('prelectura.csv','w',newline='',encoding='utf-8-sig'),fieldnames=f);w.writeheader();w.writerows(r)
from collections import Counter
print(Counter(x['categoria'] for x in r),len(para),len(exc))
