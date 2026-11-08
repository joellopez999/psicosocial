import csv,sys,os,re
d=dict(l.split() for l in open('decisiones.tsv'))
P={r['id']:r for f in ('../para-cribar.csv','../excluidos-propuestos.csv') for r in csv.DictReader(open(f,encoding='utf-8-sig'))}
done=set()
if os.path.exists('titulos_es.tsv'): done={l.split('\t')[0] for l in open('titulos_es.tsv') if '\t' in l}
pend=[i for i in sorted(d) if d[i] in 'PD' and i not in done]
print('pend',len(pend))
for i in pend[:int(sys.argv[1])]:
    t=re.sub(r'\s*;\s*\[.*$','',P[i]['titulo'])  # quitar títulos alternativos entre corchetes
    print(i[1:].lstrip('0'),t[:180])
