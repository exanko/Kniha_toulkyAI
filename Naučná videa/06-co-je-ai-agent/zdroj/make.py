import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'nastroje'))
from engine import *
from engine import _off
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"casovani.json")))[LANG]
MONO=lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",s)
T={"cs":dict(q=["Co je vlastně","AI agent?"],brain="Jazykový model = mozek",smart="chytrý",hands="ruce",mem="paměť",
        tools="Agent mu dá nástroje.",tl=["web","soubory","programy"],memt="Dá mu paměť.",notes=["projekt: kniha","jazyky: CZ + EN","hlasy: Kuba, George"],next="Příště to ví.",
        recipe="Uloží si postup.",steps=["1. přepiš","2. načasuj","3. vyrenderuj"],skill="= SKILL",
        loop=["zkusí","zkontroluje","opraví"],goal="CÍL",careful="Jen pozor:",goes=["Jde přesně tam,","kam ho nasměruješ."],point="Tak ho nasměruj dobře."),
   "en":dict(q=["What actually is","an AI agent?"],brain="Language model = brain",smart="smart",hands="hands",mem="memory",
        tools="An agent gives it tools.",tl=["web","files","programs"],memt="It gives it memory.",notes=["project: book","languages: CZ + EN","voices: Kuba, George"],next="Next time, it knows.",
        recipe="It saves the recipe.",steps=["1. transcribe","2. time it","3. render"],skill="= SKILL",
        loop=["tries","checks","fixes"],goal="GOAL",careful="Just be careful:",goes=["It goes exactly","where you point it."],point="So point it well.")}[LANG]
K={"cs":dict(smart=3.07,tools=2.03,tstep=0.8,write=1.55,next=3.28,save=1.78,skill=3.05,goal=3.61,goes=1.08,point=3.48),
   "en":dict(smart=3.52,tools=2.44,tstep=0.75,write=1.93,next=3.47,save=1.79,skill=3.45,goal=4.27,goes=1.62,point=4.03)}[LANG]
D=durations(SEG)
def brain(d,cx,cy,r,a):
    if a<=0: return
    d.ellipse([cx-r,cy-r*0.82,cx+r,cy+r*0.82],fill=(192,76,255,int(60*a)),outline=mix(MG,a),width=5)
    d.line([(cx,cy-r*0.78),(cx,cy+r*0.78)],fill=mix(MG,0.6*a),width=4)
    for k in range(3):
        yy=cy-r*0.45+k*r*0.45
        for side in (-1,1):
            x0=cx+side*r*0.5; d.arc([x0-r*0.35,yy-r*0.18,x0+r*0.35,yy+r*0.18],200 if side<0 else 160,340 if side<0 else 380,fill=mix(MG,0.7*a),width=4)
def tick(d,cx,cy,a,col=CY,k=1.0):
    d.line([(cx-18*k,cy+2*k),(cx-4*k,cy+16*k),(cx+22*k,cy-14*k)],fill=mix(col,a),width=int(7*k),joint="curve")
def cross(d,cx,cy,a,k=1.0):
    for s in (1,-1): d.line([(cx-16*k,cy-16*k*s),(cx+16*k,cy+16*k*s)],fill=mix(RD,a),width=int(7*k))
def s1(t):
    im,d=new(); lines(d,560,T["q"],font("x",110),WH,fadein(t,0.1)); brain(d,540,1150,140,fadein(t,0.6)); return im
def s2(t):
    im,d=new()
    ctext(d,360,T["brain"],font("x",70 if LANG=="cs" else 64),WH,fadein(t,0.2))
    brain(d,540,820,220,fadein(t,0.5))
    rows=[(T["smart"],True),(T["hands"],False),(T["mem"],False)]
    for i,(w,ok) in enumerate(rows):
        a=fadein(t,K["smart"]+0.35*i); y=1150+i*120
        if a<=0: continue
        d.ellipse([330-34,y+8-34+_off(a),330+34,y+8+34+_off(a)],outline=mix(CY if ok else RD,a),width=4)
        (tick if ok else cross)(d,330,y+8+_off(a),a)
        d.text((400,y-30+_off(a)),w,font=font("x",64),fill=mix(CY if ok else RD,a))
    return im
def icon(d,kind,cx,cy,a):
    if kind==0:
        r=70; d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=mix(CY,a),width=5); d.ellipse([cx-r*0.45,cy-r,cx+r*0.45,cy+r],outline=mix(CY,a),width=4)
        d.line([(cx-r,cy),(cx+r,cy)],fill=mix(CY,a),width=4)
    elif kind==1:
        d.polygon([(cx-55,cy-70),(cx+25,cy-70),(cx+55,cy-40),(cx+55,cy+70),(cx-55,cy+70)],outline=mix(OR,a),fill=(255,179,71,int(40*a)))
        d.line([(cx-55,cy-70),(cx+25,cy-70),(cx+55,cy-40),(cx+55,cy+70),(cx-55,cy+70),(cx-55,cy-70)],fill=mix(OR,a),width=5)
        for k in range(3): d.line([(cx-35,cy-20+k*28),(cx+35,cy-20+k*28)],fill=mix(OR,0.8*a),width=4)
    else:
        d.rounded_rectangle([cx-80,cy-60,cx+80,cy+60],radius=12,fill=(10,12,26,int(230*a)),outline=mix(WH,0.7*a),width=4)
        d.text((cx-55,cy-34),">_",font=MONO(52),fill=mix((80,220,120),a))
def s3(t):
    im,d=new()
    ctext(d,340,T["tools"],font("x",84 if LANG=="cs" else 76),WH,fadein(t,0.2))
    brain(d,540,1080,120,fadein(t,0.4))
    P=[(220,760),(860,760),(540,1460)]
    for i,(x,y) in enumerate(P):
        a=fadein(t,K["tools"]+i*K["tstep"])
        if a<=0: continue
        d.line([(540,1080),(x,y)],fill=(255,255,255,int(70*a)),width=4)
        icon(d,i,x,y,a); ctext(d,y+95,T["tl"][i],font("sb",48),GR,a,x=x)
    return im
def s4(t):
    im,d=new()
    ctext(d,340,T["memt"],font("x",92 if LANG=="cs" else 84),WH,fadein(t,0.2))
    a=fadein(t,0.4)
    if a>0:
        d.rounded_rectangle([170,560,910,1260],radius=24,fill=(240,244,250,int(30*a)),outline=mix(WH,0.7*a),width=4)
        for k in range(9): d.ellipse([140,600+k*70,170,630+k*70],outline=mix(GR,a),width=3)
        f=MONO(44 if LANG=="cs" else 42)
        for i,l in enumerate(T["notes"]):
            vis=int(len(l)*max(0,min(1,(t-K["write"]-i*0.45)/0.45)))
            d.text((220,650+i*150),l[:vis],font=f,fill=mix([CY,OR,MG][i],a))
            d.line([(220,710+i*150),(860,710+i*150)],fill=(255,255,255,int(40*a)),width=2)
    n=fadein(t,K["next"])
    if n>0:
        f=font("x",66); tw=d.textlength(T["next"],font=f); x0=(W-tw-110)/2
        d.ellipse([x0,1350+_off(n),x0+90,1440+_off(n)],outline=mix(CY,n),width=5); tick(d,x0+45,1395+_off(n),n)
        d.text((x0+110,1355+_off(n)),T["next"],font=f,fill=mix(CY,n))
    return im
def s5(t):
    im,d=new()
    ctext(d,340,T["recipe"],font("x",92 if LANG=="cs" else 84),WH,fadein(t,0.2))
    a=fadein(t,K["save"]-0.4)
    if a>0:
        d.rounded_rectangle([230,560,850,1150],radius=28,fill=(255,179,71,int(40*a)),outline=mix(OR,a),width=5)
        d.rectangle([230,560,850,660],fill=(255,179,71,int(90*a)))
        ctext(d,578,"SKILL.md",font("x",56),WH,a)
        for i,s in enumerate(T["steps"]):
            b=fadein(t,K["save"]+0.3*i)
            d.text((290,720+i*130+_off(b)),s,font=font("sb",62),fill=mix(WH,b))
    ctext(d,1300,T["skill"],font("x",120),OR,fadein(t,K["skill"]))
    return im
def s6(t):
    im,d=new()
    cx,cy,R=540,980,290
    a=fadein(t,0.2)
    if a>0:
        d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=(255,255,255,int(60*a)),width=6)
        ang=(t*130)%360
        d.arc([cx-R,cy-R,cx+R,cy+R],ang,ang+70,fill=mix(CY,a),width=12)
        for i,w in enumerate(T["loop"]):
            th=math.radians(-90+i*120); x=cx+R*math.cos(th); y=cy+R*math.sin(th)
            act=((ang-(-90+i*120))%360)<75
            d.ellipse([x-26,y-26,x+26,y+26],fill=mix(CY if act else GR,a))
            f=font("x",58); tw=d.textlength(w,font=f)
            tx=x-tw/2; ty=y-110 if i==0 else y+75
            d.text((tx,ty),w,font=f,fill=mix(CY if act else WH,a))
    g=fadein(t,K["goal"])
    if g>0:
        d.ellipse([cx-120,cy-120,cx+120,cy+120],fill=(63,215,224,int(70*g)),outline=mix(CY,g),width=6)
        ctext(d,cy-100,T["goal"],font("x",54),WH,g); tick(d,cx,cy+30,g,WH,k=2.2)
    return im
def s7(t):
    im,d=new()
    ctext(d,330,T["careful"],font("x",92),OR,fadein(t,0.2))
    lines(d,470,T["goes"],font("x",76),WH,fadein(t,K["goes"]))
    tx,ty=760,1180
    b=fadein(t,K["goes"]+0.2)
    if b>0:
        for k,r in enumerate([150,100,50]): d.ellipse([tx-r,ty-r,tx+r,ty+r],outline=mix([WH,OR,RD][k],b),width=8)
    p=ease((t-K["goes"]-0.4)/1.2)
    if p>0:
        x0,y0=180,1320; x1=x0+(tx-x0)*p; y1=y0+(ty-y0)*p
        d.line([(x0,y0),(x1,y1)],fill=mix(CY,1),width=10)
        ang=math.atan2(ty-y0,tx-x0); hx,hy=x1,y1
        d.polygon([(hx,hy),(hx-40*math.cos(ang)+22*math.sin(ang),hy-40*math.sin(ang)-22*math.cos(ang)),(hx-40*math.cos(ang)-22*math.sin(ang),hy-40*math.sin(ang)+22*math.cos(ang))],fill=mix(CY,1))
    ctext(d,1460,T["point"],font("x",72 if LANG=="cs" else 76),CY,fadein(t,K["point"]))
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6,s7]))
if __name__=="__main__":
    main(SCENES,LANG,os.path.dirname(os.path.abspath(__file__)),[(i,D[i]-0.5) for i in range(7)])
