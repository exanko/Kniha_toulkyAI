import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'nastroje'))
from engine import *
from kresby import *
from casy import kotvy
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(HERE,"casovani.json")))[LANG]
AUD={"cs":"hlas-CZ","en":"voice-EN","es":"voz-ES","hi":"awaz-HI","pt":"voz-PT"}
T={"cs":dict(two=["Lidé myslí","dvěma způsoby."],fast="rychle",slow="pomalu",fasttxt=["Rychlé myšlení:","hned, ale často vedle."],
        slowtxt="Pomalé myšlení dá práci.",avoid="Většina lidí se mu vyhne.",handoff=["Dřív vyhledávači,","teď celé AI."],search="hledat…",
        blind=["Kdo nemyslí pomalu,","nepozná chybu AI."],work="AI: dřina",judge="ty: úsudek",yours="Pomalé myšlení je tvoje."),
   "en":dict(two=["People think","in two ways."],fast="fast",slow="slow",fasttxt=["Fast thinking:","instant, but often wrong."],
        slowtxt="Slow thinking takes effort.",avoid="Most people avoid it.",handoff=["Once: the search engine.","Now: all of it to AI."],search="search…",
        blind=["Stop thinking slowly,","and you miss AI's mistakes."],work="AI: heavy lifting",judge="you: judgment",yours="Slow thinking is still yours."),
   "es":dict(two=["Las personas piensan","de dos maneras."],fast="rápido",slow="despacio",fasttxt=["Pensamiento rápido:","al instante, pero falla."],
        slowtxt="Pensar despacio cuesta.",avoid="La mayoría lo evita.",handoff=["Antes: al buscador.","Ahora: todo a la IA."],search="buscar…",
        blind=["Si no piensas despacio,","no ves los errores de la IA."],work="IA: trabajo pesado",judge="tú: criterio",yours="Pensar despacio sigue siendo tuyo."),
   "hi":dict(two=["इंसान दो तरह","से सोचते हैं।"],fast="तेज़",slow="धीमे",fasttxt=["तेज़ सोच:","तुरंत, पर अक्सर गलत।"],
        slowtxt="धीमी सोच में मेहनत लगती है।",avoid="ज़्यादातर लोग इससे बचते हैं।",handoff=["पहले: सर्च इंजन।","अब: सब कुछ AI को।"],search="खोजें…",
        blind=["धीमी सोच छोड़ी,","तो AI की गलती नहीं दिखेगी।"],work="AI: मेहनत",judge="आप: फ़ैसला",yours="धीमी सोच अब भी आपकी है।"),
   "pt":dict(two=["As pessoas pensam","de dois jeitos."],fast="rápido",slow="devagar",fasttxt=["Pensamento rápido:","na hora, mas erra."],
        slowtxt="Pensar devagar dá trabalho.",avoid="A maioria evita.",handoff=["Antes: o buscador.","Agora: tudo para a IA."],search="buscar…",
        blind=["Sem pensar devagar,","você não vê os erros da IA."],work="IA: trabalho pesado",judge="você: julgamento",yours="Pensar devagar continua sendo seu.")}[LANG]
A={"cs":dict(fast=(0,"rychle"),slow=(0,"pomalu"),wrong=(1,"splete"),calc=(2,"počítá"),check=(2,"ověřuje"),weigh=(2,"zvažuje"),avoid=(2,"většina"),now=(3,"teď"),notice=(4,"nepozná"),judge=(5,"úsudek"),yours=(5,"pomalé")),
   "en":dict(fast=(0,"fast"),slow=(0,"slow"),wrong=(1,"wrong"),calc=(2,"calculates"),check=(2,"checks"),weigh=(2,"weighs"),avoid=(2,"most"),now=(3,"now"),notice=(4,"notice"),judge=(5,"judgment"),yours=(5,"slow")),
   "es":dict(fast=(0,"rápido"),slow=(0,"despacio"),wrong=(1,"equivoca"),calc=(2,"calcula"),check=(2,"verifica"),weigh=(2,"sopesa"),avoid=(2,"mayoría"),now=(3,"ahora"),notice=(4,"notarás"),judge=(5,"criterio"),yours=(5,"pensamiento")),
   "hi":dict(fast=(0,"तेज़ी"),slow=(0,"धीरे"),wrong=(1,"गलत"),calc=(2,"हिसाब"),check=(2,"जाँचती"),weigh=(2,"तौलती"),avoid=(2,"ज़्यादातर"),now=(3,"अब"),notice=(4,"पता"),judge=(5,"फ़ैसला"),yours=(5,"धीमी")),
   "pt":dict(fast=(0,"rápido"),slow=(0,"devagar"),wrong=(1,"erra"),calc=(2,"calcula"),check=(2,"confere"),weigh=(2,"pondera"),avoid=(2,"maioria"),now=(3,"agora"),notice=(4,"perceber"),judge=(5,"julgamento"),yours=(5,"pensamento"))}[LANG]
K=kotvy(os.path.join(HERE,"..","zvuk",AUD[LANG]+".casy.json"),A)
D=durations(SEG)
AI="IA" if LANG in ("es","pt") else "AI"
def chipai(d,cx,cy,s,a,col=MG):
    if a<=0: return
    d.rounded_rectangle([cx-s,cy-s,cx+s,cy+s],radius=int(s*0.3),fill=(col[0],col[1],col[2],int(70*a)),outline=mix(col,a),width=6)
    for k in (-0.5,0,0.5):
        for sx in (-1,1): d.line([(cx+sx*s,cy+k*s),(cx+sx*s*1.25,cy+k*s)],fill=mix(col,a),width=6)
    ctext(d,cy-s*0.42,AI,font("x",int(s*0.75)),WH,a,x=cx)
def s1(t):
    im,d=new()
    lines(d,330,T["two"],fitl(d,T["two"],"x",84),WH,fadein(t,0.1))
    a=fadein(t,K["fast"]-0.2); b=fadein(t,K["slow"]-0.2)
    bolt(d,320,1020,150,OR,a); ctext(d,1240,T["fast"],fit(d,T["fast"],"x",70,400),OR,a,x=320)
    gear(d,760,1020,140,CY,b,rot=t*0.6); ctext(d,1240,T["slow"],fit(d,T["slow"],"x",70,400),CY,b,x=760)
    return im
def s2(t):
    im,d=new()
    lines(d,330,T["fasttxt"],fitl(d,T["fasttxt"],"x",74),OR,fadein(t,0.1))
    bolt(d,180,830,70,OR,fadein(t,0.2))
    ctext(d,780,"17 × 24 = ?",font("x",110),WH,fadein(t,0.3),x=590)
    g=fadein(t,0.9,0.15); w=fadein(t,K["wrong"]-0.1)
    ctext(d,1000,"≈ 340?",font("x",150),RD if w>0.5 else OR,g)
    cross(d,540,1100,110,RD,w,16)
    return im
def s3(t):
    im,d=new()
    ctext(d,330,T["slowtxt"],fit(d,T["slowtxt"],"x",74),CY,fadein(t,0.1))
    gear(d,540,700,110,CY,fadein(t,0.2),rot=t*0.5)
    st=["17 × 20 = 340","17 × 4 = 68","340 + 68 = 408"]
    for i,(k,s) in enumerate(zip(("calc","check","weigh"),st)):
        a=fadein(t,K[k]-0.2); ctext(d,930+i*120,s,font("x",72),CY if i==2 else WH,a)
    check(d,860,1225,30,CY,fadein(t,K["weigh"]+0.2),10)
    ctext(d,1560,T["avoid"],fit(d,T["avoid"],"x",64),OR,fadein(t,K["avoid"]-0.2))
    return im
def s4(t):
    im,d=new()
    lines(d,330,T["handoff"],fitl(d,T["handoff"],"x",74),WH,fadein(t,0.1))
    a=fadein(t,0.3); n=ease((t-K["now"]+0.2)/1.0)
    person(d,230,1150,170,GR,a)
    gx=230+(780-230)*n; gy=1000+(1050-1000)*n
    gear(d,gx,gy,55+45*n,CY,a,rot=t*0.6)
    d.line([(400,1080),(560,1080)],fill=mix(GR,a),width=8); d.polygon([(560,1055),(600,1080),(560,1105)],fill=mix(GR,a))
    sb=a*(1-n)
    if sb>0:
        d.rounded_rectangle([630,1020,980,1110],radius=45,fill=(255,255,255,int(30*sb)),outline=mix(WH,sb),width=4)
        ctext(d,1040,T["search"],fit(d,T["search"],"m",40,220),GR,sb,x=770)
        d.ellipse([890,1040,930,1080],outline=mix(WH,sb),width=5); d.line([(925,1075),(948,1098)],fill=mix(WH,sb),width=6)
    chipai(d,800,1060,130,n)
    return im
def s5(t):
    im,d=new()
    lines(d,330,T["blind"],fitl(d,T["blind"],"x",72),WH,fadein(t,0.1))
    a=fadein(t,0.3)
    if a>0:
        d.rounded_rectangle([170,620,910,1180],radius=30,fill=(30,34,60,int(200*a)),outline=mix(MG,a),width=4)
        chipai(d,260,700,48,a)
        for i in range(5):
            y=820+i*70; err=(i==2); pulse=0.35+0.25*math.sin(t*3)
            d.line([(240,y),(840-(i%2)*120,y)],fill=mix(RD if err else GR,a*(pulse if err else 0.7)),width=12)
    q=fadein(t,K["notice"]-0.2)
    person(d,840,1450,140,GR,a); ctext(d,1180,"?",font("x",130),OR,q,x=840+math.sin(t*5)*8)
    return im
def s6(t):
    im,d=new()
    a=fadein(t,0.3); j=fadein(t,K["judge"]-0.3)
    chipai(d,300,760,120,a)
    d.line([(420,900),(520,1060)],fill=mix(OR,a),width=12); d.polygon([(500,1040),(560,1030),(560,1110),(520,1120)],fill=mix(OR,a))
    ctext(d,1200,T["work"],fit(d,T["work"],"x",54,440),MG,a,x=300)
    person(d,790,880,150,CY,j)
    if j>0:
        tilt=math.sin(t*1.6)*0.08; cx,cy=790,1080
        d.line([(cx,cy-40),(cx,cy+40)],fill=mix(CY,j),width=8)
        for sx in (-1,1):
            ex,ey=cx+sx*120,cy-40+sx*tilt*120
            d.line([(cx,cy-40),(ex,ey)],fill=mix(CY,j),width=8); d.chord([ex-50,ey,ex+50,ey+60],0,180,fill=mix(CY,j))
    ctext(d,1200,T["judge"],fit(d,T["judge"],"x",54,440),CY,j,x=790)
    ctext(d,1500,T["yours"],fit(d,T["yours"],"x",74),WH,fadein(t,K["yours"]-0.2))
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6]))
if __name__=="__main__":
    main(SCENES,LANG,HERE,[(i,D[i]-0.5) for i in range(6)])
