"""Vypíše úseky řeči v nahrávce (pauzy pod -35 dB, mezery < 0,12 s se slučují).
Použití: python3 intervaly.py nahravka.mp3
Výstup: [index]začátek-konec ... – podle nich a podle přepisu (prepis.py) se skládá casovani.json."""
import sys, subprocess, numpy as np
f = sys.argv[1]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
hop = 160
env = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x), hop)])
loud = 20 * np.log10(env + 1e-9) >= -35
iv = []; i = 0; n = len(loud)
while i < n:
    if loud[i]:
        j = i
        while j < n and loud[j]: j += 1
        iv.append([i * 0.01, j * 0.01]); i = j
    else: i += 1
m = []
for a, b in iv:
    if m and a - m[-1][1] < 0.12: m[-1][1] = b
    else: m.append([a, b])
print(f"délka {len(x)/16000:.2f} s")
print(" ".join(f"[{k}]{a:.2f}-{b:.2f}" for k, (a, b) in enumerate(m)))
