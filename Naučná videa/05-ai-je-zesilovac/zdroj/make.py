import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'nastroje'))
from engine import *
from engine import _off
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"casovani.json")))[LANG]
T={"cs":dict(q=["Co s tebou","vlastně udělá AI?"],amp="Hlavně tě zesílí.",inp="ty",out="ty × AI",all="Zesílí všechno, co do ní pustíš.",
        know=["Víš, co chceš.","Rozumíš svému oboru."],fast=["Za hodiny,","co dřív trvalo týdny."],
        lost="Nevíš, kam jdeš?",chaos="Zesílí ti zmatek.",piles="Hromada textu. Nic z toho.",
        err="Zesílí i chyby.",brief=["Špatné zadání se rozroste","rychleji než kdy dřív."],
        dir=["Než ji zapneš,","ujasni si směr."],you="Ten musíš dodat ty."),
   "en":dict(q=["What does AI","actually do to you?"],amp="Mostly, it amplifies you.",inp="you",out="you × AI",all="It boosts whatever you feed it.",
        know=["You know what you want.","You know your field."],fast=["Hours instead","of weeks."],
        lost="Don't know where you're going?",chaos="It amplifies the chaos.",piles="Piles of text. Nothing comes of it.",
        err="It amplifies mistakes too.",brief=["A bad brief grows","faster than ever."],
        dir=["Before you switch it on,","know your direction."],you="That part has to come from you.")}[LANG]
K={"cs":dict(amp=1.87,all=3.58,fast=3.13,chaos=1.80,piles=3.28,brief=2.16,dir=0.35,you=3.24),
   "en":dict(amp=2.73,all=4.02,fast=3.07,chaos=2.06,piles=4.05,brief=3.13,dir=2.20,you=3.78)}[LANG]
D=durations(SEG)
def sig(kind,x,t):
    if kind=="clean": return math.sin(x*0.045-t*5)
    if kind=="noise": return 0.55*math.sin(x*0.051-t*6)+0.45*math.sin(x*0.137+t*9.3)+0.35*math.sin(x*0.29-t*13.1)+0.3*math.sin(x*0.071*1.7+t*3.1)
    if kind=="spike":
        ph=((x*0.012-t*1.2)%1.0); return -(math.exp(-((ph-0.5)*14)**2)*1.6-0.15)
def amplifier(d,t,a,kind,cin,cout,gain=1.0,cy=1060):
    if a<=0: return
    pin=[(x,cy+28*sig(kind,x,t)) for x in range(70,381,4)]
    d.line(pin,fill=mix(cin,a),width=6)
    d.polygon([(430,cy-130),(430,cy+130),(660,cy)],fill=(255,255,255,int(28*a)),outline=mix(WH,0.8*a))
    d.line([(430,cy-130),(430,cy+130),(660,cy),(430,cy-130)],fill=mix(WH,0.8*a),width=5)
    g=ease(gain)
    pout=[(x,cy+150*g*sig(kind,x-620,t)) for x in range(700,1011,4)]
    d.line(pout,fill=mix(cout,a),width=8)
def s1(t):
    im,d=new(); lines(d,640,T["q"],font("x",104),WH,fadein(t,0.1)); return im
def s2(t):
    im,d=new()
    ctext(d,360,T["amp"],font("x",88 if LANG=="cs" else 82),CY,fadein(t,0.2))
    a=fadein(t,K["amp"]-0.4); amplifier(d,t,a,"clean",WH,CY,gain=(t-K["amp"])/1.0)
    ctext(d,1230,T["inp"],font("sb",50),GR,a,x=225); ctext(d,1230,T["out"],font("sb",50),CY,a,x=855)
    ctext(d,1440,T["all"],font("x",58 if LANG=="cs" else 60),OR,fadein(t,K["all"]))
    return im
def s3(t):
    im,d=new()
    for i,l in enumerate(T["know"]): ctext(d,330+i*110,l,font("x",80 if LANG=="cs" else 74),WH,fadein(t,0.2+0.6*i))
    amplifier(d,t,fadein(t,0.6),"clean",CY,CY,gain=(t-1.0)/1.0)
    lines(d,1380,T["fast"],font("x",76),CY,fadein(t,K["fast"]))
    return im
def s4(t):
    im,d=new()
    ctext(d,360,T["lost"],font("x",84 if LANG=="cs" else 66),WH,fadein(t,0.2))
    amplifier(d,t,fadein(t,K["chaos"]-0.6),"noise",MG,MG,gain=(t-K["chaos"])/0.8)
    ctext(d,520,T["chaos"],font("x",72),MG,fadein(t,K["chaos"]))
    p=fadein(t,K["piles"]-0.2)
    n=int(max(0,min(8,(t-K["piles"]+0.2)/0.12)))
    for k in range(n):
        x=540+((k*37)%60-30); y=1490-k*26
        d.rounded_rectangle([x-150,y-14,x+150,y+14],radius=4,fill=(240,244,250,int(200*p)),outline=mix(GR,p),width=2)
    ctext(d,1570,T["piles"],font("x",58 if LANG=="cs" else 52),OR,fadein(t,K["piles"]+0.6))
    return im
def s5(t):
    im,d=new()
    ctext(d,360,T["err"],font("x",90 if LANG=="cs" else 78),RD,fadein(t,0.2))
    amplifier(d,t,fadein(t,0.5),"spike",RD,RD,gain=(t-0.9)/1.0)
    lines(d,1360,T["brief"],font("x",68),OR,fadein(t,K["brief"]))
    return im
def s6(t):
    im,d=new()
    lines(d,360,T["dir"],font("x",86 if LANG=="cs" else 74),WH,fadein(t,K["dir"]-0.15))
    a=fadein(t,K["dir"]+0.3)
    if a>0:
        cx,cy,r=540,1030,200
        d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=mix(WH,0.6*a),width=6)
        for k in range(4):
            ang=math.radians(k*90); d.line([(cx+0.82*r*math.cos(ang),cy+0.82*r*math.sin(ang)),(cx+r*math.cos(ang),cy+r*math.sin(ang))],fill=mix(WH,0.6*a),width=6)
        wob=math.radians(-45+ 25*math.sin(t*3)*(1-ease((t-K["dir"]-0.3)/2.0)))
        tip=(cx+0.75*r*math.cos(wob),cy+0.75*r*math.sin(wob)); tail=(cx-0.45*r*math.cos(wob),cy-0.45*r*math.sin(wob))
        nx,ny=-math.sin(wob),math.cos(wob)
        d.polygon([tip,(cx+26*nx,cy+26*ny),tail,(cx-26*nx,cy-26*ny)],fill=mix(OR,a))
        d.ellipse([cx-16,cy-16,cx+16,cy+16],fill=mix(WH,a))
    ctext(d,1400,T["you"],font("x",74 if LANG=="cs" else 60),CY,fadein(t,K["you"]))
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6]))
if __name__=="__main__":
    main(SCENES,LANG,os.path.dirname(os.path.abspath(__file__)),[(i,D[i]-0.5) for i in range(6)])
