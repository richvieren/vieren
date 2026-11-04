"""Instagram Story render for diary photos: photo + per-tag template from story-templates/.

A template folder story-templates/<tag>-<portrait|landscape>/ holds (made from Richard's PSD by
_tools/diary-shortcut/export_story_template.py, never by hand):
  static.png     the full 1080x1920 frame with the photo and the date hidden
  over-<n>.png   PSD layers that sit above the photo slot, applied to the slot only
  template.json  photo window, over layers (offset, blend, opacity) and the date text settings
No template folder for the tag and orientation = no render; the plain photo goes to the Story.
"""
import datetime
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "story-templates"
BLEND = {
    "normal": lambda a, b: b,
    "lighten": ImageChops.lighter,
    "darken": ImageChops.darker,
    "multiply": ImageChops.multiply,
    "screen": ImageChops.screen,
}


def template_for(tag, photo_path):
    with Image.open(photo_path) as im:
        w, h = ImageOps.exif_transpose(im).size
    folder = TEMPLATES / f"{tag}-{'landscape' if w > h else 'portrait'}"
    return folder if (folder / "template.json").exists() else None


def _fit(photo, w, h):
    s = max(w / photo.width, h / photo.height)
    photo = photo.resize((round(photo.width * s), round(photo.height * s)), Image.LANCZOS)
    l, t = (photo.width - w) // 2, (photo.height - h) // 2
    return photo.crop((l, t, l + w, t + h))


def _date(img, d, cfg, folder):
    size = cfg["size"]
    font = ImageFont.truetype(str(folder / cfg["font"]), size)
    text = cfg["format"].format(month=d.strftime("%B"), day=d.day, year=d.year)
    track = size * cfg["tracking"] / 1000
    adv = [font.getlength(c) + track for c in text]
    width = sum(adv) - track
    x = {"left": cfg["x"], "right": cfg["x"] - width}.get(cfg["align"], cfg["x"] - width / 2)
    draw = ImageDraw.Draw(img)
    for c, a in zip(text, adv):  # letter by letter: Pillow has no tracking setting
        draw.text((x, cfg["baseline"]), c, font=font, fill=tuple(cfg["color"]), anchor="ls")
        x += a


def render(folder, photo_path, date_str):
    cfg = json.loads((folder / "template.json").read_text())
    out = Image.open(folder / "static.png").convert("RGB")
    x0, y0, x1, y1 = cfg["window"]
    with Image.open(photo_path) as im:
        slot = _fit(ImageOps.exif_transpose(im).convert("RGB"), x1 - x0, y1 - y0)
    for layer in cfg["over"]:  # bottom to top, as in the PSD
        full = Image.new("RGBA", out.size, (0, 0, 0, 0))
        src = Image.open(folder / layer["file"]).convert("RGBA")
        ox, oy = layer["offset"]
        full.alpha_composite(src, (max(ox, 0), max(oy, 0)), (max(-ox, 0), max(-oy, 0)))
        piece = full.crop((x0, y0, x1, y1))
        mask = piece.getchannel("A")
        if layer["opacity"] < 255:
            mask = mask.point(lambda a: a * layer["opacity"] // 255)
        slot = Image.composite(BLEND[layer["blend"]](slot, piece.convert("RGB")), slot, mask)
    out.paste(slot, (x0, y0))
    if cfg.get("date"):
        _date(out, datetime.date.fromisoformat(date_str), cfg["date"], folder)
    return out
