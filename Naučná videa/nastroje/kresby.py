"""Společné kresby pro animované díly (od dílu 10): bubliny, štítky, dokumenty, boti, ozubené kolo, blesk…
Všechno kreslí do kreslicí plochy z engine.new() – texty tedy zvládnou i devanágarí."""
import math
from engine import *

def _fill(col, a, k): return (col[0], col[1], col[2], int(k * max(0, min(1, a))))

def bubble(d, x, y, w, h, col, a, tail="l", fill=55):
    """Řečová bublina s ocáskem vlevo („l“), vpravo („r“) nebo bez něj."""
    if a <= 0: return
    d.rounded_rectangle([x, y, x + w, y + h], radius=30, fill=_fill(col, a, fill), outline=mix(col, a), width=4)
    if tail == "l": d.polygon([(x + 46, y + h - 3), (x + 34, y + h + 36), (x + 92, y + h - 3)], fill=_fill(col, a, fill))
    if tail == "r": d.polygon([(x + w - 46, y + h - 3), (x + w - 34, y + h + 36), (x + w - 92, y + h - 3)], fill=_fill(col, a, fill))

def chip(d, cx, y, txt, f, col, a, pad=26, h=None):
    """Štítek s textem, vystředěný na cx; vrací šířku."""
    if a <= 0: return 0
    w = d.textlength(txt, font=f) + 2 * pad; h = h or int(f.size * 1.7)
    d.rounded_rectangle([cx - w / 2, y, cx + w / 2, y + h], radius=h // 2, fill=_fill(col, a, 45), outline=mix(col, a), width=3)
    ctext(d, y + (h - f.size * 1.2) / 2, txt, f, WH, a, x=cx)
    return w

def doc(d, x, y, w, h, col, a, label=None, f=None, rot_lines=4):
    """Stránka dokumentu s přehnutým rohem a řádky textu."""
    if a <= 0: return
    c = 34
    d.polygon([(x, y), (x + w - c, y), (x + w, y + c), (x + w, y + h), (x, y + h)], fill=(26, 30, 52, int(230 * a)), outline=mix(col, a))
    d.line([(x + w - c, y), (x + w - c, y + c), (x + w, y + c)], fill=mix(col, a), width=3)
    y0 = y + max(h * 0.42, (h * 0.12 + f.size * 1.35) if label else 0)
    for i in range(rot_lines):
        yy = y0 + i * max(12, h * 0.13)
        if yy > y + h - 8: break
        d.line([(x + w * 0.14, yy), (x + w * (0.86 if i % 3 else 0.66), yy)], fill=mix(GR, 0.55 * a), width=5)
    if label: ctext(d, y + h * 0.12, label, f, col, a, x=x + w / 2)

def bot(d, cx, cy, r, col, a, eyes=1.0, mouth=0):
    """Hlava bota: zaoblený čtverec, anténa, oči (eyes 0–1 = otevření)."""
    if a <= 0: return
    d.rounded_rectangle([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], radius=int(r * 0.35), fill=_fill(col, a, 70), outline=mix(col, a), width=5)
    d.line([(cx, cy - r * 0.8), (cx, cy - r * 1.15)], fill=mix(col, a), width=5)
    d.ellipse([cx - 9, cy - r * 1.15 - 9, cx + 9, cy - r * 1.15 + 9], fill=mix(col, a))
    eh = max(3, r * 0.22 * eyes)
    for ex in (-r * 0.38, r * 0.38):
        d.rounded_rectangle([cx + ex - r * 0.13, cy - eh, cx + ex + r * 0.13, cy + eh], radius=6, fill=mix(WH, a))
    if mouth: d.line([(cx - r * 0.3, cy + r * 0.45), (cx + r * 0.3, cy + r * 0.45)], fill=mix(WH, 0.7 * a), width=5)

def person(d, cx, cy, r, col, a):
    """Postava: hlava a ramena."""
    if a <= 0: return
    d.ellipse([cx - r * 0.42, cy - r, cx + r * 0.42, cy - r * 0.16], fill=mix(col, a))
    d.chord([cx - r * 0.8, cy - r * 0.05, cx + r * 0.8, cy + r * 1.5], 180, 360, fill=mix(col, a))

def gear(d, cx, cy, r, col, a, rot=0.0, teeth=9):
    if a <= 0: return
    pts = []
    for i in range(teeth * 4):
        ang = rot + i * math.pi * 2 / (teeth * 4)
        rr = r if (i % 4) in (0, 1) else r * 0.78
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=_fill(col, a, 90), outline=mix(col, a))
    d.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32], fill=(20, 22, 40, int(255 * a)), outline=mix(col, a), width=4)

def bolt(d, cx, cy, s, col, a):
    if a <= 0: return
    p = [(0.1, -1), (-0.55, 0.12), (-0.05, 0.12), (-0.2, 1), (0.55, -0.18), (0.05, -0.18), (0.25, -1)]
    d.polygon([(cx + x * s, cy + y * s) for x, y in p], fill=mix(col, a))

def check(d, cx, cy, s, col, a, w=12):
    if a <= 0: return
    d.line([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.7)], fill=mix(col, a), width=w, joint="curve")

def cross(d, cx, cy, s, col, a, w=12):
    if a <= 0: return
    d.line([(cx - s, cy - s), (cx + s, cy + s)], fill=mix(col, a), width=w); d.line([(cx - s, cy + s), (cx + s, cy - s)], fill=mix(col, a), width=w)

def badge(d, cx, cy, r, col, a, p=1.0):
    """Pečeť certifikátu: kruh se zoubky, stužky a fajfka (p = postup kreslení fajfky)."""
    if a <= 0: return
    for sx in (-1, 1):
        d.polygon([(cx + sx * r * 0.35, cy + r * 0.6), (cx + sx * r * 0.75, cy + r * 1.6), (cx + sx * r * 0.45, cy + r * 1.45),
                   (cx + sx * r * 0.2, cy + r * 1.75), (cx + sx * r * 0.05, cy + r * 0.8)], fill=_fill(col, a, 160))
    pts = [(cx + (r if i % 2 == 0 else r * 0.9) * math.cos(i * math.pi / 16), cy + (r if i % 2 == 0 else r * 0.9) * math.sin(i * math.pi / 16)) for i in range(32)]
    d.polygon(pts, fill=_fill(col, a, 110), outline=mix(col, a))
    d.ellipse([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7], outline=mix(WH, 0.8 * a), width=5)
    if p > 0:
        s = r * 0.38; pts = [(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.7)]
        if p < 0.5: e = pts[0][0] + (pts[1][0] - pts[0][0]) * p * 2, pts[0][1] + (pts[1][1] - pts[0][1]) * p * 2; d.line([pts[0], e], fill=mix(WH, a), width=14)
        else:
            q = (p - 0.5) * 2; e = pts[1][0] + (pts[2][0] - pts[1][0]) * q, pts[1][1] + (pts[2][1] - pts[1][1]) * q
            d.line([pts[0], pts[1], e], fill=mix(WH, a), width=14, joint="curve")

def fit(d, txt, w, s, maxw=980, smin=28):
    """Písmo váhy w, nejvýš velikosti s, aby se text vešel do šířky maxw (pro všechny jazyky)."""
    while s > smin and d.textlength(txt, font=font(w, s)) > maxw: s -= 2
    return font(w, s)

def fitl(d, ls, w, s, maxw=980, smin=28):
    """Totéž pro víc řádků – velikost podle nejdelšího."""
    return min((fit(d, l, w, s, maxw, smin) for l in ls), key=lambda f: f.size)
