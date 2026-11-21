import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'nastroje'))
from engine import *
from kresby import *
from casy import kotvy
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(HERE,"casovani.json")))[LANG]
AUD={"cs":"hlas-CZ","en":"voice-EN","es":"voz-ES","hi":"awaz-HI","pt":"voz-PT"}
T={"cs":dict(q=["Co když AI","mluví jen","mezi sebou?"],tried="Zkusil jsem to.",roles=["vypravěč","postava","postava","ilustrátor"],
        ideas="Zpočátku plné nápadů.",nonew="Zvenku nic nového.",echo="Jen si přikyvují.",yes=["Přesně!","Souhlasím!","Skvělé!","Přesně tak!"],
        meaning="smysl",empty=["Hodně slov,","žádný obsah."],need=["AI potřebuje","nový vstup zvenku."],inputs=["skutečná data","skutečné otázky"],you="To je tvoje role."),
   "en":dict(q=["What if AIs","only talk","to each other?"],tried="I tried it.",roles=["game master","character","character","illustrator"],
        ideas="Full of ideas at first.",nonew="Nothing new from outside.",echo="They just nod along.",yes=["Exactly!","I agree!","Great!","So true!"],
        meaning="meaning",empty=["Lots of words,","no content."],need=["AI needs","fresh input from outside."],inputs=["real data","real questions"],you="That's your part."),
   "es":dict(q=["¿Y si las IA","hablan solo","entre ellas?"],tried="Lo probé.",roles=["narrador","personaje","personaje","ilustrador"],
        ideas="Al principio, muchas ideas.",nonew="Nada nuevo desde fuera.",echo="Solo se dan la razón.",yes=["¡Exacto!","¡De acuerdo!","¡Genial!","¡Así es!"],
        meaning="sentido",empty=["Muchas palabras,","nada de contenido."],need=["La IA necesita","algo nuevo de fuera."],inputs=["datos reales","preguntas reales"],you="Eso te toca a ti."),
   "hi":dict(q=["जब AI सिर्फ़","आपस में","बात करते हैं?"],tried="मैंने आज़माया।",roles=["सूत्रधार","किरदार","किरदार","चित्रकार"],
        ideas="शुरुआत में ढेरों विचार।",nonew="बाहर से कुछ नया नहीं।",echo="बस हाँ में हाँ।",yes=["बिल्कुल!","सहमत!","शानदार!","सही कहा!"],
        meaning="मतलब",empty=["ढेर सारे शब्द,","कोई मतलब नहीं।"],need=["AI को चाहिए","बाहर से नया इनपुट।"],inputs=["असली डेटा","असली सवाल"],you="यह काम आपका है।"),
   "pt":dict(q=["E se as IAs","conversarem","só entre si?"],tried="Eu testei.",roles=["narrador","personagem","personagem","ilustrador"],
        ideas="No começo, cheio de ideias.",nonew="Nada novo vindo de fora.",echo="Só concordam entre si.",yes=["Exato!","Concordo!","Incrível!","Isso mesmo!"],
        meaning="sentido",empty=["Muitas palavras,","nenhum conteúdo."],need=["A IA precisa","de algo novo de fora."],inputs=["dados reais","perguntas reais"],you="Essa parte é sua.")}[LANG]
A={"cs":dict(ran=(1,"vedl"),chars=(1,"postavy"),drew=(1,"kreslil"),nothing=(2,"nic"),fade=(3,"smysl"),data=(5,"skutečná"),qs=(5,"skutečné"),you=(5,"tvoje")),
   "en":dict(ran=(1,"ran"),chars=(1,"characters"),drew=(1,"drew"),nothing=(2,"nothing"),fade=(3,"meaning"),data=(5,"real"),qs=(5,"real",2),you=(5,"your")),
   "es":dict(ran=(1,"dirigía"),chars=(1,"personajes"),drew=(1,"dibujaba"),nothing=(2,"nada"),fade=(3,"sentido"),data=(5,"datos"),qs=(5,"preguntas"),you=(5,"toca")),
   "hi":dict(ran=(1,"चलाता"),chars=(1,"किरदार"),drew=(1,"तस्वीरें"),nothing=(2,"नया"),fade=(3,"मतलब"),data=(5,"असली"),qs=(5,"असली",2),you=(5,"आपका")),
   "pt":dict(ran=(1,"conduzia"),chars=(1,"personagens"),drew=(1,"desenhava"),nothing=(2,"nada"),fade=(3,"sentido"),data=(5,"dados"),qs=(5,"perguntas"),you=(5,"sua"))}[LANG]
K=kotvy(os.path.join(HERE,"..","zvuk",AUD[LANG]+".casy.json"),A)
D=durations(SEG)
POS=[(300,880),(780,880),(780,1300),(300,1300)]
COLS=[OR,CY,MG,(80,220,120)]
def grey(c,g): m=sum(c)/3; return tuple(int(c[i]*(1-g)+m*g*0.8) for i in range(3))
def ring(d,t,a,g=0.0,eyes=1.0):
    for i,(x,y) in enumerate(POS): bot(d,x,y+math.sin(t*2+i)*8,95,grey(COLS[i],g),a,eyes=eyes,mouth=1)
def hop(d,t,a,g=0.0,period=0.9,text=None,f=None,gcol=None):
    """Bublina, která skáče od bota k botovi po kruhu."""
    k=int(t/period); p=ease((t%period)/period); i,j=k%4,(k+1)%4
    x=POS[i][0]+(POS[j][0]-POS[i][0])*p; y=POS[i][1]+(POS[j][1]-POS[i][1])*p-120-math.sin(p*math.pi)*60
    c=gcol or grey(COLS[i],g)
    w=(d.textlength(text,font=f)+60) if text else 130
    bubble(d,x-w/2,y-55,w,90,c,a,tail=None,fill=70)
    if text: ctext(d,y-38,text,f,WH,a,x=x)
    else:
        for s in range(3): d.ellipse([x-38+s*30,y-12,x-22+s*30,y+4],fill=mix(WH,a))
def s1(t):
    im,d=new()
    lines(d,300,T["q"],fitl(d,T["q"],"x",84),WH,fadein(t,0.1))
    ring(d,t,fadein(t,0.4)); hop(d,t,fadein(t,0.8))
    return im
def s2(t):
    im,d=new()
    ctext(d,300,T["tried"],fit(d,T["tried"],"x",86),WH,fadein(t,0.1))
    ring(d,t,fadein(t,0.2))
    for i,(x,y) in enumerate(POS):
        k=["ran","chars","chars","drew"][i]; a=fadein(t,K[k]-0.2+(0.3 if i==2 else 0))
        ctext(d,y+110,T["roles"][i],fitl(d,T["roles"],"sb",44,330),COLS[i],a,x=x)
    a=fadein(t,K["ran"]-0.2)
    if a>0:   # kostka u vypravěče, štětec u ilustrátora
        d.rounded_rectangle([170,560,240,630],radius=12,fill=mix(WH,a)); [d.ellipse([cx-7,cy-7,cx+7,cy+7],fill=(30,30,40,int(255*a))) for cx,cy in ((190,580),(220,610),(205,595))]
    b=fadein(t,K["drew"]-0.2)
    if b>0: d.line([(400,1370),(460,1300)],fill=mix(OR,b),width=12); d.ellipse([452,1282,476,1306],fill=mix(MG,b))
    return im
def s3(t):
    im,d=new()
    ctext(d,300,T["ideas"],fit(d,T["ideas"],"x",74),CY,fadein(t,0.1))
    ring(d,t,1)
    hop(d,t,1,period=0.7)
    for k in range(10):   # jiskry nápadů
        ph=(t*1.3+k*0.37)%1.0; x=540+math.cos(k*2.4)*(140+ph*260); y=1040+math.sin(k*2.4)*(140+ph*260)
        s=10*(1-ph); d.polygon([(x,y-s*2),(x+s,y),(x,y+s*2),(x-s,y)],fill=mix([OR,CY,MG][k%3],1-ph))
    n=fadein(t,K["nothing"]-0.2)
    if n>0:
        d.line([(40,1040),(170,1040)],fill=mix(GR,n),width=10); d.polygon([(170,1010),(210,1040),(170,1070)],fill=mix(GR,n))
        d.ellipse([60,980,160,1100],outline=mix(RD,n),width=8); d.line([(75,1085),(145,995)],fill=mix(RD,n),width=8)
        ctext(d,1560,T["nonew"],fit(d,T["nonew"],"x",66),OR,n)
    return im
def meter(d,v,a,y=1560):
    d.rounded_rectangle([190,y,890,y+46],radius=23,outline=mix(GR,a),width=4)
    if v>0.02: d.rounded_rectangle([196,y+6,196+688*v,y+40],radius=18,fill=mix(CY if v>0.4 else OR if v>0.15 else RD,a))
    ctext(d,y+60,T["meaning"],fit(d,T["meaning"],"sb",44),GR,a,x=540)
def s4(t):
    im,d=new()
    ctext(d,300,T["echo"],fit(d,T["echo"],"x",80),WH,fadein(t,0.1))
    g=min(1,t/max(1,D[3]-0.5))
    ring(d,t,1,g=g)
    k=int(t/0.8)%len(T["yes"]); hop(d,t,1,g=g,period=0.8,text=T["yes"][k],f=fitl(d,T["yes"],"x",46,400),gcol=grey(CY,g))
    v=1-0.75*ease((t-K["fade"]+0.6)/2.5)
    meter(d,v,fadein(t,0.4))
    return im
def s5(t):
    im,d=new()
    lines(d,300,T["empty"],fitl(d,T["empty"],"x",86),RD,fadein(t,0.1))
    ring(d,t,0.8,g=1,eyes=0.35)
    for k in range(7):   # bubliny plné čmáranic
        ph=(t*0.6+k/7)%1.0; x=540+math.cos(k*0.9+t*0.4)*330; y=1050+math.sin(k*0.9+t*0.4)*300-ph*40
        a=math.sin(ph*math.pi)*0.9
        bubble(d,x-120,y-45,240,90,GR,a,tail=None,fill=40)
        pts=[(x-90+s*12,y+math.sin(s*1.3+k)*18) for s in range(16)]; d.line(pts,fill=mix(WH,0.6*a),width=4)
    meter(d,0.05,1)
    return im
def s6(t):
    im,d=new()
    lines(d,300,T["need"],fitl(d,T["need"],"x",80),WH,fadein(t,0.1))
    rv=ease((t-K["data"]+0.2)/1.5)
    ring(d,t,1,g=1-rv,eyes=0.35+0.65*rv)
    for i,(k,txt) in enumerate(zip(("data","qs"),T["inputs"])):
        p=ease((t-K[k]+0.4)/1.0)
        if p>0:
            x=-200+p*740 if i==0 else 1280-p*740; y=1040+(i*2-1)*60
            c=[OR,CY][i]; fi=fitl(d,T["inputs"],"sb",48,560); w=d.textlength(txt,font=fi)+60
            d.rounded_rectangle([x-w/2,y-40,x+w/2,y+40],radius=40,fill=mix((25,30,55),0.9),outline=mix(c,1),width=4)
            ctext(d,y-28,txt,fi,c,1,x=x)
    ctext(d,1580,T["you"],fit(d,T["you"],"x",76),CY,fadein(t,K["you"]-0.2))
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6]))
if __name__=="__main__":
    main(SCENES,LANG,HERE,[(i,D[i]-0.5) for i in range(6)])
