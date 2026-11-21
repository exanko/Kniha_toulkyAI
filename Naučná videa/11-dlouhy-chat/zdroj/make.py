import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'nastroje'))
from engine import *
from kresby import *
from casy import kotvy
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(HERE,"casovani.json")))[LANG]
AUD={"cs":"hlas-CZ","en":"voice-EN","es":"voz-ES","hi":"awaz-HI","pt":"voz-PT"}
T={"cs":dict(q=["Proč AI","v dlouhém chatu","začne chybovat?"],all=["Každá zpráva =","celá konverzace znovu."],model="model",
        contra="Protiklady se hromadí.",blue="Chci modrou.",green="Ne, chci zelenou.",which="Co platí?",
        cut=["Nevejde se?","Zkrátí se."],imp="důležité",memory="paměť",newchat="Nový chat",notes="poznámky",
        items=["cíl: web","barva: zelená","termín: pátek"],tip="Důležité věci do krátkých poznámek.",
        end=["Krátký a čistý kontext","je lepší než","dlouhý a zamotaný."]),
   "en":dict(q=["Why does AI","start slipping","in a long chat?"],all=["Every message =","the whole chat again."],model="model",
        contra="Contradictions pile up.",blue="I want blue.",green="No, I want green.",which="Which one counts?",
        cut=["Doesn't fit?","It gets shortened."],imp="important",memory="memory",newchat="New chat",notes="notes",
        items=["goal: website","color: green","deadline: Friday"],tip="Keep key points in short notes.",
        end=["A short, clean context","beats","a long, tangled one."]),
   "es":dict(q=["¿Por qué la IA","se equivoca","en un chat largo?"],all=["Cada mensaje =","toda la conversación otra vez."],model="modelo",
        contra="Se acumulan contradicciones.",blue="Quiero azul.",green="No, quiero verde.",which="¿Cuál vale?",
        cut=["¿No cabe?","Se recorta."],imp="importante",memory="memoria",newchat="Chat nuevo",notes="notas",
        items=["meta: sitio web","color: verde","plazo: viernes"],tip="Lo importante, en notas cortas.",
        end=["Un contexto corto y limpio","es mejor que","uno largo y enredado."]),
   "hi":dict(q=["लंबी चैट में","AI गलतियाँ क्यों","करने लगता है?"],all=["हर मैसेज =","पूरी बातचीत फिर से।"],model="मॉडल",
        contra="विरोधाभास जमा होते हैं।",blue="मुझे नीला चाहिए।",green="नहीं, हरा चाहिए।",which="कौन-सा सही है?",
        cut=["नहीं समाती?","छोटी कर दी जाती है।"],imp="ज़रूरी",memory="याददाश्त",newchat="नई चैट",notes="नोट्स",
        items=["लक्ष्य: वेबसाइट","रंग: हरा","समय: शुक्रवार"],tip="ज़रूरी बातें छोटे नोट्स में।",
        end=["छोटा और साफ़ संदर्भ","बेहतर है","लंबे और उलझे से।"]),
   "pt":dict(q=["Por que a IA","começa a errar","num chat longo?"],all=["Cada mensagem =","a conversa inteira de novo."],model="modelo",
        contra="As contradições se acumulam.",blue="Quero azul.",green="Não, quero verde.",which="Qual vale?",
        cut=["Não cabe?","É encurtada."],imp="importante",memory="memória",newchat="Chat novo",notes="notas",
        items=["meta: site","cor: verde","prazo: sexta"],tip="O importante, em notas curtas.",
        end=["Um contexto curto e limpo","é melhor do que","um longo e embolado."])}[LANG]
A={"cs":dict(whole=(1,"celá"),blue=(2,"modrou"),green=(2,"zelenou"),which=(2,"neví"),cut=(3,"zkrátí"),fall=(3,"vypadnout"),new=(4,"nový"),notes=(4,"poznámk")),
   "en":dict(whole=(1,"whole"),blue=(2,"blue"),green=(2,"green"),which=(2,"doesn't"),cut=(3,"shortened"),fall=(3,"fall"),new=(4,"new"),notes=(4,"notes")),
   "es":dict(whole=(1,"toda"),blue=(2,"azul"),green=(2,"verde"),which=(2,"sabe"),cut=(3,"recorta"),fall=(3,"quedarse"),new=(4,"nuevo"),notes=(4,"notas")),
   "hi":dict(whole=(1,"पूरी"),blue=(2,"नीला"),green=(2,"हरा"),which=(2,"पता"),cut=(3,"छोटा"),fall=(3,"छूट"),new=(4,"नई"),notes=(4,"नोट्स")),
   "pt":dict(whole=(1,"inteira"),blue=(2,"azul"),green=(2,"verde"),which=(2,"sabe"),cut=(3,"encurtada"),fall=(3,"ficar"),new=(4,"novo"),notes=(4,"notas"))}[LANG]
K=kotvy(os.path.join(HERE,"..","zvuk",AUD[LANG]+".casy.json"),A)
D=durations(SEG)
BLUE=(80,140,255); GREEN=(80,220,120)
def msg(d,i,y,a,col=None,w=None):
    """Prázdná zpráva chatu (řádky místo textu), střídavě vlevo a vpravo."""
    left=i%2==0; w=w or (420+(i*97)%220); h=96
    x=90 if left else 990-w; c=col or (GR if left else CY)
    bubble(d,x,y,w,h,c,a,tail="l" if left else "r",fill=45)
    for k in range(2): d.line([(x+30,y+32+k*30),(x+w-40-(k*90),y+32+k*30)],fill=mix(WH,0.45*a),width=6)
def s1(t):
    im,d=new()
    lines(d,300,T["q"],fitl(d,T["q"],"x",84),WH,fadein(t,0.1))
    off=t*150
    for i in range(14):
        y=1780+i*160-off*1.0-(i*160 if False else 0)-i*0
        y=700+((i*150-off)%2100)
        if 640<y<1480: msg(d,i,y,fadein(t,0.3)*min(1,(y-640)/120,(1480-y)/120))
    w=fadein(t,max(0.8,D[0]-1.4))
    if w>0:
        d.polygon([(540,1540),(440,1710),(640,1710)],fill=mix(OR,w)); ctext(d,1590,"!",font("x",90),(20,20,30),w)
    return im
def model_icon(d,cx,cy,r,a,glow=0):
    if a<=0: return
    for k in range(3 if glow>0 else 0): d.ellipse([cx-r-20*(k+1),cy-r-20*(k+1),cx+r+20*(k+1),cy+r+20*(k+1)],outline=mix(CY,0.25*glow*a/(k+1)),width=4)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(30,40,70,int(230*a)),outline=mix(CY,a),width=6)
    for k in range(3): d.arc([cx-r*0.6,cy-r*0.6+k*r*0.35,cx+r*0.6,cy+k*r*0.35],200,340,fill=mix(CY,0.7*a),width=5)
    ctext(d,cy+r+24,T["model"],font("sb",46),CY,a,x=cx)
def s2(t):
    im,d=new()
    lines(d,300,T["all"],fitl(d,T["all"],"x",76),WH,fadein(t,0.1))
    n=min(9,int(t*1.6)+2)
    a=fadein(t,0.3)
    for i in range(n):
        y=1500-i*92; d.rounded_rectangle([110,y,520,y+70],radius=22,fill=(40,44,70,int(220*a)),outline=mix(GR if i%2 else CY,a),width=3)
    pulse=(t*1.1)%1.0 if t>K["whole"]-0.3 else 0
    if pulse>0:
        p=ease(pulse); x=540+p*230; d.line([(540,1300),(x,1300)],fill=mix(CY,1-pulse*0.5),width=10)
        d.polygon([(x,1270),(x+40,1300),(x,1330)],fill=mix(CY,1-pulse*0.5))
        d.rectangle([110,1500-(n-1)*92,520,1570],outline=mix(CY,0.9*(1-pulse)),width=6)
    model_icon(d,860,1300,120,a,glow=1 if pulse>0 else 0)
    return im
def s3(t):
    im,d=new()
    ctext(d,300,T["contra"],fit(d,T["contra"],"x",72),WH,fadein(t,0.1))
    b=fadein(t,K["blue"]-0.2); g=fadein(t,K["green"]-0.2)
    if b>0:
        bubble(d,100,620,700,130,BLUE,b,tail="l",fill=60); ctext(d,655,T["blue"],fit(d,T["blue"],"x",56,620),WH,b,x=450)
        d.ellipse([860,640,940,720],fill=mix(BLUE,b))
    if g>0:
        bubble(d,280,860,700,130,GREEN,g,tail="r",fill=60); ctext(d,895,T["green"],fit(d,T["green"],"x",56,620),WH,g,x=630)
        d.ellipse([150,880,230,960],fill=mix(GREEN,g))
    w=fadein(t,K["which"]-0.2)
    model_icon(d,540,1320,120,fadein(t,0.4))
    if w>0:
        ctext(d,1100,"?",font("x",150),OR,w,x=540+math.sin(t*6)*10); ctext(d,1560,T["which"],fit(d,T["which"],"x",70),OR,w)
    return im
def s4(t):
    im,d=new()
    lines(d,300,T["cut"],fitl(d,T["cut"],"x",80),WH,fadein(t,0.1))
    a=fadein(t,0.3); c=ease((t-K["cut"]+0.3)/1.0)
    fx0,fy0,fx1,fy1=160,700,920,1450
    d.rounded_rectangle([fx0,fy0,fx1,fy1],radius=30,outline=mix(CY,a),width=6)
    ctext(d,fy1+20,T["memory"],font("sb",46),CY,a,x=540)
    n=9; hh=(fy1-fy0-60)/n
    for i in range(n):
        y=fy0+30+i*hh; sq=1-0.55*c if i<5 else 1
        if i<5: y=fy0+30+i*hh*sq
        else: y=fy0+30+5*hh*(1-0.55*c)+(i-5)*hh
        imp=(i==2)
        if imp:
            f=ease((t-K["fall"]+0.2)/1.0)
            if f>0: y=y+f*900;
            col=RD; al=a*(1-0.6*max(0,f-0.6))
        else: col=GR if i%2 else CY; al=a
        hgt=max(18,(hh-16)*(sq if i<5 else 1))
        d.rounded_rectangle([fx0+40,y,fx1-40,y+hgt],radius=14,fill=(40,44,70,int(200*al)),outline=mix(col,al),width=3)
        if imp and hgt>30: ctext(d,y+hgt/2-24,T["imp"],fit(d,T["imp"],"sb",40,640),RD,al,x=540)
    return im
def s5(t):
    im,d=new()
    ctext(d,300,T["newchat"],fit(d,T["newchat"],"x",86),CY,fadein(t,K["new"]-0.3))
    a=fadein(t,0.3)
    d.rounded_rectangle([140,520,940,1460],radius=36,outline=mix(WH,0.7*a),width=5)
    n=fadein(t,K["notes"]-0.3)
    if n>0:
        d.rounded_rectangle([200,580,880,960],radius=22,fill=(255,200,90,int(40*n)),outline=mix(OR,n),width=4)
        ctext(d,600,T["notes"],font("x",50),OR,n,x=540)
        for i,it in enumerate(T["items"]):
            b=fadein(t,K["notes"]+0.25*i); check(d,270,720+i*75,18,OR,b,7); ctext(d,696+i*75,it,fitl(d,T["items"],"sb",44,560),WH,b,x=560)
    msg(d,1,1050,fadein(t,K["notes"]+1.0),w=420); msg(d,0,1200,fadein(t,K["notes"]+1.4),w=520)
    ctext(d,1560,T["tip"],fit(d,T["tip"],"x",58),WH,fadein(t,K["notes"]+0.6))
    return im
def s6(t):
    im,d=new()
    a=fadein(t,0.2); b=fadein(t,0.8)
    for i in range(3): d.rounded_rectangle([140,700+i*90,460,770+i*90],radius=18,fill=(40,60,80,int(220*a)),outline=mix(CY,a),width=4)
    check(d,300,1060,46,CY,a,14)
    if b>0:
        pts=[]; import random; r=random.Random(3)
        for k in range(26): pts.append((640+r.uniform(0,320),660+r.uniform(0,340)))
        d.line(pts,fill=mix(RD,0.8*b),width=6,joint="curve")
    cross(d,800,1060,40,RD,b,14)
    ctext(d,1260,T["end"][0],fitl(d,T["end"],"x",74),CY,fadein(t,0.4))
    ctext(d,1360,T["end"][1],font("m",56),WH,fadein(t,0.9))
    ctext(d,1450,T["end"][2],fitl(d,T["end"],"x",74),RD,fadein(t,1.3))
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6]))
if __name__=="__main__":
    main(SCENES,LANG,HERE,[(i,D[i]-0.5) for i in range(6)])
