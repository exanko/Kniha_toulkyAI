import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'nastroje'))
from engine import *
from kresby import *
from casy import kotvy
LANG=os.environ.get("LANG_V","cs")
SEG=json.load(open(os.path.join(HERE,"casovani.json")))[LANG]
AUD={"cs":"hlas-CZ","en":"voice-EN","es":"voz-ES","hi":"awaz-HI","pt":"voz-PT"}
T={"cs":dict(q=["Normy.","Dlouhé texty, které","nikdo nechce číst?"],before=["Dřív: čím víc norem,","tím víc bolení hlavy."],
        flip="S AI je to naopak.",prompt=["„Udělejme to podle ISO 9001.","A mysli i na zaměstnance.“"],chips=["ISO 9001 · kvalita","ISO 45003 · lidé"],
        numbers="Čísla znát nemusíš.",ask="Které normy se hodí?",list=["ISO 9001 · kvalita","ISO 27001 · bezpečnost dat","ISO 45003 · pohoda lidí"],
        exp=["Norma = zkušenost","tisíců lidí."],free="Rada zdarma.",cert=["Certifikace?","Připravený od začátku."]),
   "en":dict(q=["Standards.","Long documents","nobody wants to read?"],before=["Before: more standards","meant more headaches."],
        flip="With AI, it's the other way round.",prompt=["“Let's do this by ISO 9001.","Keep the employees in mind too.”"],chips=["ISO 9001 · quality","ISO 45003 · people"],
        numbers="No need to know the numbers.",ask="Which standards fit?",list=["ISO 9001 · quality","ISO 27001 · data security","ISO 45003 · wellbeing at work"],
        exp=["A standard = the experience","of thousands of people."],free="Free advice.",cert=["Certification?","Ready from the start."]),
   "es":dict(q=["Normas.","¿Textos largos","que nadie quiere leer?"],before=["Antes: más normas,","más dolores de cabeza."],
        flip="Con la IA es al revés.",prompt=["«Hagámoslo según ISO 9001.","Y piensa en los empleados.»"],chips=["ISO 9001 · calidad","ISO 45003 · personas"],
        numbers="No necesitas saber los números.",ask="¿Qué normas sirven?",list=["ISO 9001 · calidad","ISO 27001 · seguridad de datos","ISO 45003 · bienestar laboral"],
        exp=["Una norma = la experiencia","de miles de personas."],free="Un consejo gratis.",cert=["¿Certificación?","Listo desde el principio."]),
   "hi":dict(q=["मानक।","लंबे दस्तावेज़, जिन्हें","कोई पढ़ना नहीं चाहता?"],before=["पहले: ज़्यादा मानक,","ज़्यादा सिरदर्द।"],
        flip="AI के साथ उल्टा है।",prompt=["\"इसे ISO 9001 के हिसाब से करें।","कर्मचारियों का भी ध्यान रखो।\""],chips=["ISO 9001 · गुणवत्ता","ISO 45003 · लोग"],
        numbers="नंबर जानना ज़रूरी नहीं।",ask="कौन-से मानक सही हैं?",list=["ISO 9001 · गुणवत्ता","ISO 27001 · डेटा सुरक्षा","ISO 45003 · कर्मचारियों की भलाई"],
        exp=["मानक = हज़ारों लोगों","का अनुभव।"],free="मुफ़्त सलाह।",cert=["सर्टिफ़िकेशन?","शुरुआत से तैयार।"]),
   "pt":dict(q=["Normas.","Textos longos que","ninguém quer ler?"],before=["Antes: mais normas,","mais dor de cabeça."],
        flip="Com a IA, é o contrário.",prompt=["“Vamos seguir a ISO 9001.","E pense nos funcionários.”"],chips=["ISO 9001 · qualidade","ISO 45003 · pessoas"],
        numbers="Nem precisa saber os números.",ask="Quais normas servem?",list=["ISO 9001 · qualidade","ISO 27001 · segurança de dados","ISO 45003 · bem-estar no trabalho"],
        exp=["Norma = a experiência","de milhares de pessoas."],free="Conselho grátis.",cert=["Certificação?","Pronto desde o começo."])}[LANG]
# kotevní slova: kdy se co objeví (scéna od 0, začátek slova v namluveném textu)
A={"cs":dict(pain=(1,"bolení"),tell=(2,"řekni"),staff=(2,"zaměstnance"),ask=(3,"zeptat"),free=(4,"rada"),ready=(5,"připraven")),
   "en":dict(pain=(1,"headaches"),tell=(2,"tell"),staff=(2,"employees"),ask=(3,"ask"),free=(4,"free"),ready=(5,"ready")),
   "es":dict(pain=(1,"dolores"),tell=(2,"dile"),staff=(2,"empleados"),ask=(3,"preguntar"),free=(4,"consejo"),ready=(5,"preparado")),
   "hi":dict(pain=(1,"सिरदर्द"),tell=(2,"उससे"),staff=(2,"कर्मचारियों"),ask=(3,"पूछिए"),free=(4,"मुफ़्त"),ready=(5,"तैयार")),
   "pt":dict(pain=(1,"dor"),tell=(2,"diga"),staff=(2,"funcionários"),ask=(3,"perguntar"),free=(4,"conselho"),ready=(5,"preparado"))}[LANG]
K=kotvy(os.path.join(HERE,"..","zvuk",AUD[LANG]+".casy.json"),A)
D=durations(SEG)
LABELS=["ISO 9001","ISO 27001","ISO 45003","ISO 14001","ISO 22301","EN 1090","ISO 31000","ISO 50001"]
def pile(d,n,a,x0=300,y0=1560,w=480,h=110,col=GR):
    """Hromada dokumentů (n kusů, poslední může být rozpracovaný)."""
    for i in reversed(range(int(math.ceil(n)))):   # odshora dolů – štítek každého listu zůstane vidět
        k=min(1,n-i); yy=y0-i*h*0.8-(1-ease(k))*260; xx=x0+((i*37)%5-2)*14
        doc(d,xx,yy-h,w,h,[CY,MG,OR,GR][i%4],a*ease(k),LABELS[i%len(LABELS)],font("sb",34),rot_lines=2)
def s1(t):
    im,d=new()
    ctext(d,330,T["q"][0],font("x",130),CY,fadein(t,0.1))
    lines(d,520,T["q"][1:],fitl(d,T["q"][1:],"x",78),WH,fadein(t,0.6))
    pile(d,min(7,0.8+t*2.4),fadein(t,0.3),y0=1620)
    return im
def s2(t):
    im,d=new()
    lines(d,330,T["before"],fitl(d,T["before"],"x",76),WH,fadein(t,0.2))
    pile(d,min(8,3+t*1.6),1,x0=140,y0=1640,w=420)
    p=fadein(t,K["pain"]-0.3)
    if p>0:
        cx,cy=800,1080; person(d,cx,cy,150,GR,p)
        for k,(dx,dy) in enumerate([(-120,-230),(0,-270),(120,-230)]):
            j=math.sin(t*14+k)*8; x,y=cx+dx,cy+dy
            d.line([(x-20,y+j),(x+6,y-30+j),(x-8,y-30+j),(x+18,y-62+j)],fill=mix(RD,p),width=9)
    return im
def s3(t):
    im,d=new()
    ctext(d,320,T["flip"],fit(d,T["flip"],"x",78),CY,fadein(t,0.1))
    a=fadein(t,K["tell"]-0.2)
    if a>0:
        bubble(d,90,620,900,300,CY,a,tail="l")
        lines(d,690,T["prompt"],fitl(d,T["prompt"],"x",54,820),WH,a)
    for i,c in enumerate(T["chips"]):
        chip(d,540,1080+i*130,c,fit(d,c,"sb",56,860),[CY,MG][i],fadein(t,K["staff"]-0.4+0.35*i))
    return im
def s4(t):
    im,d=new()
    ctext(d,320,T["numbers"],fit(d,T["numbers"],"x",76),WH,fadein(t,0.1))
    a=fadein(t,K["ask"]-0.3)
    if a>0:
        bubble(d,170,560,740,170,MG,a,tail="r"); ctext(d,600,T["ask"],fit(d,T["ask"],"x",60,660),WH,a)
    for i,c in enumerate(T["list"]):
        b=fadein(t,K["ask"]+0.6+0.45*i)
        if b>0:
            y=900+i*170; d.rounded_rectangle([110,y,970,y+130],radius=26,fill=(30,34,60,int(200*b)),outline=mix([CY,OR,MG][i],b),width=4)
            check(d,190,y+65,26,[CY,OR,MG][i],b,10); ctext(d,y+38,c,fitl(d,T["list"],"sb",48,660),WH,b,x=600)
    return im
def s5(t):
    im,d=new()
    lines(d,320,T["exp"],fitl(d,T["exp"],"x",76),WH,fadein(t,0.1))
    cx,cy=540,1080; p=ease(t/2.4)
    import random
    rnd=random.Random(5)
    for k in range(90):
        ang=rnd.uniform(0,2*math.pi); r0=rnd.uniform(330,520); r=r0*(1-p)+60*p
        x,y=cx+r*math.cos(ang+t*0.3),cy+r*math.sin(ang+t*0.3)
        col=[CY,MG,OR,WH][k%4]; d.ellipse([x-9,y-9,x+9,y+9],fill=mix(col,0.9*(1-0.8*p)+0.1))
    g=fadein(t,1.6)
    if g>0:
        doc(d,cx-110,cy-140,220,280,CY,g,"ISO",font("x",44))
        for r in (180,240): d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=mix(CY,0.25*g),width=4)
    ctext(d,1500,T["free"],fit(d,T["free"],"x",92),OR,fadein(t,K["free"]-0.2))
    return im
def s6(t):
    im,d=new()
    lines(d,320,T["cert"],fitl(d,T["cert"],"x",84),WH,fadein(t,0.1))
    a=fadein(t,0.5); p=ease((t-K["ready"]+0.2)/0.8)
    badge(d,540,1020,190,OR,a,p)
    return im
SCENES=list(zip(D,[s1,s2,s3,s4,s5,s6]))
if __name__=="__main__":
    main(SCENES,LANG,HERE,[(i,D[i]-0.5) for i in range(6)])
