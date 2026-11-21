"""Sestaví jazykové verze dílu: python3 build.py [cs en es hi] (bez argumentu všechny; vyžaduje ffmpeg, Pillow, numpy, font Inter)"""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "nastroje"))
from engine import build
SRC = {"cs": "../zvuk/hlas-CZ.mp3", "en": "../zvuk/voice-EN.mp3", "es": "../zvuk/voz-ES.mp3", "hi": "../zvuk/awaz-HI.mp3"}
OUT = {"cs": "../03-nech-ai-postavit-kalkulacku-CZ.mp4", "en": "../03-have-ai-build-the-calculator-EN.mp4",
       "es": "../03-que-la-ia-te-construya-la-calculadora-ES.mp4",
       "hi": "../03-ai-se-calculator-banwaiye-HI.mp4"}
LANGS = sys.argv[1:] or list(SRC)                    # python3 build.py es → jen vybrané jazyky
build(here, json.load(open(os.path.join(here, "casovani.json"))),
      {L: SRC[L] for L in LANGS}, {L: OUT[L] for L in LANGS}, 6)
