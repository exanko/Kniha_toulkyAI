"""Sdílený engine naučných videí: pozadí, písmo, záře, ukazatel průběhu, render scén."""
import sys, os, subprocess, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/"
def font(w,s): return ImageFont.truetype(F+{"b":"Inter-Bold.otf","x":"Inter-ExtraBold.otf","m":"Inter-Medium.otf","r":"Inter-Regular.otf","sb":"Inter-SemiBold.otf"}[w],s)
CY=(63,215,224); MG=(192,76,255); OR=(255,179,71); WH=(240,244,250); GR=(150,162,186); RD=(255,90,110)
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def fadein(t,s,dur=0.4): return ease((t-s)/dur)
def mix(c,a): return (c[0],c[1],c[2],int(255*max(0,min(1,a))))
def _off(a): return (1-max(0,min(1,a)))*34
def new(): im=Image.new("RGBA",(W,H),(0,0,0,0)); return im,ImageDraw.Draw(im)
def ctext(d,y,txt,f,col,a=1.0,x=None):
    if a<=0: return
    w=d.textlength(txt,font=f); xx=(W-w)/2 if x is None else x-w/2
    d.text((xx,y+_off(a)),txt,font=f,fill=mix(col,a))
def wrap(d,txt,f,maxw):
    words=txt.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def lines(d,y,ls,f,col,a=1,lh=1.18):
    for i,l in enumerate(ls): ctext(d,y+i*f.size*lh,l,f,col,a)
SW,SH=270,480
_yy,_xx=np.mgrid[0:SH,0:SW].astype(np.float32)
NOISE=(np.random.default_rng(7).normal(0,2.2,(H,W,1))).astype(np.float32)
BLOBS=[((20,170,230),0.18,0.16,0.40,0.42,0.07,0.0),((150,40,255),0.85,0.64,0.46,0.42,0.05,1.7),((255,120,40),0.15,0.92,0.36,0.32,0.06,3.1),((0,230,200),0.90,0.10,0.30,0.30,0.08,4.4)]
def bg_at(T):
    img=np.zeros((SH,SW,3),np.float32)+np.array([5,6,18],np.float32)
    for col,cx,cy,r,amp,spd,ph in BLOBS:
        x=(cx+0.12*math.sin(T*spd*2*math.pi/3+ph))*SW; y=(cy+0.08*math.cos(T*spd*2*math.pi/4+ph))*SH
        rr=r*SW*(1+0.08*math.sin(T*0.4+ph))
        img+=(np.exp(-((_xx-x)**2+(_yy-y)**2)/(2*rr*rr))*amp)[...,None]*np.array(col,np.float32)
    img*=(1-0.45*(((_xx/SW-0.5)**2+(_yy/SH-0.5)**2)*2.2))[...,None]
    big=Image.fromarray(np.clip(img,0,255).astype(np.uint8)).resize((W,H),Image.BICUBIC)
    return Image.fromarray(np.clip(np.asarray(big).astype(np.float32)+NOISE,0,255).astype(np.uint8))
FADE=0.3
def frame(SCENES,si,t):
    dur,fn=SCENES[si]; T0=sum(x for x,_ in SCENES[:si]); Tg=T0+t; TOTAL=sum(x for x,_ in SCENES)
    out=bg_at(Tg).convert("RGBA"); ov=fn(t)
    a=min(1,t/FADE,(dur-t)/FADE)
    if si==0: a=min(1,(dur-t)/FADE) if t>FADE else 1
    if a<1: ov.putalpha(ov.getchannel("A").point(lambda v:int(v*max(0,a))))
    gl=ov.resize((W//4,H//4),Image.BILINEAR).filter(ImageFilter.GaussianBlur(9)).resize((W,H),Image.BILINEAR)
    gl.putalpha(gl.getchannel("A").point(lambda v:min(255,int(v*0.75))))
    out.alpha_composite(gl); out.alpha_composite(ov)
    d=ImageDraw.Draw(out); d.rectangle([0,0,W,10],fill=(255,255,255,30)); d.rectangle([0,0,int(W*Tg/TOTAL),10],fill=CY+(255,))
    return out.convert("RGB")
def durations(seg,lead=0.35,tail=0.55,last_tail=1.4):
    return [round(lead+(e-b)+(last_tail if i==len(seg)-1 else tail),2) for i,(b,e) in enumerate(seg)]
def main(SCENES,LANG,outdir,preview_times):
    mode=sys.argv[1]
    if mode=="preview":
        for si,t in preview_times: frame(SCENES,si,t).save(f"{outdir}/prev_{LANG}_{si}.png")
        return
    si=int(mode); dur,_=SCENES[si]; n=int(round(dur*FPS)); tmp=f"{outdir}/{LANG}_scene{si}.tmp.mp4"
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-r",str(FPS),tmp],stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(SCENES,si,i/FPS).tobytes())
    p.stdin.close(); rc=p.wait()
    if rc==0: os.rename(tmp,f"{outdir}/{LANG}_scene{si}.mp4")
    sys.exit(rc)
def build(outdir,seg,src,out,nscenes,make="make.py"):
    """Vyrenderuje scény obou jazyků a přidá hlas: seg[L]=[[začátek,konec],...] řeči v nahrávce."""
    for L in src:
        for i in range(nscenes): subprocess.run(["python3",make,str(i)],cwd=outdir,env={**os.environ,"LANG_V":L},check=True)
        parts=[]
        for i,(b,e) in enumerate(seg[L]):
            v=f"{L}_scene{i}.mp4"
            dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",v],cwd=outdir))
            a=f"{L}_a{i}.wav"
            subprocess.run(["ffmpeg","-y","-v","error","-i",src[L],"-af",f"atrim=start={b-0.03}:end={e+0.08},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e-b+0.06}:d=0.05,adelay=320|320,apad=whole_dur={dur}","-ar","48000","-ac","2",a],cwd=outdir,check=True)
            parts.append((v,a))
        open(f"{outdir}/{L}_v.txt","w").write("".join(f"file '{v}'\n" for v,_ in parts))
        open(f"{outdir}/{L}_a.txt","w").write("".join(f"file '{a}'\n" for _,a in parts))
        subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{L}_v.txt","-c","copy",f"{L}_video.mp4"],cwd=outdir,check=True)
        subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{L}_a.txt","-c:a","pcm_s16le",f"{L}_audio.wav"],cwd=outdir,check=True)
        subprocess.run(["ffmpeg","-y","-v","error","-i",f"{L}_video.mp4","-i",f"{L}_audio.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",out[L]],cwd=outdir,check=True)
        for f in os.listdir(outdir):
            if f.startswith(L+"_"): os.remove(os.path.join(outdir,f))
        print("hotovo:",out[L])
