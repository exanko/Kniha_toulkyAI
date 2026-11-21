"""Náhled pro YouTube (540 × 960) ze snímku scény dílu postaveného na engine.py.

  python3 nahled.py <složka dílu> <jazyk> <scéna> [čas]

scéna = číslo od 0; čas v sekundách od začátku scény, záporný = od konce (výchozí −0.5).
Příklad: python3 nahled.py ../02-mozek-spojeny-provazkem es 2   → nahled-es.jpg ze 3. scény 0,5 s před koncem."""
import os, sys, importlib.util

def main():
    if len(sys.argv) < 4: sys.exit(__doc__)
    dil, L, si = os.path.abspath(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    t = float(sys.argv[4]) if len(sys.argv) > 4 else -0.5
    zdroj = os.path.join(dil, "zdroj")
    os.environ["LANG_V"] = L; sys.argv = ["make.py", "none"]
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    spec = importlib.util.spec_from_file_location("dil_make", os.path.join(zdroj, "make.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    dur = m.SCENES[si][0]; t = dur + t if t < 0 else t
    from engine import frame
    from PIL import Image
    out = os.path.join(dil, f"nahled-{L}.jpg")
    frame(m.SCENES, si, t).resize((540, 960), Image.LANCZOS).save(out, quality=90)
    print("uloženo:", out, f"(scéna {si}, {t:.2f} s)")

if __name__ == "__main__":
    main()
