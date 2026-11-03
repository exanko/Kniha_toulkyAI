"""Sestaví hotová videa: vyrenderuje scény (make.py) a přidá hlas podle casovani.json.
Použití:  python3 build.py        (vyžaduje ffmpeg, Pillow, numpy, font Inter)"""
import json, subprocess, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SEG = json.load(open("casovani.json"))           # [začátek, konec] řeči každé scény v nahrávce (s)
SRC = {"cs": "../zvuk/hlas-CZ.mp3", "en": "../zvuk/voice-EN.mp3"}
OUT = {"cs": "../01-jak-mysli-ai-CZ.mp4", "en": "../01-how-ai-thinks-EN.mp4"}
for L in ["cs", "en"]:
    for i in range(6):
        subprocess.run(["python3", "make.py", str(i)], env={**os.environ, "LANG_V": L}, check=True)
    parts = []
    for i, (b, e) in enumerate(SEG[L]):
        v = f"{L}_scene{i}.mp4"
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v]))
        a = f"{L}_a{i}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC[L], "-af",
            f"atrim=start={b-0.03}:end={e+0.08},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e-b+0.06}:d=0.05,adelay=320|320,apad=whole_dur={dur}",
            "-ar", "48000", "-ac", "2", a], check=True)
        parts.append((v, a))
    open(f"{L}_v.txt", "w").write("".join(f"file '{v}'\n" for v, _ in parts))
    open(f"{L}_a.txt", "w").write("".join(f"file '{a}'\n" for _, a in parts))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{L}_v.txt", "-c", "copy", f"{L}_video.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{L}_a.txt", "-c:a", "pcm_s16le", f"{L}_audio.wav"], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{L}_video.mp4", "-i", f"{L}_audio.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT[L]], check=True)
    for f in os.listdir("."):
        if f.startswith(L + "_"): os.remove(f)
    print("hotovo:", OUT[L])
