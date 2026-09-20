# mowak-mods

Mods de mesas de **Visual Pinball X** para el gabinete de pinball de Mowak: el arte que hicimos
nosotros, las imágenes originales de base y la mesa ya armada, lista para copiar al gabinete.

Las mesas originales son de **XFL** (XFL4Ever en VPForums), que nos dio permiso para modificarlas.
Su ficha dice "Permission to MOD?: Yes, without approval". **Este repo es privado**: el permiso es
para modificarlas, no para redistribuirlas.

Repos relacionados (carpetas hermanas en `D:\Git\Mowak`):

| Repo | Qué es |
|---|---|
| `mowak-launcher` (carpeta `mowak-launcher-native`) | El launcher del gabinete. Sus `tools/` arman los `.directb2s` y las imágenes del menú |
| `mowak-bazzite` | Configuración del gabinete, incluida la de Visual Pinball X |

## Qué hay en cada carpeta

Una carpeta por mesa, `XFL-<mesa>/`:

| Archivo | Qué es |
|---|---|
| `<Mesa>.mod.vpx` | La mesa armada, con nuestro arte. Es la que corre en el gabinete |
| `<Mesa>.mod.directb2s` | Su backglass, el de la pantalla 2. **Tiene que llamarse igual que la mesa**: VPX lo busca por el nombre del archivo |
| Imágenes sueltas (`<nombre>.png`) | Nuestro arte. El nombre es el de la imagen **dentro** del `.vpx` que reemplaza |
| `original/` | Las mismas imágenes de la mesa original, de base para editar, y `directb2s-backglass.png`, el backglass original |
| `directb2s-layout.json` | Dónde va cada marcador (puntaje, bolas, TILT…) sobre nuestro backglass |
| `make-directb2s.py` | Solo en Rails: arma su `.directb2s` (el layout quedó escrito en el script) |

## Mesas

| Mesa | Qué le cambiamos |
|---|---|
| `XFL-Rails` | Playfield, plásticos, el fondo de la vista escritorio y el backglass |
| `XFL-Barnstorming` | Playfield y plásticos; el backglass usa el arte del menú |
| `XFL-Route66` | Playfield y plásticos; el backglass usa el arte del menú |

## Cómo se arma una mesa

Se usa [vpxtool](https://github.com/francisdb/vpxtool) (se probó con la v0.34.1). Un `.vpx` es un
archivo compuesto con una firma que VPX revisa, así que no se edita con un zip:

```bash
vpxtool extract Rails.vpx                  # crea la carpeta Rails/ (imágenes en Rails/images/)
cp XFL-Rails/*.png Rails/images/           # nuestras imágenes, con el nombre de las originales
vpxtool assemble Rails Rails.mod.vpx       # vuelve a armar la mesa, con la firma
vpxtool audit Rails.mod.vpx                # compara el resultado con el audit de la original
```

El backglass se arma con las herramientas del repo del launcher:

```bash
python ../mowak-launcher-native/tools/restyle-directb2s.py XFL-Route66/directb2s-layout.json \
    Route66.original.directb2s XFL-Route66/Route66.mod.directb2s preview.png
```

## En el gabinete

Las mesas van en `~/Pinball/vpx-tables/<mesa>/`, cada una con su mod y su original:

```
Rails/Rails.mod.vpx          Rails/Rails.mod.directb2s
Rails/Rails.original.vpx     Rails/Rails.original.directb2s
```

El launcher las abre desde su `games.json` (`-play <mesa>.mod.vpx`). **Cierra VPX antes de
reemplazar una mesa**: si está abierta, queda leyendo basura.

Las cartas y los backglass que se ven en el menú del launcher **no** están acá: van en
`cabinet/images/` del repo del launcher.
