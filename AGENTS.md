# Instrucciones para agentes: mowak-mods

Mods de mesas de Visual Pinball X para el gabinete de Mowak: nuestro arte, las imágenes originales
de base y la mesa armada (`.vpx` + `.directb2s`). El detalle está en el `README.md`.

Repos relacionados (carpetas hermanas en `D:\Git\Mowak`):

| Repo | Qué es |
|---|---|
| `mowak-launcher` (carpeta `mowak-launcher-native`) | Launcher del gabinete, en C con SDL3. Sus `tools/` arman `.directb2s` e imágenes del menú |
| `mowak-bazzite` | Configuración del gabinete (VPX incluido) |

## Idioma y estilo

- Habla con el usuario en **español de Chile, tuteo neutro, nunca voseo** ("prueba", "dime",
  "fíjate"; nunca "probá", "decime").
- README y mensajes de commit en ese mismo español.

## Git

- Trabaja directo en `main`. No crees ramas si el usuario no lo pide.
- Haz commit y push solo cuando el usuario lo pida.
- **Repo privado.** Las mesas son de XFL, que dio permiso para modificarlas, no para
  redistribuirlas. No publiques estos archivos ni los subas a otro lado.

## Reglas que el usuario pidió

- Nuestras mesas se llaman `<Mesa>.mod.vpx` y las originales `<Mesa>.original.vpx`, para no
  confundirlas. El `.directb2s` lleva el mismo nombre que su mesa, porque VPX lo busca así.
- **Cierra VPX antes de reemplazar una mesa en el gabinete** (`pgrep -x VPinballX_BGFX`); si está
  abierta, corta y no la reemplaces.
- Las pruebas van en el gabinete, nunca en el PC Windows del usuario.

## Cómo se arma

- Con [vpxtool](https://github.com/francisdb/vpxtool) (v0.34.1): `extract`, copiar las imágenes
  con el nombre que tienen dentro del `.vpx`, `assemble`. Compara `audit` de la mesa armada con
  el de la original: tiene que dar lo mismo.
- Las imágenes del mod tienen el **nombre exacto** de la imagen dentro del `.vpx`, incluida la
  mayúscula de la extensión cuando corresponde (`barnstormingplastics.PNG`).
- El `.directb2s` se arma con `tools/restyle-directb2s.py` del repo del launcher y el
  `directb2s-layout.json` de la mesa (Rails tiene su propio `make-directb2s.py`).
- En un `.directb2s`, `LocX`, `LocY`, `Width` y `Height` son píxeles de la imagen del backglass.

## Gabinete

| | |
|---|---|
| Host / usuario | `192.168.31.150`, `mowak_games` |
| SSH desde el PC Windows | `ssh -i ~/.ssh/id_ed25519_bazzite mowak_games@192.168.31.150` |
| Mesas | `~/Pinball/vpx-tables/<mesa>/` |
| VPX | `~/Pinball/vpinball/VPinballX_BGFX` (configuración en el repo `mowak-bazzite`) |
