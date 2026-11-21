"""Sestaví jazykové verze dílu: python3 build.py [cs en es hi] (bez argumentu všechny; vyžaduje ffmpeg, Pillow, numpy, font Inter)"""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "nastroje"))
from engine import build
SRC = {"cs": "../zvuk/hlas-CZ.mp3", "en": "../zvuk/voice-EN.mp3", "es": "../zvuk/voz-ES.mp3", "hi": "../zvuk/awaz-HI.mp3"}
OUT = {"cs": "../05-ai-je-zesilovac-CZ.mp4", "en": "../05-ai-is-an-amplifier-EN.mp4",
       "es": "../05-la-ia-es-un-amplificador-ES.mp4",
       "hi": "../05-ai-ek-amplifier-hai-HI.mp4"}
LANGS = sys.argv[1:] or list(SRC)                    # python3 build.py es → jen vybrané jazyky
build(here, json.load(open(os.path.join(here, "casovani.json"))),
      {L: SRC[L] for L in LANGS}, {L: OUT[L] for L in LANGS}, 6)
