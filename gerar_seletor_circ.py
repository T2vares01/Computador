#!/usr/bin/env python3
"""Gera circuitos/seletor.circ (Logisim 2.7.1) só com portas de 2 entradas e túneis.

Funciona em qualquer versão do Logisim: não depende do modo do XOR de várias entradas
nem de entradas soltas. Contém dois circuitos:
  seletor           P=1,N=0 -> A OR B | P=0,N=1 -> A AND B | P=1,N=1 -> A XNOR B | P=0,N=0 -> A NOR B
  seletor_com_NOT   o mesmo, com um NOT na saída (NOR, NAND, XOR, OR)
"""
import os
OFF={"AND":[(-50,-20),(-50,20)],"OR":[(-50,-20),(-50,20)],"XOR":[(-60,-20),(-60,20)],"NOT":[(-30,0)]}
NAME={"AND":"AND Gate","OR":"OR Gate","XOR":"XOR Gate","NOT":"NOT Gate"}
HEADER='''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<project source="2.7.1" version="1.0">
This file is intended to be loaded by Logisim (http://www.cburch.com/logisim/).
<lib desc="#Wiring" name="0">
<tool name="Constant">
<a name="facing" val="north"/>
</tool>
</lib>
<lib desc="#Gates" name="1"/>
<lib desc="#Plexers" name="2"/>
<lib desc="#Arithmetic" name="3"/>
<lib desc="#Memory" name="4"/>
<lib desc="#I/O" name="5"/>
<lib desc="#Base" name="6">
<tool name="Text Tool">
<a name="text" val=""/>
<a name="font" val="SansSerif plain 12"/>
<a name="halign" val="center"/>
<a name="valign" val="base"/>
</tool>
</lib>
<main name="seletor"/>
<options>
<a name="gateUndefined" val="error"/>
<a name="simlimit" val="1000"/>
<a name="simrand" val="0"/>
</options>
<mappings>
<tool lib="6" map="Button2" name="Menu Tool"/>
<tool lib="6" map="Button3" name="Menu Tool"/>
<tool lib="6" map="Ctrl Button1" name="Menu Tool"/>
</mappings>
<toolbar>
<tool lib="6" name="Poke Tool"/>
<tool lib="6" name="Edit Tool"/>
<sep/>
<tool lib="0" name="Pin">
<a name="facing" val="north"/>
<a name="tristate" val="false"/>
</tool>
<tool lib="0" name="Pin">
<a name="facing" val="west"/>
<a name="output" val="true"/>
<a name="labelloc" val="east"/>
</tool>
<tool lib="1" name="NOT Gate"/>
<tool lib="1" name="AND Gate"/>
<tool lib="1" name="OR Gate"/>
</toolbar>
'''
def circuito(nome, com_not):
    g=[("AND",300,100,["A","B"],"G1"),("OR",300,200,["A","B"],"G2"),("XOR",300,300,["A","B"],"X"),
       ("NOT",460,300,["X"],"G3"),("NOT",300,400,["P"],"nP"),("NOT",300,480,["N"],"nN"),
       ("AND",560,100,["G1","nP"],"u1"),("AND",720,100,["u1","N"],"T1"),
       ("AND",560,200,["G2","P"],"u2"),("AND",720,200,["u2","nN"],"T2"),
       ("AND",560,300,["G3","P"],"u3"),("AND",720,300,["u3","N"],"T3"),
       ("OR",560,400,["G2","P"],"u4"),("OR",720,400,["u4","N"],"u5"),("NOT",880,400,["u5"],"T4"),
       ("OR",1040,150,["T1","T2"],"S1"),("OR",1200,250,["S1","T3"],"S2"),
       ("OR",1360,350,["S2","T4"],"Y" if com_not else "X_out")]
    if com_not: g.append(("NOT",1500,350,["Y"],"X_out"))
    comps=[];wires=[]
    def tun(x,y,lab,face): comps.append('<comp lib="0" loc="(%d,%d)" name="Tunnel">\n<a name="facing" val="%s"/>\n<a name="label" val="%s"/>\n</comp>'%(x,y,face,lab))
    def wire(a,b): wires.append('<wire from="(%d,%d)" to="(%d,%d)"/>'%(a[0],a[1],b[0],b[1]))
    for t,x,y,ins,out in g:
        if t=="NOT": comps.append('<comp lib="1" loc="(%d,%d)" name="NOT Gate"/>'%(x,y))
        else: comps.append('<comp lib="1" loc="(%d,%d)" name="%s">\n<a name="inputs" val="2"/>\n</comp>'%(x,y,NAME[t]))
        for (dx,dy),n in zip(OFF[t],ins):
            p=(x+dx,y+dy); wire(p,(p[0]-20,p[1])); tun(p[0]-20,p[1],n,"east")
        wire((x,y),(x+20,y)); tun(x+20,y,out,"west")
    for i,n in enumerate("ABPN"):
        y=100+i*60; comps.append('<comp lib="0" loc="(100,%d)" name="Pin">\n<a name="tristate" val="false"/>\n<a name="label" val="%s"/>\n</comp>'%(y,n))
        wire((100,y),(130,y)); tun(130,y,n,"west")
    xo=1700 if com_not else 1560
    comps.append('<comp lib="0" loc="(%d,350)" name="Pin">\n<a name="facing" val="west"/>\n<a name="output" val="true"/>\n<a name="label" val="X"/>\n<a name="labelloc" val="east"/>\n</comp>'%xo)
    wire((xo-30,350),(xo,350)); tun(xo-30,350,"X_out","east")
    return '<circuit name="%s">\n<a name="circuit" val="%s"/>\n<a name="clabel" val=""/>\n<a name="clabelup" val="east"/>\n<a name="clabelfont" val="SansSerif plain 12"/>\n%s\n%s\n</circuit>\n'%(nome,nome,"\n".join(wires),"\n".join(comps))
def gerar(caminho):
    txt=HEADER+circuito("seletor",False)+circuito("seletor_com_NOT",True)+"</project>\n"
    open(caminho,"w",encoding="utf-8").write(txt)
if __name__=="__main__":
    gerar(os.path.join(os.path.dirname(os.path.abspath(__file__)),"seletor.circ"))
    print("seletor.circ gerado")
