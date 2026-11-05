import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'nastroje'))
from engine import *
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"casovani.json")))[LANG]
T={"cs":dict(q=["Proč si doma","nepostavíš vlastní","velkou AI?"],qc=2,
        big="Velký model je obří.",nofit="Nevejde se do jedné karty.",model="MODEL",
        split=["Tak ho rozdělíš","na víc karet."],every="Při každém slově si karty",every2="předávají data.",
        home=["Doma je spojuje","základní deska."],string="Mozek spojený provázkem.",
        dc=["V datovém centru:","superrychlé propojení."],stays="Mozek drží pohromadě.",
        why="Proto:",dcl="Datové centrum",dcs="největší modely",hl="Doma",hs="menší modely"),
   "en":dict(q=["Why can't you build","your own","big AI at home?"],qc=2,
        big="A big model is huge.",nofit="It doesn't fit on one card.",model="MODEL",
        split=["So you split it","across several cards."],every="For every single word,",every2="the cards pass data.",
        home=["At home, they talk","through the motherboard."],string="A brain tied with string.",
        dc=["In a data center:","super-fast links."],stays="The brain stays in one piece.",
        why="That's why:",dcl="Data center",dcs="the biggest models",hl="At home",hs="smaller models")}[LANG]
K={"cs":dict(nofit=1.97,every=2.17,string=2.58,stays=4.12,home=3.26),
   "en":dict(nofit=2.78,every=3.11,string=2.94,stays=4.52,home=3.39)}[LANG]
D=durations(SEG)
def gpu(d,cx,cy,w,h,a,frac=0,fcol=MG,warn=0):
    if a<=0: return
    oc=RD if warn>0.5 else WH
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],radius=22,fill=(28,34,64,int(200*a)),outline=mix(oc,0.55*a+0.45*warn*a),width=4)
    if frac>0:
        d.rounded_rectangle([cx-w/2+10,cy-h/2+10,cx-w/2+10+(w-20)*frac,cy+h/2-10],radius=16,fill=(fcol[0],fcol[1],fcol[2],int(110*a)))
    r=h*0.30
    for fx in (cx-w*0.22,cx+w*0.22):
        d.ellipse([fx-r,cy-r,fx+r,cy+r],outline=mix(GR,0.8*a),width=4)
        d.ellipse([fx-r*0.25,cy-r*0.25,fx+r*0.25,cy+r*0.25],fill=mix(GR,0.7*a))
    d.rectangle([cx-w*0.32,cy+h/2,cx+w*0.32,cy+h/2+14],fill=mix(OR,0.8*a))
def s1(t):
    im,d=new(); f=font("x",104 if LANG=="cs" else 94)
    for i,l in enumerate(T["q"]): ctext(d,600+i*130,l,f,CY if i==T["qc"] else WH,fadein(t,0.1+0.3*i))
    return im
def s2(t):
    im,d=new()
    ctext(d,380,T["big"],font("x",92),WH,fadein(t,0.2))
    a=fadein(t,0.3); warn=fadein(t,K["nofit"],0.3)
    g=ease((t-0.8)/0.9)
    if g>0:
        mw,mh=440+420*g,240+300*g
        d.rounded_rectangle([540-mw/2,1100-mh/2,540+mw/2,1100+mh/2],radius=30,outline=mix(MG,g),width=6,fill=(192,76,255,int(40*g)))
        ctext(d,1100-mh/2+24,T["model"],font("x",56),MG,g)
    gpu(d,540,1130,440,240,a,warn=warn)
    ctext(d,1520,T["nofit"],font("x",72),OR,warn)
    return im
POS=[(290,960),(790,960),(290,1300),(790,1300)]
def s3(t):
    im,d=new()
    lines(d,330,T["split"],font("x",90),WH,fadein(t,0.2))
    for i,(x,y) in enumerate(POS):
        a=fadein(t,0.4+i*0.15); fr=ease((t-0.9-i*0.2)/0.6)
        gpu(d,x,y,400,220,a,frac=fr)
    e=fadein(t,K["every"])
    if e>0:
        links=[(0,1),(1,3),(3,2),(2,0)]
        for k,(p,q) in enumerate(links):
            (x1,y1),(x2,y2)=POS[p],POS[q]
            d.line([x1,y1,x2,y2],fill=(255,255,255,int(50*e)),width=3)
            for j in range(3):
                s=((t*0.9+j/3+k*0.17)%1.0); px=x1+(x2-x1)*s; py=y1+(y2-y1)*s
                d.ellipse([px-11,py-11,px+11,py+11],fill=mix(CY,e))
    ctext(d,1530,T["every"],font("sb",62),OR,e); ctext(d,1610,T["every2"],font("sb",62),OR,fadein(t,K["every"]+0.2))
    return im
def hemis(d,gap,a,cy=1060):
    cx=540; w=330; h=380
    for side in (-1,1):
        x0=cx+side*(gap/2+w/2)
        d.ellipse([x0-w/2,cy-h/2,x0+w/2,cy+h/2],fill=(192,76,255,int(55*a)),outline=mix(MG,a),width=5)
        for k in range(4):
            yy=cy-h*0.32+k*h*0.21; ww=w*(0.62-0.08*abs(k-1.5))
            d.arc([x0-ww/2,yy-36,x0+ww/2,yy+36],200 if side<0 else 160,340 if side<0 else 380,fill=mix(MG,0.7*a),width=4)
    return cx-gap/2, cx+gap/2
def s4(t):
    im,d=new()
    lines(d,330,T["home"],font("x",84 if LANG=="cs" else 76),WH,fadein(t,0.2))
    a=fadein(t,0.4); xl,xr=hemis(d,190,a)
    if a>0:
        pts=[(xl+(xr-xl)*k/40, 1060+14*math.sin(k/40*math.pi*3+t*1.5)) for k in range(41)]
        d.line(pts,fill=(205,160,105,int(255*a)),width=5)
        for j in range(2):
            s=((t*0.12+j*0.5)%1.0); k=int(s*40); px,py=pts[k]
            d.ellipse([px-9,py-9,px+9,py+9],fill=mix(OR,a))
    ctext(d,1450,T["string"],font("x",72),OR,fadein(t,K["string"]))
    return im
def s5(t):
    im,d=new()
    lines(d,330,T["dc"],font("x",84),WH,fadein(t,0.2))
    a=fadein(t,0.2); g=ease((t-0.4)/1.2); gap=190-120*g
    xl,xr=hemis(d,gap,a)
    bw=ease((t-0.8)/0.8)
    if bw>0:
        d.rounded_rectangle([xl-110,1060-80*bw,xr+110,1060+80*bw],radius=40,fill=(63,215,224,int(150*bw)))
        for j in range(10):
            s=((t*1.6+j/10)%1.0); px=xl-100+(xr-xl+200)*s; py=1060+((j%3)-1)*40*bw
            d.ellipse([px-8,py-8,px+8,py+8],fill=mix(WH,bw))
    ctext(d,1450,T["stays"],font("x",70),CY,fadein(t,K["stays"]))
    return im
def rack(d,x,y0,y1,w,a):
    d.rounded_rectangle([x-w/2,y0,x+w/2,y1],radius=18,fill=(28,34,64,int(210*a)),outline=mix(WH,0.5*a),width=4)
    n=int((y1-y0-30)//60)
    for k in range(n):
        yy=y0+20+k*60; d.rounded_rectangle([x-w/2+20,yy,x+w/2-20,yy+40],radius=8,outline=mix(GR,0.6*a),width=2)
        for j in range(3): d.ellipse([x+w/2-90+j*22,yy+14,x+w/2-78+j*22,yy+26],fill=mix(CY if (k+j)%2 else OR,a))
def s6(t):
    im,d=new()
    ctext(d,360,T["why"],font("x",96),WH,fadein(t,0.2))
    a=fadein(t,0.4); rack(d,300,640,1300,300,a)
    ctext(d,1340,T["dcl"],font("x",56),CY,a,x=300); ctext(d,1415,T["dcs"],font("m",46),WH,a,x=300)
    b=fadein(t,K["home"]); 
    if b>0:
        d.rounded_rectangle([700,1060,860,1300],radius=16,fill=(28,34,64,int(210*b)),outline=mix(WH,0.5*b),width=4)
        d.ellipse([768,1100,792,1124],fill=mix(OR,b)); d.rounded_rectangle([720,1160,840,1180],radius=6,fill=mix(GR,0.6*b))
    ctext(d,1340,T["hl"],font("x",56),OR,b,x=780); ctext(d,1415,T["hs"],font("m",46),WH,b,x=780)
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6]))
if __name__=="__main__":
    main(SCENES,LANG,os.path.dirname(os.path.abspath(__file__)),[(0,2.5),(1,D[1]-0.5),(2,D[2]-0.5),(3,D[3]-0.5),(4,D[4]-0.5),(5,D[5]-0.6)])
