import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'nastroje'))
from engine import *
from engine import _off
import numpy as np
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"casovani.json")))[LANG]
T={"cs":dict(q=["Když něco nevidíme,","znamená to,","že to neexistuje?"],radio=["Rádiové vlny","tu byly odjakživa."],device="Chyběl jen přístroj.",
        antenna="Porucha antény?",noise="šum",whatif="Co když to není šum?",nothing=["Naše „nic“","není důkaz."],proof="Nemáme na to nástroj.",
        ai=["AI najde vzory,","které přehlédneme."],fake=["…i vzor,","který tam není."],check="Každý objev ověř."),
   "en":dict(q=["If we can't see it,","does that mean","it isn't there?"],radio=["Radio waves","were always here."],device="We just lacked the device.",
        antenna="A faulty antenna?",noise="noise",whatif="What if it isn't noise?",nothing=["Our “nothing”","isn't proof."],proof="We lack the tool to see it.",
        ai=["AI finds patterns","people miss."],fake=["…and patterns","that aren't there."],check="Every discovery needs checking.")}[LANG]
K={"cs":dict(radio=1.47,device=3.77,noise=4.89,whatif=7.46,proof=4.13,why=3.57),
   "en":dict(radio=1.70,device=3.95,noise=5.30,whatif=8.13,proof=4.74,why=3.71)}[LANG]
D=durations(SEG)
rng=np.random.default_rng(3)
PTS_LINE=[(x, 0.55*x+rng.normal(0,40)) for x in rng.uniform(0,640,26)]
PTS_RAND=[(x,y) for x,y in zip(rng.uniform(0,640,26),rng.uniform(0,420,26))]
def s1(t):
    im,d=new()
    for i,l in enumerate(T["q"]): ctext(d,520+i*115,l,font("x",88 if LANG=="cs" else 84),CY if i==2 else WH,fadein(t,0.1+0.3*i))
    a=fadein(t,1.0)
    if a>0:
        d.ellipse([400,1050,680,1330],fill=(0,0,0,int(160*a)),outline=mix(GR,0.5*a),width=4)
        ctext(d,1110,"?",font("x",130),GR,a)
    return im
def s2(t):
    im,d=new()
    lines(d,340,T["radio"],font("x",92),WH,fadein(t,K["radio"]-0.3))
    dev=fadein(t,K["device"]-0.2)
    for k in range(3):
        y0=900+k*150; amp=45
        pts=[(x,y0+amp*math.sin(x*0.02-t*4+k)) for x in range(60,1021,6)]
        d.line(pts,fill=(63,215,224,int(255*(0.10+0.9*dev))),width=6)
    if dev>0:
        ax=900; d.line([(ax,1500),(ax,1300)],fill=mix(WH,dev),width=8)
        for r in (40,80,120): d.arc([ax-r,1300-r,ax+r,1300+r],210,330,fill=mix(OR,dev),width=6)
        d.ellipse([ax-14,1286,ax+14,1314],fill=mix(OR,dev))
    ctext(d,1560,T["device"],font("x",70 if LANG=="cs" else 64),OR,fadein(t,K["device"]))
    return im
def s3(t):
    im,d=new()
    ctext(d,330,T["antenna"],font("x",90),WH,fadein(t,0.2))
    a=fadein(t,0.5)
    if a>0:
        x0,y0,w,h=140,560,800,700
        r=np.random.default_rng(int(t*30)).integers(0,255,(70,80)).astype(np.uint8)
        sig=fadein(t,K["whatif"],1.2)
        if sig>0:
            yy,xx=np.mgrid[0:70,0:80]
            band=np.exp(-((yy-35-14*np.sin(xx/9))**2)/18.0)
            r=np.clip(r*(1-0.7*sig*band)+255*0.0*band,0,255).astype(np.uint8)
        nimg=Image.fromarray(r).resize((w,h),Image.NEAREST).convert("L")
        layer=Image.new("RGBA",(w,h),(200,210,230,0)); layer.putalpha(nimg.point(lambda v:int(v*0.55*a)))
        im.alpha_composite(layer,(x0,y0)); d=ImageDraw.Draw(im)
        d.rounded_rectangle([x0,y0,x0+w,y0+h],radius=20,outline=mix(WH,0.6*a),width=4)
        if sig>0:
            pts=[(x0+x*10,y0+(35+14*math.sin(x/9))*10) for x in range(0,81)]
            d.line(pts,fill=mix(CY,sig),width=10)
        ctext(d,y0+h+30,T["noise"],font("sb",50),GR,fadein(t,K["noise"]),x=540)
    ctext(d,1480,T["whatif"],font("x",72 if LANG=="cs" else 70),CY,fadein(t,K["whatif"]))
    return im
def s4(t):
    im,d=new()
    lines(d,330,T["nothing"],font("x",96),WH,fadein(t,0.2))
    a=fadein(t,0.6)
    if a>0:
        sweep=math.sin(t*0.8)*0.35
        cx,cy=540,1500; ang=-math.pi/2+sweep; spread=0.28; L=760
        p1=(cx+L*math.cos(ang-spread),cy+L*math.sin(ang-spread)); p2=(cx+L*math.cos(ang+spread),cy+L*math.sin(ang+spread))
        d.polygon([(cx,cy),p1,p2],fill=(255,240,200,int(55*a)))
        objs=[(300,900,MG),(760,820,OR),(520,1000,CY),(250,1180,CY),(850,1150,MG),(640,760,WH)]
        for x,y,c in objs:
            th=math.atan2(y-cy,x-cx); lit=abs(((th-ang+math.pi)%(2*math.pi))-math.pi)<spread
            d.ellipse([x-30,y-30,x+30,y+30],fill=mix(c,a*(0.95 if lit else 0.06)))
        d.rounded_rectangle([cx-40,cy-10,cx+40,cy+90],radius=12,fill=mix(GR,a))
    ctext(d,1640,T["proof"],font("x",64 if LANG=="cs" else 58),OR,fadein(t,K["proof"]))
    return im
def plot(d,pts,a,col,ox=220,oy=760):
    for x,y in pts: d.ellipse([ox+x-12,oy+420-y*0.75-12,ox+x+12,oy+420-y*0.75+12],fill=mix(col,a))
def s5(t):
    im,d=new()
    lines(d,330,T["ai"],font("x",86 if LANG=="cs" else 80),WH,fadein(t,0.2))
    plot(d,PTS_LINE,fadein(t,0.5),WH)
    p=ease((t-1.3)/1.2)
    if p>0:
        x1=640*p; d.line([(220,760+420),(220+x1,760+420-0.55*x1*0.75)],fill=mix(CY,1),width=10)
    return im
def s6(t):
    im,d=new()
    lines(d,330,T["fake"],font("x",86 if LANG=="cs" else 80),RD,fadein(t,0.2))
    plot(d,PTS_RAND,fadein(t,0.4),WH)
    p=ease((t-1.0)/1.4)
    if p>0:
        x1=640*p; pts=[(220+x,760+420-(200+120*math.sin(x/90))*0.9) for x in range(0,int(x1)+1,8)]
        if len(pts)>1:
            for k in range(0,len(pts)-1,2): d.line([pts[k],pts[k+1]],fill=mix(RD,1),width=8)
    w=fadein(t,K["why"])
    if w>0:
        cx,cy=800,1330
        d.ellipse([cx-90,cy-90,cx+90,cy+90],outline=mix(CY,w),width=12); d.line([(cx+64,cy+64),(cx+140,cy+140)],fill=mix(CY,w),width=22)
    ctext(d,1540,T["check"],font("x",68 if LANG=="cs" else 58),CY,w)
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6]))
if __name__=="__main__":
    main(SCENES,LANG,os.path.dirname(os.path.abspath(__file__)),[(i,D[i]-0.5) for i in range(6)])
