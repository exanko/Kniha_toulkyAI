"""Sestaví obě jazykové verze dílu: python3 build.py (vyžaduje ffmpeg, Pillow, numpy, font Inter)"""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "nastroje"))
from engine import build
build(here, json.load(open(os.path.join(here, "casovani.json"))),
      {"cs": "../zvuk/hlas-CZ.mp3", "en": "../zvuk/voice-EN.mp3"},
      {"cs": "../05-ai-je-zesilovac-CZ.mp4", "en": "../05-ai-is-an-amplifier-EN.mp4"}, 6)
