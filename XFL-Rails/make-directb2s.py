#!/usr/bin/env python3
"""Arma el Rails.directb2s del gabinete: el backglass es RailsInGameBackglass.png (16:9, a
pantalla completa en la pantalla 2) y las luces que quedan se ordenan en el espacio libre de
arriba a la izquierda: el puntaje, GAME OVER, TILT y los números de bola. Las demás luces eran
recortes del arte original (las letras R-A-I-L-S, el cruce, la barrera) y se quitan.

    python make-directb2s.py <Rails.directb2s original> RailsInGameBackglass.png Rails.directb2s preview.png

La vista previa muestra todas las luces encendidas. Requiere Pillow.
"""
import base64, io, sys
import xml.etree.ElementTree as ET
from PIL import Image

SRC, ART, OUT, PREVIEW = sys.argv[1:5]
tree = ET.parse(SRC)
root = tree.getroot()

# Luces que se quedan (las que indican algo) y dónde van en el arte nuevo: x, y, ancho, alto.
BALL_W, BALL_H = 92, 87
KEEP = {
    "25": (40, 225, 352, 104),   # GAME OVER
    "26": (412, 225, 248, 73),   # TILT
}
for i, bid in enumerate(("20", "21", "22", "23", "24")):  # bola 1..5
    KEEP[bid] = (40 + i * 104, 345, BALL_W, BALL_H)
SCORE = (40, 40, 620, 158)

illum = root.find("Illumination")
for b in list(illum):
    if b.get("ID") in KEEP:
        x, y, w, h = KEEP[b.get("ID")]
        b.set("LocX", str(x)); b.set("LocY", str(y)); b.set("Width", str(w)); b.set("Height", str(h))
    else:
        illum.remove(b)
score = root.find("Scores/Score")
for k, v in zip(("LocX", "LocY", "Width", "Height"), SCORE):
    score.set(k, str(v))

art_bytes = open(ART, "rb").read()
art = Image.open(io.BytesIO(art_bytes)).convert("RGB")
root.find("Images/BackglassImage").set("Value", base64.b64encode(art_bytes).decode())
thumb = art.copy(); thumb.thumbnail((100, 75))
buf = io.BytesIO(); thumb.save(buf, "PNG")
root.find("Images/ThumbnailImage").set("Value", base64.b64encode(buf.getvalue()).decode())
tree.write(OUT, encoding="utf-8", xml_declaration=True)

# Vista previa: todas las luces encendidas y el puntaje con el primer rodillo.
prev = art.convert("RGBA")
for b in illum:
    im = Image.open(io.BytesIO(base64.b64decode(b.get("Image")))).convert("RGBA")
    x, y, w, h = (int(b.get(k)) for k in ("LocX", "LocY", "Width", "Height"))
    prev.alpha_composite(im.resize((w, h)), (x, y))
reel = [i for i in root.iter("Image") if i.get("Name") == "EMR_T5_0"][0]
digit = Image.open(io.BytesIO(base64.b64decode(reel.get("Image")))).convert("RGBA")
x, y, w, h = SCORE
dw = w // 6
for i in range(6):
    prev.alpha_composite(digit.resize((dw - 6, h)), (x + i * dw, y))
prev.convert("RGB").save(PREVIEW)
print("luces:", len(illum), "->", OUT)
