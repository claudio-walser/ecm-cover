#!/usr/bin/env python3
"""Generiert die Laser-Vorlage (SVG, mm) fuer die Filzmatte der ECM-Tassenablage.

Koordinaten: Ursprung = hintere linke Ecke der Edelstahlplatte,
x nach rechts (Breite), y nach vorne (Tiefe). Alle Masse in mm.
Die Werte wurden aus den Fotos in ./bilder per Perspektiv-Entzerrung
(Lochraster als Referenz, Meterstab als Massstab) ermittelt.
"""
from pathlib import Path

# --- Platte (Aussenmass, gemessen) -----------------------------------------
PLATE_W = 242.0          # Breite links-rechts
PLATE_D = 266.0          # Tiefe hinten-vorne

# --- Matte ------------------------------------------------------------------
INSET = 1.0              # Matte ringsum kleiner als Platte (Biegeradius der Kante)
CORNER_R = 3.0           # Eckenradius der Matte

# --- Lochraster der Platte --------------------------------------------------
COLS = 10                # Spalten quer
ROWS = 6                 # Reihen in der Tiefe (nur vordere Hälfte gelocht)
PITCH_X = 19.6           # Lochabstand quer
PITCH_Y = 19.6           # Lochabstand Tiefe
FIRST_ROW_Y = 130.0      # Mitte hinterste Lochreihe ab Hinterkante
X0 = (PLATE_W - (COLS - 1) * PITCH_X) / 2   # symmetrisch (gemessen ~33 mm)
PLATE_HOLE_D = 6.5       # Loch in der Platte (nur Referenz)
FELT_HOLE_D = 8.0        # Loch in der Matte (grösser = Toleranz, nichts wird verdeckt)

# --- Kupferbügel: Beine, die in die Platte gehen ----------------------------
TUBE_D = 6.5             # Rohrdurchmesser
# Schlitze von der Mattenkante bis zum Bein (rundes Ende um die Beinmitte).
# (x, y, Kante, Schlitzbreite)  Kante: 'links' | 'rechts' | 'hinten'
# Breite 8 = Rohr + Spiel; 14 bei Beinen, deren Position nur ±5 mm genau ist.
LEGS = [
    (7.5,            246.0, 'links',  8.0),   # Seitenbügel links, vorderes Bein
    (PLATE_W - 7.5,  246.0, 'rechts', 8.0),   # Seitenbügel rechts, vorderes Bein
    (7.5,             37.0, 'links', 14.0),   # Seitenbügel links, hinteres Bein
    (PLATE_W - 7.5,   37.0, 'rechts', 14.0),  # Seitenbügel rechts, hinteres Bein
    (60.0,             7.0, 'hinten', 14.0),  # Rückbügel, linkes Bein
    (PLATE_W - 60.0,   7.0, 'hinten', 14.0),  # Rückbügel, rechtes Bein
]

CUT = 'fill:none;stroke:#ff0000;stroke-width:0.1'
REF = 'fill:none;stroke:#0060ff;stroke-width:0.2;stroke-dasharray:1,1'
MARGIN = 10.0


def rrect(x, y, w, h, r):
    return (f'M {x+r:.3f},{y:.3f} H {x+w-r:.3f} A {r},{r} 0 0 1 {x+w:.3f},{y+r:.3f} '
            f'V {y+h-r:.3f} A {r},{r} 0 0 1 {x+w-r:.3f},{y+h:.3f} H {x+r:.3f} '
            f'A {r},{r} 0 0 1 {x:.3f},{y+h-r:.3f} V {y+r:.3f} A {r},{r} 0 0 1 {x+r:.3f},{y:.3f} Z')


def outline_with_slots():
    """Mattenkontur im Uhrzeigersinn, Schlitze von aussen direkt eingearbeitet."""
    x0, y0 = INSET, INSET
    x1, y1 = PLATE_W - INSET, PLATE_D - INSET
    R = CORNER_R
    top = sorted((l for l in LEGS if l[2] == 'hinten'), key=lambda l: l[0])
    right = sorted((l for l in LEGS if l[2] == 'rechts'), key=lambda l: l[1])
    left = sorted((l for l in LEGS if l[2] == 'links'), key=lambda l: -l[1])
    d = [f'M {x0+R:.3f},{y0:.3f}']
    for cx, cy, _, w in top:            # Hinterkante, nach rechts
        r = w / 2
        d.append(f'H {cx-r:.3f} V {cy:.3f} A {r},{r} 0 0 0 {cx+r:.3f},{cy:.3f} V {y0:.3f}')
    d.append(f'H {x1-R:.3f} A {R},{R} 0 0 1 {x1:.3f},{y0+R:.3f}')
    for cx, cy, _, w in right:          # rechte Kante, nach vorne
        r = w / 2
        d.append(f'V {cy-r:.3f} H {cx:.3f} A {r},{r} 0 0 0 {cx:.3f},{cy+r:.3f} H {x1:.3f}')
    d.append(f'V {y1-R:.3f} A {R},{R} 0 0 1 {x1-R:.3f},{y1:.3f}')
    d.append(f'H {x0+R:.3f} A {R},{R} 0 0 1 {x0:.3f},{y1-R:.3f}')
    for cx, cy, _, w in left:           # linke Kante, nach hinten
        r = w / 2
        d.append(f'V {cy+r:.3f} H {cx:.3f} A {r},{r} 0 0 0 {cx:.3f},{cy-r:.3f} H {x0:.3f}')
    d.append(f'V {y0+R:.3f} A {R},{R} 0 0 1 {x0+R:.3f},{y0:.3f} Z')
    return ' '.join(d)


def build():
    vb_w, vb_h = PLATE_W + 2 * MARGIN, PLATE_D + 2 * MARGIN
    cut, ref = [], []
    cut.append(f'<path id="matte_aussen" style="{CUT}" d="{outline_with_slots()}"/>')
    for r in range(ROWS):
        for c in range(COLS):
            x, y = X0 + c * PITCH_X, FIRST_ROW_Y + r * PITCH_Y
            cut.append(f'<circle id="loch_r{r}_c{c}" style="{CUT}" cx="{x:.3f}" cy="{y:.3f}" r="{FELT_HOLE_D/2:.3f}"/>')
            ref.append(f'<circle style="{REF}" cx="{x:.3f}" cy="{y:.3f}" r="{PLATE_HOLE_D/2:.3f}"/>')
    for x, y, _, _ in LEGS:
        ref.append(f'<circle style="{REF}" cx="{x:.3f}" cy="{y:.3f}" r="{TUBE_D/2:.3f}"/>')
    ref.append(f'<rect style="{REF}" x="0" y="0" width="{PLATE_W}" height="{PLATE_D}"/>')
    ref.append(f'<text x="{PLATE_W/2}" y="-3" style="font:5px sans-serif;fill:#0060ff;text-anchor:middle">HINTEN</text>')
    ref.append(f'<text x="{PLATE_W/2}" y="{PLATE_D+7}" style="font:5px sans-serif;fill:#0060ff;text-anchor:middle">VORNE (Bruehgruppe)</text>')

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="{vb_w}mm" height="{vb_h}mm" viewBox="{-MARGIN} {-MARGIN} {vb_w} {vb_h}">
  <title>ECM Filzmatte {PLATE_W-2*INSET:.0f}x{PLATE_D-2*INSET:.0f} mm</title>
  <g id="referenz" inkscape:groupmode="layer" inkscape:label="Referenz (nicht schneiden)">
    {chr(10).join('    ' + s for s in ref)}
  </g>
  <g id="schnitt" inkscape:groupmode="layer" inkscape:label="Schnitt">
    {chr(10).join('    ' + s for s in cut)}
  </g>
</svg>
'''


if __name__ == '__main__':
    out = Path(__file__).with_name('filzmatte.svg')
    out.write_text(build())
    print(f'{out}  (Lochfeld X0={X0:.1f} mm, letzte Reihe y={FIRST_ROW_Y+(ROWS-1)*PITCH_Y:.1f} mm)')
