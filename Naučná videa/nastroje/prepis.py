"""Offline přepis nahrávky po úsecích mezi pauzami (Whisper base přes sherpa-onnx).
Použití: python3 prepis.py <složka_modelu> nahravka.mp3 cs|en
Model: https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.tar.bz2
Instalace: pip install --break-system-packages sherpa-onnx"""
import sys, subprocess, numpy as np, sherpa_onnx
M=sys.argv[1]; f=sys.argv[2]; lang=sys.argv[3]
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{M}/base-encoder.int8.onnx",decoder=f"{M}/base-decoder.int8.onnx",tokens=f"{M}/base-tokens.txt",language=lang,task="transcribe")
raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
x=np.frombuffer(raw,np.int16).astype(np.float32)/32768
# find pauses >=0.3s below -35 dB
hop=160; env=np.array([np.sqrt(np.mean(x[i:i+hop]**2)) for i in range(0,len(x),hop)])
quiet=20*np.log10(env+1e-9)<-35
segs=[];start=None;run=0;last_end=0
cuts=[]
i=0;n=len(quiet)
while i<n:
    if quiet[i]:
        j=i
        while j<n and quiet[j]: j+=1
        if (j-i)*0.01>=0.3: cuts.append(((i)*0.01,(j)*0.01))
        i=j
    else: i+=1
bounds=[0.0]+[ (a+b)/2 for a,b in cuts]+[len(x)/16000]
for a,b in zip(bounds,bounds[1:]):
    seg=x[int(a*16000):int(b*16000)]
    if np.sqrt(np.mean(seg**2))<0.005: continue
    s=rec.create_stream(); s.accept_waveform(16000,seg); rec.decode_stream(s)
    print(f"{a:6.2f}-{b:6.2f}  {s.result.text.strip()}")
