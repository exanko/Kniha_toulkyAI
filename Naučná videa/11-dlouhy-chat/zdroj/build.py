"""Sestaví jazykové verze dílu: python3 build.py [cs en es hi pt] (bez argumentu všechny; vyžaduje ffmpeg, Pillow, numpy, font Inter)"""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "nastroje"))
from engine import build
SRC = {"cs": "../zvuk/hlas-CZ.mp3", "en": "../zvuk/voice-EN.mp3", "es": "../zvuk/voz-ES.mp3", "hi": "../zvuk/awaz-HI.mp3", "pt": "../zvuk/voz-PT.mp3"}
OUT = {"cs": "../11-proc-ai-v-dlouhem-chatu-chybuje-CZ.mp4",
       "en": "../11-why-ai-slips-in-long-chats-EN.mp4",
       "es": "../11-por-que-la-ia-falla-en-chats-largos-ES.mp4",
       "hi": "../11-lambi-chat-mein-ai-kyon-chookta-hai-HI.mp4",
       "pt": "../11-por-que-a-ia-erra-em-chats-longos-PT.mp4"}
LANGS = sys.argv[1:] or list(SRC)                    # python3 build.py es → jen vybrané jazyky
build(here, json.load(open(os.path.join(here, "casovani.json"))),
      {L: SRC[L] for L in LANGS}, {L: OUT[L] for L in LANGS}, 6)
