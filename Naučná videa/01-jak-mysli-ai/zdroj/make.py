import sys, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/"
def font(w,s): return ImageFont.truetype(F+{"b":"Inter-Bold.otf","x":"Inter-ExtraBold.otf","m":"Inter-Medium.otf","r":"Inter-Regular.otf","sb":"Inter-SemiBold.otf"}[w],s)
BG1=(9,13,28); BG2=(18,26,52)
CY=(63,215,224); MG=(192,76,255); OR=(255,179,71); WH=(240,244,250); GR=(140,152,176)
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
import numpy as np
SW,SH=270,480
_yy,_xx=np.mgrid[0:SH,0:SW].astype(np.float32)
rng=np.random.default_rng(7)
NOISE=(rng.normal(0,2.2,(H,W,1))).astype(np.float32)
BLOBS=[((20,170,230),0.18,0.16,0.40,0.42,0.07,0.0),((150,40,255),0.85,0.64,0.46,0.42,0.05,1.7),((255,120,40),0.15,0.92,0.36,0.32,0.06,3.1),((0,230,200),0.90,0.10,0.30,0.30,0.08,4.4)]
def bg_at(T):
    img=np.zeros((SH,SW,3),np.float32)+np.array([5,6,18],np.float32)
    for col,cx,cy,r,amp,spd,ph in BLOBS:
        x=(cx+0.12*math.sin(T*spd*2*math.pi/3+ph))*SW; y=(cy+0.08*math.cos(T*spd*2*math.pi/4+ph))*SH
        rr=r*SW*(1+0.08*math.sin(T*0.4+ph))
        g=np.exp(-((_xx-x)**2+(_yy-y)**2)/(2*rr*rr))*amp
        img+=g[...,None]*np.array(col,np.float32)
    # vignette
    v=1-0.45*(((_xx/SW-0.5)**2+(_yy/SH-0.5)**2)*2.2)
    img*=v[...,None]
    big=Image.fromarray(np.clip(img,0,255).astype(np.uint8)).resize((W,H),Image.BICUBIC)
    arr=np.asarray(big).astype(np.float32)+NOISE
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
BASE=Image.new("RGB",(W,H),BG1)
def mix(c,a): return (c[0],c[1],c[2],int(255*max(0,min(1,a))))
def _off(a): return (1-max(0,min(1,a)))*34
def ctext(d,y,txt,f,col,a=1.0):
    if a<=0: return
    w=d.textlength(txt,font=f); d.text(((W-w)/2,y+_off(a)),txt,font=f,fill=mix(col,a))
def wrap(d,txt,f,maxw):
    words=txt.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def block(d,y,txt,f,col,a=1,lh=1.2,maxw=900):
    for i,l in enumerate(wrap(d,txt,f,maxw)): ctext(d,y+i*f.size*lh,l,f,col,a)
def brand(d,a=1):
    pass
def fadein(t,s,dur=0.4): return ease((t-s)/dur)


LANG=os.environ.get("LANG_V","cs")
T={
 "cs":dict(q1="Jak vlastně",q2="„myslí“",q3="AI?",n1="Nemyslí.",n2="Hádá další slovo.",type="Napíšeš:",
   pre="Párek v ",word="rohlíku",calc="AI spočítá, co asi přijde dál:",
   cands=[("rohlíku",0.82,CY),("těstě",0.09,MG),("bramborách",0.05,OR),("kostce",0.04,GR)],
   illu="(čísla jsou ilustrační)",pick="→ vybere nejpravděpodobnější",again="A pak znovu. A znovu.",
   sent="Párek v rohlíku je klasika české kuchyně.",wbw1="Slovo po slovu vznikne",wbw2="celá odpověď.",
   t1="Neví, co je pravda.",t2="Ví jen, co obvykle",t3="následuje.",
   e1="Proto umí znít",e2="přesvědčivě,",e3="i když se plete.",e4="Důležité věci",e5="si vždycky ověř."),
 "en":dict(q1="How does",q2="AI",q3="actually think?",n1="It doesn't.",n2="It guesses the next word.",type="You type:",
   pre="Peanut butter and",word="jelly",calc="The AI calculates what comes next:",
   cands=[("jelly",0.82,CY),("banana",0.09,MG),("honey",0.05,OR),("toast",0.04,GR)],
   illu="(illustrative numbers)",pick="→ picks the most likely one",again="Then again. And again.",
   sent="Peanut butter and jelly is a classic sandwich.",wbw1="Word by word,",wbw2="a whole answer appears.",
   t1="It doesn't know what's true.",t2="It only knows what",t3="usually comes next.",
   e1="That's why it can",e2="sound convincing",e3="even when it's wrong.",e4="Always double-check",e5="what matters."),
}[LANG]
# per-language timing: scene durations and key moments (seconds, scene-local)
K={"cs":dict(d=[3.16, 2.77, 8.51, 5.13, 3.95, 6.55], n2=1.2, pick=6.5, calc=2.27, again2=1.4, w0=2.23, t2=1.62, e3=1.9, e4=3.09),
   "en":dict(d=[2.86, 3.22, 9.18, 5.74, 4.73, 7.1], n2=1.29, pick=6.22, calc=2.9, again2=1.34, w0=2.52, t2=2.12, e3=1.36, e4=3.84)}[LANG]
def s1(t):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    if LANG=="cs":
        ctext(d,640,T["q1"],font("b",92),WH,fadein(t,0.1)); ctext(d,760,T["q2"],font("x",170),CY,fadein(t,0.5)); ctext(d,960,T["q3"],font("x",130),WH,fadein(t,0.9))
    else:
        ctext(d,620,T["q1"],font("b",92),WH,fadein(t,0.1)); ctext(d,740,T["q2"],font("x",200),CY,fadein(t,0.5)); ctext(d,980,T["q3"],font("x",104),WH,fadein(t,0.9))
    return im
def s2(t):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    ctext(d,700,T["n1"],font("x",150 if LANG=="cs" else 130),WH,fadein(t,0.3))
    f=font("b",96 if LANG=="cs" else 84)
    ctext(d,900,T["n2"],f,OR,fadein(t,K["n2"]))
    return im
def s3(t):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    ctext(d,280,T["type"],font("m",56),GR,fadein(t,0))
    pick=fadein(t,K["pick"],0.4); pre=T["pre"]
    n=int(min(len(pre),max(0,(t-0.4)/0.07))); shown=pre[:n]
    if LANG=="cs":
        fb=font("x",120); pw=d.textlength(pre,font=fb)
        x0=(W-d.textlength(pre+T["word"],font=fb))/2; y=400
        d.text((x0,y),shown,font=fb,fill=mix(WH,1))
        cx=x0+pw; wy=y
    else:
        fb=font("x",104); ctext(d,380,shown or " ",fb,WH) if False else None
        x0=(W-d.textlength(pre,font=fb))/2; d.text((x0,380),shown,font=fb,fill=mix(WH,1))
        fw=font("x",130); cx=(W-d.textlength(T["word"],font=fw))/2; wy=510; fb=fw
    if t<K["pick"]:
        if int(t*2)%2==0 and n==len(pre): d.rectangle([cx+6,wy+20,cx+16,wy+140],fill=mix(CY,1))
    else: d.text((cx,wy),T["word"],font=fb,fill=mix(CY,pick))
    ctext(d,720,T["calc"],font("m",52),GR,fadein(t,K["calc"]))
    pa=fadein(t,K["calc"]+0.2)
    if pa>0: d.rounded_rectangle([40,820,W-40,1440],radius=36,fill=(255,255,255,int(16*pa)),outline=(255,255,255,int(46*pa)),width=2)
    fl=font("sb",62); fp=font("b",62)
    for i,(w,p,c) in enumerate(T["cands"]):
        st=K["calc"]+0.4+i*0.3; a=fadein(t,st); y=850+i*150; g=ease((t-st)/1.3)
        barw=int(330*p*g/0.82)
        d.text((90,y),w,font=fl,fill=mix(WH,a))
        d.rounded_rectangle([500,y+8,500+max(barw,6),y+72],radius=14,fill=mix(c,a))
        d.text((500+max(barw,6)+24,y+4),f"{int(round(p*100*g))} %",font=fp,fill=mix(c,a))
    ctext(d,1480,T["illu"],font("r",40),GR,fadein(t,K["calc"]+1.5)*0.8)
    if t>K["pick"]: ctext(d,1580,T["pick"],font("sb",52),CY,pick)
    return im
def s4(t):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    a,b=T["again"].split(". ",1); a+="."
    f0=font("b",80); wa=d.textlength(a+" ",font=f0); wb=d.textlength(b,font=f0); x=(W-wa-wb)/2
    d.text((x,420),a,font=f0,fill=mix(WH,fadein(t,0.3))); d.text((x+wa,420),b,font=f0,fill=mix(WH,fadein(t,K["again2"])))
    ws=T["sent"].split(); k=min(len(ws),int(max(0,(t-K["w0"]+0.45)/0.32)))
    f=font("x",96)
    for i,l in enumerate(wrap(d," ".join(ws[:k]) or " ",f,900)): ctext(d,680+i*125,l,f,CY,1)
    ctext(d,1260,T["wbw1"],font("m",60),GR,fadein(t,K["w0"]))
    ctext(d,1340,T["wbw2"],font("m",60),GR,fadein(t,K["w0"]+0.3))
    return im
def s5(t):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    if LANG=="cs":
        f=font("x",96); ctext(d,700,T["t1"],f,WH,fadein(t,0.3))
        ctext(d,880,T["t2"],f,OR,fadein(t,K["t2"])); ctext(d,1000,T["t3"],f,OR,fadein(t,K["t2"]+0.25))
    else:
        f=font("x",88); ctext(d,620,"It doesn't know",f,WH,fadein(t,0.3)); ctext(d,730,"what's true.",f,WH,fadein(t,0.5))
        ctext(d,900,T["t2"],f,OR,fadein(t,K["t2"])); ctext(d,1010,T["t3"],f,OR,fadein(t,K["t2"]+0.25))
    return im
def s6(t):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    ctext(d,560,T["e1"],font("b",84),WH,fadein(t,0.3)); ctext(d,670,T["e2"],font("b",84),WH,fadein(t,0.5))
    ctext(d,800,T["e3"],font("x",96 if LANG=="cs" else 88),MG,fadein(t,K["e3"]))
    ctext(d,1120,T["e4"],font("sb",72),CY,fadein(t,K["e4"])); ctext(d,1210,T["e5"],font("sb",72),CY,fadein(t,K["e4"]+0.2))
    return im
SCENES=list(zip(K["d"],[s1,s2,s3,s4,s5,s6]))
FADE=0.3
TOTAL=sum(x for x,_ in SCENES)
def frame(si,t):
    dur,fn=SCENES[si]; T0=sum(x for x,_ in SCENES[:si]); Tg=T0+t
    out=bg_at(Tg).convert("RGBA"); ov=fn(t)
    a=min(1,t/FADE,(dur-t)/FADE)
    if si==0: a=min(1,(dur-t)/FADE) if t>FADE else 1
    if a<1:
        al=ov.getchannel("A").point(lambda v:int(v*max(0,a))); ov.putalpha(al)
    gl=ov.resize((W//4,H//4),Image.BILINEAR).filter(ImageFilter.GaussianBlur(9)).resize((W,H),Image.BILINEAR)
    ga=gl.getchannel("A").point(lambda v:min(255,int(v*0.75))); gl.putalpha(ga)
    out.alpha_composite(gl); out.alpha_composite(ov)
    d=ImageDraw.Draw(out)
    d.rectangle([0,0,W,10],fill=(255,255,255,30)); d.rectangle([0,0,int(W*Tg/TOTAL),10],fill=CY+(255,))
    return out.convert("RGB")
if __name__=="__main__":
    mode=sys.argv[1]; out=os.path.dirname(os.path.abspath(__file__))
    if mode=="preview":
        for si,t in [(0,2.2),(1,2.2),(2,7.6),(3,4.6),(4,3.3),(5,5.0)]: frame(si,t).save(f"{out}/prev_{LANG}_{si}.png")
    else:
        si=int(mode); dur,_=SCENES[si]; n=int(round(dur*FPS))
        tmp=f"{out}/{LANG}_scene{si}.tmp.mp4"
        p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-r",str(FPS),tmp],stdin=subprocess.PIPE)
        for i in range(n): p.stdin.write(frame(si,i/FPS).tobytes())
        p.stdin.close(); rc=p.wait()
        if rc==0: os.rename(tmp,f"{out}/{LANG}_scene{si}.mp4")
        sys.exit(rc)
