import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'nastroje'))
from engine import *
from engine import _off
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"casovani.json")))[LANG]
T={"cs":dict(q=["Je každá AI","stejně chytrá?"],sizes=["malý","střední","velký"],
        diff=["Modely mají","různou velikost."],grows="A s ní roste, co zvládnou.",
        small="Malý model",onecard="1 herní karta",fast="RYCHLÝ",chat="bla bla bla…",made="Kecálek. Domýšlí si.",
        mid="Střední model",cards="pár karet",code="umí programovat",loop="Víc zkouší a opravuje.",
        big="Největší modely",dc="datové centrum",see="Vidí za roh.",finds=["souvislosti","chyby"],
        exp=["12 AI hodnotilo","stejný text."],smallest="nejmenší",score="9/10",nofind="…a nenašla jedinou chybu.",
        end=["Čím menší model,","tím víc si ověřuj."]),
   "en":dict(q=["Is every AI","equally smart?"],sizes=["small","mid-size","big"],
        diff=["Models come in","different sizes."],grows="What they can handle grows too.",
        small="Small model",onecard="1 gaming card",fast="FAST",chat="blah blah blah…",made="A chatterbox. Makes things up.",
        mid="Mid-size model",cards="a few cards",code="can write code",loop="Tries and fixes more often.",
        big="The biggest models",dc="data center",see="Sees around corners.",finds=["connections","mistakes"],
        exp=["12 AIs reviewed","the same text."],smallest="smallest",score="9/10",nofind="…and found not a single flaw.",
        end=["The smaller the model,","the more you double-check."])}[LANG]
K={"cs":dict(grows=3.0,fast=3.0,made=5.23,tries=3.58,catch=3.39,twelve=1.35,smallest=3.95,nofind=6.09),
   "en":dict(grows=3.37,fast=3.06,made=5.37,tries=4.35,catch=4.56,twelve=1.41,smallest=4.18,nofind=6.67)}[LANG]
D=durations(SEG)
def gpu(d,cx,cy,w,h,a):
    if a<=0: return
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],radius=20,fill=(28,34,64,int(210*a)),outline=mix(WH,0.55*a),width=4)
    r=h*0.30
    for fx in (cx-w*0.22,cx+w*0.22):
        d.ellipse([fx-r,cy-r,fx+r,cy+r],outline=mix(GR,0.8*a),width=4); d.ellipse([fx-r*.25,cy-r*.25,fx+r*.25,cy+r*.25],fill=mix(GR,0.7*a))
    d.rectangle([cx-w*0.32,cy+h/2,cx+w*0.32,cy+h/2+12],fill=mix(OR,0.8*a))
def rack(d,x,y0,y1,w,a,glow=0):
    if a<=0: return
    d.rounded_rectangle([x-w/2,y0,x+w/2,y1],radius=18,fill=(28,34,64,int(210*a)),outline=mix(CY if glow else WH,(0.5+0.5*glow)*a),width=4)
    n=int((y1-y0-30)//60)
    for k in range(n):
        yy=y0+20+k*60; d.rounded_rectangle([x-w/2+20,yy,x+w/2-20,yy+40],radius=8,outline=mix(GR,0.6*a),width=2)
        for j in range(3): d.ellipse([x+w/2-90+j*22,yy+14,x+w/2-78+j*22,yy+26],fill=mix(CY if (k+j)%2 else OR,a))
def orb(d,cx,cy,r,col,a,label=None,lf=None):
    if a<=0: return
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(col[0],col[1],col[2],int(70*a)),outline=mix(col,a),width=5)
    if label: ctext(d,cy+r+24,label,lf or font("sb",46),col,a,x=cx)
def check(d,cx,cy,a,col=CY,k=1.0):
    d.line([(cx-18*k,cy+2*k),(cx-4*k,cy+16*k),(cx+22*k,cy-14*k)],fill=mix(col,a),width=int(8*k),joint="curve")
def s1(t):
    im,d=new()
    lines(d,520,T["q"],font("x",110),WH,fadein(t,0.1))
    for i,(x,r,c) in enumerate([(250,50,OR),(520,90,MG),(830,140,CY)]): orb(d,x,1180,r,c,fadein(t,0.5+0.2*i))
    return im
def s2(t):
    im,d=new()
    lines(d,360,T["diff"],font("x",96),WH,fadein(t,0.2))
    for i,(x,r,c) in enumerate([(220,60,OR),(510,110,MG),(830,165,CY)]):
        orb(d,x,1100,r,c,fadein(t,0.6+0.35*i),T["sizes"][i])
    g=fadein(t,K["grows"])
    if g>0:
        d.line([(170,1420),(900,1420)],fill=mix(WH,0.5*g),width=4); d.polygon([(900,1400),(940,1420),(900,1440)],fill=mix(WH,0.5*g))
    ctext(d,1480,T["grows"],font("x",64 if LANG=="cs" else 60),OR,g)
    return im
def s3(t):
    im,d=new()
    ctext(d,360,T["small"],font("x",100),OR,fadein(t,0.2))
    gpu(d,540,820,460,250,fadein(t,0.5)); ctext(d,980,T["onecard"],font("sb",48),GR,fadein(t,0.6))
    f=fadein(t,K["fast"])
    if f>0:
        d.rounded_rectangle([380,1080,700,1170],radius=45,fill=(63,215,224,int(70*f)),outline=mix(CY,f),width=4)
        ctext(d,1093,T["fast"],font("x",56),CY,f)
    m=fadein(t,K["made"]-0.6)
    if m>0:
        d.rounded_rectangle([200,1240,880,1380],radius=50,fill=(255,179,71,int(50*m)),outline=mix(OR,m),width=4)
        d.polygon([(300,1380),(340,1380),(280,1430)],fill=mix(OR,m))
        ctext(d,1272,T["chat"],font("x",60),WH,m)
    ctext(d,1500,T["made"],font("x",62 if LANG=="cs" else 54),OR,fadein(t,K["made"]))
    return im
def s4(t):
    im,d=new()
    ctext(d,360,T["mid"],font("x",100),MG,fadein(t,0.2))
    for i in range(3): gpu(d,220+i*320,760,280,160,fadein(t,0.4+0.15*i))
    ctext(d,880,T["cards"],font("sb",48),GR,fadein(t,0.6))
    a=fadein(t,1.0)
    if a>0:
        d.rounded_rectangle([140,980,940,1240],radius=24,fill=(10,12,26,int(235*a)),outline=mix(GR,0.6*a),width=3)
        for k in range(3): d.ellipse([170+k*36,1005,192+k*36,1027],fill=mix([RD,OR,(80,220,120)][k],a))
        ctext(d,1080,T["code"],font("sb",56),CY,a)
    l=fadein(t,K["tries"])
    if l>0:
        cx,cy,r=540,1380,60; ang=(t*240)%360
        d.arc([cx-r,cy-r,cx+r,cy+r],ang,ang+290,fill=mix(OR,l),width=10)
        ex=cx+r*math.cos(math.radians(ang+290)); ey=cy+r*math.sin(math.radians(ang+290))
        d.ellipse([ex-14,ey-14,ex+14,ey+14],fill=mix(OR,l))
    ctext(d,1500,T["loop"],font("x",62 if LANG=="cs" else 58),OR,l)
    return im
def s5(t):
    im,d=new()
    ctext(d,340,T["big"],font("x",96 if LANG=="cs" else 88),CY,fadein(t,0.2))
    rack(d,540,560,1130,360,fadein(t,0.4),glow=fadein(t,1.2))
    ctext(d,1160,T["dc"],font("sb",48),GR,fadein(t,0.6))
    ctext(d,1260,T["see"],font("x",76),WH,fadein(t,1.0))
    c=fadein(t,K["catch"])
    for i,w in enumerate(T["finds"]):
        a=fadein(t,K["catch"]+0.3*i); y=1400+i*110+_off(a)
        if a>0:
            d.ellipse([300-34,y-34,300+34,y+34],fill=(63,215,224,int(60*a)),outline=mix(CY,a),width=4)
            check(d,300,y,a); d.text((360,y-34),w,font=font("x",58),fill=mix(WH,a))
    return im
def s6(t):
    im,d=new()
    lines(d,330,T["exp"],font("x",90),WH,fadein(t,0.2))
    tw=fadein(t,K["twelve"]-0.3)
    xs=[100+i*80 for i in range(12)]
    for i,x in enumerate(xs):
        a=fadein(t,K["twelve"]-0.3+i*0.06); r=14+i*2.6
        hl=fadein(t,K["smallest"]) if i==0 else 0
        col=OR if i==0 else (MG if i<6 else CY)
        if a>0: d.ellipse([x-r,900-r,x+r,900+r],fill=(col[0],col[1],col[2],int(80*a)),outline=mix(col,a),width=3)
    s=fadein(t,K["smallest"])
    if s>0:
        d.line([(100,940),(100,1040)],fill=mix(OR,s),width=4)
        d.rounded_rectangle([60,1040+_off(s),460,1260+_off(s)],radius=30,fill=(255,179,71,int(45*s)),outline=mix(OR,s),width=4)
        d.text((90,1060+_off(s)),T["smallest"],font=font("sb",48),fill=mix(OR,s))
        d.text((90,1120+_off(s)),T["score"],font=font("x",110),fill=mix(WH,s))
        for k in range(5):
            cx=520+k*95; cy=1150
            pts=[(cx+40*math.cos(math.radians(-90+j*36))*(1 if j%2==0 else 0.45),cy+40*math.sin(math.radians(-90+j*36))*(1 if j%2==0 else 0.45)) for j in range(10)]
            d.polygon(pts,fill=mix(OR,s*(1 if k<4 else 0.5)))
    ctext(d,1440,T["nofind"],font("x",60 if LANG=="cs" else 56),RD,fadein(t,K["nofind"]))
    return im
def s7(t):
    im,d=new()
    lines(d,640,T["end"],font("x",90 if LANG=="cs" else 70),WH,fadein(t,0.2))
    a=fadein(t,1.0)
    if a>0:
        cx,cy=540,1200
        d.ellipse([cx-110,cy-110,cx+110,cy+110],outline=mix(CY,a),width=14)
        d.line([(cx+78,cy+78),(cx+170,cy+170)],fill=mix(CY,a),width=26)
        check(d,cx,cy,a,WH,k=3.0)
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6,s7]))
if __name__=="__main__":
    main(SCENES,LANG,os.path.dirname(os.path.abspath(__file__)),[(i,D[i]-0.5) for i in range(7)])
