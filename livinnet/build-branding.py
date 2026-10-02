#!/usr/bin/env python3
"""Genera los assets de branding de NetBox a partir de logo-source.png.

Uso (desde livinnet/):  python3 build-branding.py
Requiere: pip install pillow

Salida en branding/ (los nombres son los que NetBox espera en /static):
  logo_netbox_dark_teal.svg    -> logo para tema CLARO  (colores originales)
  logo_netbox_bright_teal.svg  -> logo para tema OSCURO (azul marino -> blanco)
  netbox.ico                   -> favicon
  netbox_touch-icon-180.png    -> icono Apple
  rest-api.ico                 -> favicon de la API navegable (/api/)
"""
import base64
import io
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
OUT = HERE / "branding"
OUT.mkdir(exist_ok=True)

src = Image.open(HERE / "logo-source.png").convert("RGBA")

# --- recorte al contenido visible + margen pequeño ---------------------------
alpha = src.getchannel("A").point(lambda a: 255 if a > 8 else 0)
bbox = alpha.getbbox()
pad = 6
bbox = (max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
        min(bbox[2] + pad, src.width), min(bbox[3] + pad, src.height))
logo = src.crop(bbox)


def is_navy(r, g, b):
    # azul marino de marca (~#16325A); el naranja tiene R alto
    return r < 110 and b > r


def to_dark_theme(img):
    """Azul marino -> blanco, conservando alpha (y antialiasing). El naranja no se toca."""
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a and is_navy(r, g, b):
                px[x, y] = (255, 255, 255, a)
    return out


def svg_wrap(img):
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    w, h = img.size
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}">'
        f'<image width="{w}" height="{h}" xlink:href="data:image/png;base64,{b64}"/>'
        f"</svg>\n"
    )


(OUT / "logo_netbox_dark_teal.svg").write_text(svg_wrap(logo))
(OUT / "logo_netbox_bright_teal.svg").write_text(svg_wrap(to_dark_theme(logo)))

# --- favicon: la "n" partida (azul/naranja) del logo --------------------------
# Se localiza por columnas dentro del recorte: usamos la "n" del medio (6ª letra).
FAV_BOX = (620, 175, 812, 350)  # coordenadas sobre logo-source.png
glyph = src.crop(FAV_BOX)
gb = glyph.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
glyph = glyph.crop(gb)


def square(img, size, bg=None, margin=0.12):
    canvas = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
    inner = int(size * (1 - 2 * margin))
    scale = min(inner / img.width, inner / img.height)
    g = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.LANCZOS)
    canvas.alpha_composite(g, ((size - g.width) // 2, (size - g.height) // 2))
    return canvas


big = square(glyph, 256)
big.save(OUT / "netbox.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
big.save(OUT / "rest-api.ico", sizes=[(16, 16), (32, 32), (48, 48)])
square(glyph, 180, bg=(255, 255, 255, 255), margin=0.18).convert("RGB").save(
    OUT / "netbox_touch-icon-180.png", optimize=True)
print("OK ->", *sorted(p.name for p in OUT.iterdir()), sep="\n  ")
