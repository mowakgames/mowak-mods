# mowak-mods

Visual Pinball X table mods made by **Mowak Games** for our pinball cabinet: our artwork, the
original images we started from, and the rebuilt table, ready to drop into a cabinet.

## Credits and permission

The original tables are by **XFL** (XFL4Ever on VPForums). His release pages state
*"Permission to MOD?: Yes, without approval"*, and these mods are shared under that permission.
All credit for the tables, their rules and their original artwork goes to him:

| Table | Original release |
|---|---|
| Rails | [VPForums](https://www.vpforums.org/index.php?showtopic=54912) |
| Barnstorming | [VPForums](https://www.vpforums.org/index.php?showtopic=53408) |
| Route 66 | [VPForums](https://www.vpforums.org/index.php?showtopic=54117) |

If you are XFL and want any of this taken down, open an issue and it's gone.

## What's in each folder

One folder per table, `XFL-<table>/`:

| File | What it is |
|---|---|
| `<Table>.mod.vpx` | The rebuilt table, with our artwork. This is what runs on the cabinet |
| `<Table>.mod.directb2s` | Its backglass, for the second screen. **It must share the table's file name**: VPX looks it up that way |
| Loose images (`<name>.png`) | Our artwork. Each file is named after the image **inside** the `.vpx` that it replaces |
| `original/` | The same images as shipped in the original table, to use as a starting point, plus `directb2s-backglass.png`, the original backglass |
| `<Table>.mod.backglass.png` | The artwork behind our backglass (Rails uses `RailsInGameBackglass.png`) |
| `directb2s-layout.json` | Where each indicator goes (score reels, ball number, TILT…) over our backglass |
| `make-directb2s.py` | Rails only: builds its `.directb2s` (that table's layout lives in the script) |

## The mods

| Table | What we changed |
|---|---|
| `XFL-Rails` | Playfield, plastics, desktop backdrop and backglass |
| `XFL-Barnstorming` | Playfield and plastics; the backglass uses our menu artwork |
| `XFL-Route66` | Playfield and plastics; the backglass uses our menu artwork |

Our tables are named `<Table>.mod.vpx` and the untouched ones `<Table>.original.vpx`, so there is
no way to mix them up.

## Rebuilding a table

A `.vpx` is a compound file with a signature that VPX checks, so it can't be edited like a zip.
We use [vpxtool](https://github.com/francisdb/vpxtool) (tested with v0.34.1):

```bash
vpxtool extract Rails.vpx                  # creates Rails/ (images under Rails/images/)
cp XFL-Rails/*.png Rails/images/           # our images, named after the originals
vpxtool assemble Rails Rails.mod.vpx       # rebuilds the table, signature included
vpxtool audit Rails.mod.vpx                # compare against the audit of the original table
```

Keep the image names exactly as they are inside the `.vpx`, including an uppercase extension when
that's how the table has it (`barnstormingplastics.PNG`).

The backglass is built with `tools/restyle-directb2s.py` (Python 3 with Pillow):

```bash
python tools/restyle-directb2s.py XFL-Route66/directb2s-layout.json \
    Route66.original.directb2s XFL-Route66/Route66.mod.directb2s preview.png
```

`restyle-directb2s.py` swaps the backglass image and moves the indicators listed in the layout;
anything not in the layout is dropped (that's how the light overlays cut from the original
artwork are removed). In a `.directb2s`, `LocX`, `LocY`, `Width` and `Height` are pixels of the
backglass image.

## Installing on a cabinet

Tables live in `~/Pinball/vpx-tables/<table>/`, each with the mod and the original side by side:

```
Rails/Rails.mod.vpx          Rails/Rails.mod.directb2s
Rails/Rails.original.vpx     Rails/Rails.original.directb2s
```

Our launcher opens them with `VPinballX_BGFX -play <table>.mod.vpx`. **Close VPX before replacing
a table**: swapping the file while it's open leaves the game reading garbage.

The cover art and backglass images shown in the launcher menu are not here: they live in
`cabinet/images/` of the launcher repo.
