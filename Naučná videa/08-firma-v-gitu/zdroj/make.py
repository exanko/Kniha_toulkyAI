import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'nastroje'))
from engine import *
from engine import _off
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"casovani.json")))[LANG]
T={"cs":dict(q=["Jak dostat malou firmu","do doby AI?"],one="Jedno místo pro všechno.",repo="repozitář",truth="Jeden zdroj pravdy.",
        data="Nahraj data.",ask=["Je ti všechno jasné?","Kde vidíš rozpory?"],up="Od základů nahoru.",
        layers=["výpočty","smlouvy","produkty","příběh firmy"],know="Dodávej svoje know-how.",kh="moje know-how",crit="Co si o tom kriticky myslíš?",
        git="Git hlídá každou změnu.",lost="Nic se neztratí.",cust="zákazník",out=["prezentace","leták","kalkulačka"],
        small="malá firma",big="velká firma",robust=["→ robustnější","systém"],careful="Jen pozor:"),
   "en":dict(q=["How do you bring","a small business","into the age of AI?"],one="One place for everything.",repo="repository",truth="A single source of truth.",
        data="Put your data in.",ask=["Is everything clear?","Any contradictions?"],up="From the ground up.",
        layers=["calculations","contracts","products","company story"],know="Keep feeding it your know-how.",kh="my know-how",crit="What do you honestly think?",
        git="Git tracks every change.",lost="Nothing gets lost.",cust="customer",out=["presentation","flyer","calculator"],
        small="small business",big="big company",robust=["→ needs a more","robust system"],careful="Just one catch:")}[LANG]
K={"cs":dict(repo=2.36,truth=3.76,ask=3.94,layer=2.54,lstep=0.6,crit=2.63,lost=2.20,out=[3.80,4.80,5.50],big=1.17,robust=4.13),
   "en":dict(repo=1.59,truth=2.78,ask=6.03,layer=2.60,lstep=0.55,crit=2.42,lost=2.44,out=[3.83,4.83,5.58],big=1.81,robust=5.28)}[LANG]
D=durations(SEG)
def repo_icon(d,cx,cy,s,a):
    if a<=0: return
    w,h=420*s,320*s
    d.rounded_rectangle([cx-w/2,cy-h/2+40*s,cx+w/2,cy+h/2],radius=24*s,fill=(63,215,224,int(45*a)),outline=mix(CY,a),width=5)
    d.rounded_rectangle([cx-w/2,cy-h/2,cx-w/2+170*s,cy-h/2+60*s],radius=16*s,fill=(63,215,224,int(80*a)),outline=mix(CY,a),width=5)
    gx,gy=cx-40*s,cy+30*s
    d.line([(gx,gy-80*s),(gx,gy+80*s)],fill=mix(WH,a),width=int(8*s)); d.line([(gx,gy-20*s),(gx+90*s,gy-70*s)],fill=mix(WH,a),width=int(8*s))
    for (x,y) in [(gx,gy-80*s),(gx,gy+80*s),(gx+90*s,gy-70*s)]: d.ellipse([x-18*s,y-18*s,x+18*s,y+18*s],fill=mix(OR,a))
def doc(d,cx,cy,a,col=WH,s=1.0):
    d.rounded_rectangle([cx-40*s,cy-52*s,cx+40*s,cy+52*s],radius=8,fill=(240,244,250,int(200*a)),outline=mix(col,a),width=3)
    for k in range(3): d.line([(cx-24*s,cy-24*s+k*22*s),(cx+24*s,cy-24*s+k*22*s)],fill=(90,100,130,int(255*a)),width=4)
def s1(t):
    im,d=new()
    for i,l in enumerate(T["q"]): ctext(d,560+i*115,l,font("x",88 if LANG=="cs" else 84),CY if i==len(T["q"])-1 else WH,fadein(t,0.1+0.3*i))
    return im
def s2(t):
    im,d=new()
    ctext(d,340,T["one"],font("x",80 if LANG=="cs" else 74),WH,fadein(t,0.2))
    repo_icon(d,540,920,1.25,fadein(t,K["repo"]-0.4)); ctext(d,1160,T["repo"],font("sb",52),GR,fadein(t,K["repo"]))
    ctext(d,1380,T["truth"],font("x",76 if LANG=="cs" else 70),CY,fadein(t,K["truth"]))
    return im
def s3(t):
    im,d=new()
    ctext(d,340,T["data"],font("x",90),WH,fadein(t,0.2))
    repo_icon(d,540,1020,1.0,fadein(t,0.3))
    for k in range(6):
        st=0.5+k*0.35; p=ease((t-st)/0.8)
        if p<=0 or p>=1: continue
        x=300+k*95; y=520+p*(980-520); doc(d,x,y,1-p*0.6,s=0.8)
    a=fadein(t,K["ask"])
    if a>0:
        d.rounded_rectangle([140,1260+_off(a),940,1500+_off(a)],radius=40,fill=(63,215,224,int(50*a)),outline=mix(CY,a),width=4)
        d.polygon([(780,1260+_off(a)),(840,1260+_off(a)),(820,1210+_off(a))],fill=mix(CY,a))
        lines(d,1290,T["ask"],font("x",62 if LANG=="cs" else 60),WH,a)
    return im
def s4(t):
    im,d=new()
    ctext(d,340,T["up"],font("x",90 if LANG=="cs" else 84),WH,fadein(t,0.2))
    cols=[CY,MG,OR,(80,220,120)]
    for i,w in enumerate(T["layers"]):
        a=fadein(t,K["layer"]-0.9+i*K["lstep"]) if i else fadein(t,K["layer"]-0.9)
        a=fadein(t,max(0.4,K["layer"]-0.6)+i*K["lstep"])
        if a<=0: continue
        bw=880-i*140; y=1420-i*180+_off(a)
        d.rounded_rectangle([540-bw/2,y,540+bw/2,y+150],radius=18,fill=(cols[i][0],cols[i][1],cols[i][2],int(90*a)),outline=mix(cols[i],a),width=4)
        f=font("x",54 if len(w)<12 else 46); ctext(d,y+42-_off(a),w,f,WH,a)
    return im
def s5(t):
    im,d=new()
    ctext(d,340,T["know"],font("x",80 if LANG=="cs" else 66),WH,fadein(t,0.2))
    a=fadein(t,0.6)
    if a>0:
        d.rounded_rectangle([90,700+_off(a),660,880+_off(a)],radius=40,fill=(255,179,71,int(60*a)),outline=mix(OR,a),width=4)
        d.polygon([(150,880+_off(a)),(210,880+_off(a)),(130,940+_off(a))],fill=mix(OR,a))
        ctext(d,755,T["kh"],font("x",58),WH,a,x=375)
    c=fadein(t,K["crit"])
    if c>0:
        d.rounded_rectangle([120,1060+_off(c),990,1300+_off(c)],radius=40,fill=(63,215,224,int(55*c)),outline=mix(CY,c),width=4)
        d.polygon([(860,1300+_off(c)),(920,1300+_off(c)),(940,1360+_off(c))],fill=mix(CY,c))
        lines(d,1115,wrap(d,T["crit"],font("x",60),780),font("x",60),WH,c)
    return im
def s6(t):
    im,d=new()
    ctext(d,340,T["git"],font("x",80 if LANG=="cs" else 76),WH,fadein(t,0.2))
    y=950; xs=[140+i*160 for i in range(6)]
    n=sum(1 for i in range(6) if t>0.5+i*0.25)
    if n: d.line([(xs[0],y),(xs[n-1],y)],fill=mix(WH,0.6),width=6)
    for i in range(n): d.ellipse([xs[i]-26,y-26,xs[i]+26,y+26],fill=mix(OR if i==n-1 else CY,1))
    l=fadein(t,K["lost"])
    if l>0:
        d.arc([xs[2],y-260,xs[5],y+40],200,340,fill=mix(MG,l),width=8)
        ax,ay=xs[2]+18,y-40; d.polygon([(ax-30,ay-10),(ax+10,ay-40),(ax+14,ay+6)],fill=mix(MG,l))
    ctext(d,1200,T["lost"],font("x",82),CY,l)
    return im
def s7(t):
    im,d=new()
    a=fadein(t,0.3)
    if a>0:
        d.ellipse([440,420,640,620],fill=(255,179,71,int(70*a)),outline=mix(OR,a),width=5)
        d.ellipse([505,455,575,525],fill=mix(OR,a)); d.pieslice([470,525,610,665],180,360,fill=mix(OR,a))
        ctext(d,640,T["cust"],font("x",58),OR,a)
    P=[(220,1120),(540,1180),(860,1120)]
    for i,(x,y) in enumerate(P):
        b=fadein(t,K["out"][i]-0.2)
        if b<=0: continue
        d.line([(540,740),(x,y-130)],fill=(255,255,255,int(70*b)),width=4)
        if i==0:
            d.rounded_rectangle([x-120,y-90,x+120,y+70],radius=12,fill=(28,34,64,int(220*b)),outline=mix(CY,b),width=4)
            for k,hh in enumerate([40,80,60,110]): d.rectangle([x-80+k*44,y+40-hh,x-52+k*44,y+40],fill=mix(CY,b))
        elif i==1:
            d.rounded_rectangle([x-80,y-120,x+80,y+100],radius=10,fill=(240,244,250,int(220*b)),outline=mix(MG,b),width=4)
            d.rectangle([x-60,y-100,x+60,y-30],fill=mix(MG,0.8*b))
            for k in range(3): d.line([(x-60,y+k*26),(x+60,y+k*26)],fill=(90,100,130,int(255*b)),width=5)
        else:
            d.rounded_rectangle([x-80,y-115,x+80,y+105],radius=16,fill=(28,34,64,int(220*b)),outline=mix(WH,0.6*b),width=4)
            d.rounded_rectangle([x-60,y-95,x+60,y-50],radius=8,fill=mix(CY,0.5*b))
            for k in range(9):
                r,c=divmod(k,3); d.rounded_rectangle([x-60+c*42,y-35+r*44,x-26+c*42,y-5+r*44],radius=6,fill=mix(OR if c==2 else GR,0.8*b))
        ctext(d,y+130,T["out"][i],font("x",50),WH,b,x=x)
    return im
def s8(t):
    im,d=new()
    ctext(d,330,T["careful"],font("x",92),OR,fadein(t,0.2))
    a=fadein(t,0.5)
    if a>0:
        x=270; d.polygon([(x-110,1000),(x,900),(x+110,1000)],fill=mix(CY,a)); d.rectangle([x-90,1000,x+90,1150],fill=(63,215,224,int(80*a)),outline=mix(CY,a),width=4)
        d.ellipse([x-40,1040,x+40,1120],outline=mix(WH,a),width=6)
        d.line([(x-20,1080),(x-5,1097),(x+24,1062)],fill=mix(WH,a),width=7)
        ctext(d,1180,T["small"],font("x",50),CY,a,x=x)
    b=fadein(t,K["big"])
    if b>0:
        x=780
        d.rectangle([x-150,640,x+150,1150],fill=(28,34,64,int(220*b)),outline=mix(WH,0.6*b),width=4)
        for r in range(7):
            for c in range(4): d.rectangle([x-120+c*64,670+r*66,x-82+c*64,710+r*66],fill=mix(OR if (r+c)%3==0 else GR,0.7*b))
        ctext(d,1180,T["big"],font("x",50),WH,b,x=x)
    lines(d,1380,T["robust"],font("x",72 if LANG=="cs" else 66),OR,fadein(t,K["robust"]))
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6,s7,s8]))
if __name__=="__main__":
    main(SCENES,LANG,os.path.dirname(os.path.abspath(__file__)),[(i,D[i]-0.5) for i in range(8)])
