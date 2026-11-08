# uso: python3 apr.py "ids..." "excepciones id:cod ..."  (resto P). ids como rango a-b o lista
import sys,subprocess
done={l.split('\t')[0] for l in open('decisiones.tsv')}
import csv
r=sorted(x['id'] for x in csv.DictReader(open('../para-cribar.csv',encoding='utf-8-sig')))
pend=[x for x in r if x not in done]
hasta=int(sys.argv[1]); exc=dict(t.split(':') for t in sys.argv[2].split()) if len(sys.argv)>2 else {}
with open('decisiones.tsv','a') as f:
    n=0
    for x in pend:
        if int(x[1:])>hasta: break
        f.write(f"{x}\t{exc.get(str(int(x[1:])),'P')}\n"); n+=1
print('anotados',n,'excepciones',len(exc))
