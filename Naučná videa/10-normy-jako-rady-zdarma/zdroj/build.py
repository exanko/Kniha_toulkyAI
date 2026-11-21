"""Sestaví jazykové verze dílu: python3 build.py [cs en es hi pt] (bez argumentu všechny; vyžaduje ffmpeg, Pillow, numpy, font Inter)"""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "nastroje"))
from engine import build
SRC = {"cs": "../zvuk/hlas-CZ.mp3", "en": "../zvuk/voice-EN.mp3", "es": "../zvuk/voz-ES.mp3", "hi": "../zvuk/awaz-HI.mp3", "pt": "../zvuk/voz-PT.mp3"}
OUT = {"cs": "../10-normy-jako-rady-zdarma-CZ.mp4",
       "en": "../10-standards-as-free-advice-EN.mp4",
       "es": "../10-normas-como-consejos-gratis-ES.mp4",
       "hi": "../10-maanak-muft-salaah-HI.mp4",
       "pt": "../10-normas-como-conselhos-gratis-PT.mp4"}
LANGS = sys.argv[1:] or list(SRC)                    # python3 build.py es → jen vybrané jazyky
build(here, json.load(open(os.path.join(here, "casovani.json"))),
      {L: SRC[L] for L in LANGS}, {L: OUT[L] for L in LANGS}, 6)
