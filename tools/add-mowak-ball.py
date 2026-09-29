#!/usr/bin/env python3
"""Give an extracted table (vpxtool extract) our own ball, the one from our vertical mini games.

Adds ball/MowakBall.png (a chrome sphere photo, read as a sphere map) and
ball/MowakBallScratches.png (the scratches that roll with the ball) to the table's images, and
points the table's ball settings at them. Our games also draw a blurred reflection under the ball;
VPX has no image for that and mirrors the ball on the playfield instead, so we just make sure that
reflection is on.

    python tools/add-mowak-ball.py Rails/        # then: vpxtool assemble Rails Rails.mod.vpx
"""
import json
import shutil
import sys
from pathlib import Path

BALL_DIR = Path(__file__).resolve().parent.parent / "ball"
IMAGES = {"MowakBall": "MowakBall.png", "MowakBallScratches": "MowakBallScratches.png"}


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    table = Path(sys.argv[1])

    images_json = table / "images.json"
    images = json.loads(images_json.read_text(encoding="utf-8"))
    names = {image["name"] for image in images}
    for name, file in IMAGES.items():
        shutil.copyfile(BALL_DIR / file, table / "images" / file)
        if name not in names:
            images.append({"name": name, "path": file, "alpha_test_value": 1.0})
    images_json.write_text(json.dumps(images, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    gamedata_json = table / "gamedata.json"
    gamedata = json.loads(gamedata_json.read_text(encoding="utf-8"))
    gamedata["ball_image"] = "MowakBall"
    # The photo is a sphere filling the frame, not an equirectangular environment map.
    gamedata["ball_spherical_mapping"] = True
    gamedata["ball_image_front"] = "MowakBallScratches"
    gamedata["ball_decal_mode"] = False
    # VPX mirrors the ball on the playfield itself; turn it on where the table has it off, with
    # the same strength as our games (REFLECTION_STRENGTH in pinball_ball.gd).
    if not gamedata.get("ball_playfield_reflection_strength"):
        gamedata["ball_playfield_reflection_strength"] = 0.5
    gamedata_json.write_text(json.dumps(gamedata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
