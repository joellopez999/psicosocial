import csv,sys,os
H=os.path.dirname(os.path.abspath(__file__))
r=list(csv.DictReader(open(H+'/../para-cribar.csv',encoding='utf-8-sig')))
r.sort(key=lambda x:x['id'])
done=set()
if os.path.exists(H+'/decisiones.tsv'):
    done={l.split('\t')[0] for l in open(H+'/decisiones.tsv') if l.strip()}
n=int(sys.argv[1]) if len(sys.argv)>1 else 55; L=int(sys.argv[2]) if len(sys.argv)>2 else 520
pend=[x for x in r if x['id'] not in done]
print(f'hechos {len(done)} pendientes {len(pend)}')
for x in pend[:n]:
    a=' '.join(x['resumen'].split())
    print(f"{x['id']}|{x['anio']}|{x['titulo'][:200]}|| {a[:L]}")
