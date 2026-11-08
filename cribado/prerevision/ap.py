import sys
# uso: python3 ap.py "R00046 P, R00047 P ..."  ; tambien acepta lineas
t=sys.stdin.read().replace(',', '\n').split('\n')
with open('decisiones.tsv','a') as f:
    for x in t:
        x=x.split()
        if len(x)>=2: f.write(f"R{int(x[0].lstrip('R')):05d}\t{x[1]}\n")
