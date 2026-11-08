import sys
with open('titulos_es.tsv','a') as f:
    for l in sys.stdin:
        l=l.strip()
        if not l: continue
        n,t=l.split(' ',1); f.write(f"R{int(n):05d}\t{t}\n")
