# Agent instructions: mowak-mods

Visual Pinball X table mods by Mowak Games for our pinball cabinet: our artwork, the original
images we started from, and the rebuilt tables (`.vpx` + `.directb2s`). See `README.md` for the
details.

Related repos (sibling folders in `D:\Git\Mowak`):

| Repo | What it is |
|---|---|
| `mowak-launcher` (local folder `mowak-launcher-native`) | The cabinet launcher, C with SDL3. Its `tools/` build the `.directb2s` files and the menu images |
| `mowak-bazzite` | Cabinet configuration, including Visual Pinball X |

## Language

- **Everything in this repo is in English**: README, these instructions, commit messages, code and
  comments. The repo is public and the Visual Pinball community reads it.
- Talk to the user in **Chilean Spanish**, informal "tú", never "voseo" ("prueba", "dime",
  "fíjate"; never "probá", "decime").

## Git

- Work straight on `main`. Don't create branches unless the user asks.
- Commit and push only when the user asks.
- **Commits are authored by the repo's git user and nobody else.** No co-author trailers, no
  "generated with" lines, no mention of any AI tool, in the message or anywhere else.
- Public repo. The tables are XFL's, shared under his "Permission to MOD: Yes, without approval".
  Keep the credits in the README, and credit him in anything new.

## Rules the user asked for

- Our tables are named `<Table>.mod.vpx`, the untouched ones `<Table>.original.vpx`. The
  `.directb2s` shares its table's file name, because that's how VPX looks it up.
- **Close VPX before replacing a table on the cabinet** (`pgrep -x VPinballX_BGFX`). If it's
  running, stop and don't replace anything.
- Test on the cabinet, never on the user's Windows PC.

## How a table is rebuilt

- With [vpxtool](https://github.com/francisdb/vpxtool) (v0.34.1): `extract`, copy the images using
  the name they have inside the `.vpx`, then `assemble`. Compare the `audit` of the rebuilt table
  against the original one: they must match.
- Mod images use the **exact** name of the image inside the `.vpx`, including an uppercase
  extension where the table has one (`barnstormingplastics.PNG`).
- The `.directb2s` is built with `tools/restyle-directb2s.py` from the launcher repo plus the
  table's `directb2s-layout.json` (Rails has its own `make-directb2s.py`).
- In a `.directb2s`, `LocX`, `LocY`, `Width` and `Height` are pixels of the backglass image.

## Cabinet

| | |
|---|---|
| Host / user | `192.168.31.150`, `mowak_games` |
| SSH from the Windows PC | `ssh -i ~/.ssh/id_ed25519_bazzite mowak_games@192.168.31.150` |
| Tables | `~/Pinball/vpx-tables/<table>/` |
| VPX | `~/Pinball/vpinball/VPinballX_BGFX` (configured in the `mowak-bazzite` repo) |
