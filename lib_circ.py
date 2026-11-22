"""Leitor mínimo de arquivos .circ do Logisim (portas AND/OR/XOR/NOT, fios, pinos e túneis)."""
import xml.etree.ElementTree as ET, re
OFF={"AND Gate":[(-50,-20),(-50,20)],"OR Gate":[(-50,-20),(-50,20)],"XOR Gate":[(-60,-20),(-60,20)],"NOT Gate":[(-30,0)]}
F={"AND Gate":lambda v:int(all(v)),"OR Gate":lambda v:int(any(v)),"XOR Gate":lambda v:sum(v)%2,"NOT Gate":lambda v:1-v[0]}
pt=lambda s:tuple(int(n) for n in re.findall(r"-?\d+",s))
def avaliador(caminho,nome):
    circ=[c for c in ET.parse(caminho).getroot().iter("circuit") if c.get("name")==nome][0]
    pai={}
    def f(a):
        pai.setdefault(a,a)
        while pai[a]!=a: pai[a]=pai[pai[a]]; a=pai[a]
        return a
    def u(a,b): pai[f(a)]=f(b)
    tun={}; pinos=[]; portas=[]
    for w in circ.iter("wire"): u(pt(w.get("from")),pt(w.get("to")))
    for c in circ.iter("comp"):
        n=c.get("name"); loc=pt(c.get("loc")); a={x.get("name"):x.get("val") for x in c.findall("a")}
        if n=="Tunnel": tun.setdefault(a["label"],[]).append(loc); f(loc)
        elif n=="Pin": pinos.append((a.get("label"),a.get("output")=="true",loc)); f(loc)
        elif n in OFF:
            k=int(a.get("inputs","5" if n!="NOT Gate" else "1")); assert k==len(OFF[n]),"número de entradas inesperado"
            portas.append((n,[f((loc[0]+dx,loc[1]+dy)) for dx,dy in OFF[n]],f(loc)))
    for ps in tun.values():
        for p in ps[1:]: u(ps[0],p)
    portas=[(n,[f(i) for i in ins],f(o)) for n,ins,o in portas]
    def avaliar(entradas):
        v={f(l):entradas[r] for r,o,l in pinos if not o}
        for _ in range(100):
            ch=False
            for n,ins,o in portas:
                if all(i in v for i in ins):
                    r=F[n]([v[i] for i in ins])
                    if v.get(o)!=r: v[o]=r; ch=True
            if not ch: break
        return {r:v.get(f(l)) for r,o,l in pinos if o}
    return avaliar
