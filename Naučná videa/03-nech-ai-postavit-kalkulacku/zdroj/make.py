import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'nastroje'))
from engine import *
from engine import _off
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"casovani.json")))[LANG]
MONO=lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",s)
T={"cs":dict(q=["Chceš, aby AI","spočítala","tvoje data?"],catch="Má to háček.",lm="Jazykový model",calc="kalkulačka",
        pred=["Odhaduje, jak vypadá","správná odpověď."],ok="Správně:",ai="AI:",notice="A na první pohled to nepoznáš.",
        instead="Zkus to jinak.",prompt=["„Napiš mi program,","který to spočítá.“"],
        code=["data = nacti('tabulka.csv')","print(sum(data))"],
        checks=["Jednou ho zkontroluješ","Počítá přesně","Pokaždé stejně","Zůstane ti"],
        end1=["AI nemá dělat","kalkulačku."],end2="Má ti ji postavit.",num_ok="48 213",num_ai="48 312"),
   "en":dict(q=["Want AI","to crunch","your numbers?"],catch="There's a catch.",lm="Language model",calc="calculator",
        pred=["It predicts what the","right answer looks like."],ok="Correct:",ai="AI:",notice="At first glance, you won't notice.",
        instead="Try this instead.",prompt=["\"Write me a program","that calculates it.\""],
        code=["data = load('sheet.csv')","print(sum(data))"],
        checks=["Check it once","Calculates exactly","Same way every time","You get to keep it"],
        end1=["Don't make AI","your calculator."],end2="Have it build you one.",num_ok="48,213",num_ai="48,312")}[LANG]
K={"cs":dict(lm=1.56,pred=4.47,notice=2.71,tell=1.26,prog=2.01,c=[0.4,2.28,3.75,4.92],build=2.66),
   "en":dict(lm=1.65,pred=4.98,notice=3.36,tell=1.91,prog=2.66,c=[0.4,2.25,4.41,6.22],build=2.94)}[LANG]
D=durations(SEG)
def calc_icon(d,cx,cy,s,a,nbtn=12):
    if a<=0: return
    w,h=220*s,320*s
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],radius=24*s,fill=(28,34,64,int(220*a)),outline=mix(WH,0.55*a),width=4)
    d.rounded_rectangle([cx-w/2+18*s,cy-h/2+18*s,cx+w/2-18*s,cy-h/2+80*s],radius=10*s,fill=mix(CY,0.35*a))
    for k in range(min(nbtn,12)):
        r,c=divmod(k,3); bx=cx-w/2+28*s+c*58*s; by=cy-h/2+100*s+r*52*s
        d.rounded_rectangle([bx,by,bx+44*s,by+38*s],radius=8*s,fill=mix(OR if c==2 else GR,0.75*a))
def grid(d,a,cy=1000):
    if a<=0: return
    x0,x1=150,930; rows=6; rh=70
    for r in range(rows+1): d.line([x0,cy+r*rh,x1,cy+r*rh],fill=(255,255,255,int(60*a)),width=2)
    for c in range(4): xx=x0+c*(x1-x0)/3; d.line([xx,cy,xx,cy+rows*rh],fill=(255,255,255,int(60*a)),width=2)
    f=MONO(34)
    for r in range(rows):
        for c in range(3):
            v=f"{(r*7919+c*104729)%9000+1000}"; d.text((x0+20+c*(x1-x0)/3,cy+r*rh+16),v,font=f,fill=mix(GR,0.8*a))
def s1(t):
    im,d=new()
    for i,l in enumerate(T["q"]): ctext(d,420+i*120,l,font("x",100),CY if i==2 else WH,fadein(t,0.1+0.25*i))
    grid(d,fadein(t,0.6),cy=900)
    return im
def s2(t):
    im,d=new()
    ctext(d,360,T["catch"],font("x",96),OR,fadein(t,0.2))
    a=fadein(t,K["lm"])
    if a>0:
        d.rounded_rectangle([90,820,450,1120],radius=36,fill=(192,76,255,int(60*a)),outline=mix(MG,a),width=5)
        ctext(d,920,"AI",font("x",110),WH,a,x=270)
        ctext(d,1150,T["lm"],font("sb",44),MG,a,x=270)
        ctext(d,890,"≠",font("x",170),WH,fadein(t,K["lm"]+0.4))
        calc_icon(d,810,970,0.95,fadein(t,K["lm"]+0.6))
        ctext(d,1150,T["calc"],font("sb",44),OR,fadein(t,K["lm"]+0.6),x=810)
    lines(d,1360,T["pred"],font("x",70),CY,fadein(t,K["pred"]))
    return im
def s3(t):
    im,d=new()
    grid(d,fadein(t,0.2),cy=380)
    a=fadein(t,0.6); n=fadein(t,K["notice"])
    f=font("x",100); y1,y2=950,1110
    ctext(d,y1,T["ok"],font("sb",52),GR,a,x=330); ctext(d,y2,T["ai"],font("sb",52),GR,a,x=330)
    if a>0:
        x=520; d.text((x,y1-30+_off(a)),T["num_ok"],font=f,fill=mix(CY,a))
        # AI number, highlight swapped digits on "notice"
        s=T["num_ai"]; xx=x
        for i,ch in enumerate(s):
            col=RD if (n>0 and i in (3,5)) else WH
            d.text((xx,y2-30+_off(a)),ch,font=f,fill=mix(col,a)); xx+=d.textlength(ch,font=f)
    ctext(d,1400,T["notice"],font("x",64 if LANG=="cs" else 60),OR,n)
    return im
def s4(t):
    im,d=new()
    ctext(d,360,T["instead"],font("x",96),WH,fadein(t,0.2))
    a=fadein(t,K["tell"])
    if a>0:
        d.rounded_rectangle([110,600+_off(a),970,880+_off(a)],radius=40,fill=(63,215,224,int(55*a)),outline=mix(CY,a),width=4)
        lines(d,650,T["prompt"],font("x",66),WH,a)
    b=fadein(t,K["prog"])
    if b>0:
        d.rounded_rectangle([110,980,970,1330],radius=24,fill=(10,12,26,int(235*b)),outline=mix(GR,0.6*b),width=3)
        for k in range(3): d.ellipse([140+k*36,1005,162+k*36,1027],fill=mix([RD,OR,(80,220,120)][k],b))
        f=MONO(44)
        for i,l in enumerate(T["code"]):
            vis=int(len(l)*max(0,min(1,(t-K["prog"]-0.2-i*0.6)/0.6)))
            d.text((150,1080+i*80),l[:vis],font=f,fill=mix([CY,OR][i],b))
    return im
def s5(t):
    im,d=new()
    f=font("x",60 if LANG=="cs" else 64)
    for i,txt in enumerate(T["checks"]):
        a=fadein(t,K["c"][i]); y=560+i*230
        if a<=0: continue
        cx=170; cy=y+42+_off(a)
        d.ellipse([cx-52,cy-52,cx+52,cy+52],fill=(63,215,224,int(60*a)),outline=mix(CY,a),width=5)
        p=ease((t-K["c"][i]-0.1)/0.35)
        if p>0:
            pts=[(cx-24,cy+2),(cx-6,cy+22),(cx+28,cy-20)]
            if p<0.5: q=p/0.5; d.line([pts[0],(pts[0][0]+(pts[1][0]-pts[0][0])*q,pts[0][1]+(pts[1][1]-pts[0][1])*q)],fill=mix(WH,a),width=9)
            else:
                q=(p-0.5)/0.5; d.line([pts[0],pts[1],(pts[1][0]+(pts[2][0]-pts[1][0])*q,pts[1][1]+(pts[2][1]-pts[1][1])*q)],fill=mix(WH,a),width=9,joint="curve")
        d.text((260,y+_off(a)),txt,font=f,fill=mix(WH if i else OR,a))
    return im
def s6(t):
    im,d=new()
    lines(d,380,T["end1"],font("x",92),WH,fadein(t,0.2))
    b=fadein(t,K["build"])
    ctext(d,690,T["end2"],font("x",88 if LANG=="cs" else 80),CY,b)
    nb=int(max(0,min(12,(t-K["build"]-0.1)/0.08)))
    calc_icon(d,540,1190,1.35,fadein(t,K["build"]-0.6),nbtn=nb)
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6]))
if __name__=="__main__":
    main(SCENES,LANG,os.path.dirname(os.path.abspath(__file__)),[(i,D[i]-0.5) for i in range(6)])
