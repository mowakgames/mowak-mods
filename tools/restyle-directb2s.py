#!/usr/bin/env python3
"""Swap the artwork of a .directb2s (the backglass of a VPX table) and move its indicators.

    python tools/restyle-directb2s.py LAYOUT.json ORIGINAL.directb2s OUTPUT.directb2s [PREVIEW.png]

LAYOUT.json (paths are relative to the layout file):
    {
      "art": "backglass.png",                  new image (for example 16:9, 1672x941)
      "bar": {"y": 781, "alpha": 0.8},         optional: dark band from y down to the bottom
      "keep": {                                 what to keep and where, in pixels of the new art:
        "Score 1": [x, y, width, height],       "Score <ID>" or "Bulb <ID>" (ID in the .directb2s)
        "Bulb 2": [x, y, width, height]
      }
    }

Anything not listed in "keep" is dropped, which is how the light overlays cut from the original
artwork are removed. The preview shows every light lit and the reels at 0. Requires Pillow.
"""
import base64
import io
import json
import os
import sys
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    layout_path, source, output = sys.argv[1:4]
    preview_path = sys.argv[4] if len(sys.argv) > 4 else None
    layout = json.load(open(layout_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(layout_path))
    keep = {k: v for k, v in layout["keep"].items()}

    tree = ET.parse(source)
    root = tree.getroot()

    # Artwork, with the dark band if the layout asks for one.
    art = Image.open(os.path.join(base, layout["art"])).convert("RGBA")
    bar = layout.get("bar")
    if bar:
        y0 = int(bar["y"])
        shade = Image.new("RGBA", art.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(shade)
        fade = 40
        for y in range(y0 - fade, art.height):
            a = bar.get("alpha", 0.8) * (min(1.0, (y - (y0 - fade)) / fade))
            d.line([(0, y), (art.width, y)], fill=(0, 0, 0, int(255 * a)))
        art.alpha_composite(shade)
    art = art.convert("RGB")
    buf = io.BytesIO()
    art.save(buf, "PNG")
    root.find("Images/BackglassImage").set("Value", base64.b64encode(buf.getvalue()).decode())
    thumb = art.copy()
    thumb.thumbnail((100, 75))
    buf = io.BytesIO()
    thumb.save(buf, "PNG")
    root.find("Images/ThumbnailImage").set("Value", base64.b64encode(buf.getvalue()).decode())

    # Indicators: the ones in "keep" are moved, the rest are dropped.
    used = set()
    for parent_path, tag in (("Scores", "Score"), ("Illumination", "Bulb")):
        parent = root.find(parent_path)
        if parent is None:
            continue
        for e in list(parent):
            key = "%s %s" % (tag, e.get("ID"))
            if key in keep:
                x, y, w, h = (int(round(v)) for v in keep[key])
                for k, v in zip(("LocX", "LocY", "Width", "Height"), (x, y, w, h)):
                    e.set(k, str(v))
                used.add(key)
            else:
                parent.remove(e)
    missing = set(keep) - used
    if missing:
        sys.exit("not found in the .directb2s: %s" % ", ".join(sorted(missing)))
    tree.write(output, encoding="utf-8", xml_declaration=True)
    print("%s: %d indicators" % (output, len(used)))

    if not preview_path:
        return
    prev = art.convert("RGBA")
    reels = {i.get("Name"): i for i in root.iter("Image") if i.get("Name")}
    for s in root.iter("Score"):
        x, y, w, h = (int(s.get(k)) for k in ("LocX", "LocY", "Width", "Height"))
        n = int(s.get("Digits"))
        img = reels.get(s.get("ReelType"))
        if img is None:
            continue
        digit = Image.open(io.BytesIO(base64.b64decode(img.get("Image")))).convert("RGBA")
        dw = w / n
        for i in range(n):
            prev.alpha_composite(digit.resize((max(1, int(dw) - 4), h)), (int(x + i * dw), y))
    shown = set()
    for b in root.iter("Bulb"):
        x, y, w, h = (int(b.get(k)) for k in ("LocX", "LocY", "Width", "Height"))
        if (x, y) in shown:  # digits stacked in the same spot: show only one
            continue
        shown.add((x, y))
        im = Image.open(io.BytesIO(base64.b64decode(b.get("Image")))).convert("RGBA")
        prev.alpha_composite(im.resize((w, h)), (x, y))
    prev.convert("RGB").save(preview_path)


if __name__ == "__main__":
    main()
