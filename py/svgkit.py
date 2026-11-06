"""Tiny deterministic SVG kit for the figures: Fira Sans metrics via PIL, hard text limits, PNG via resvg."""
from html import escape

from PIL import ImageFont

from objectcore_utils import FONTS

W, H = 1750, 1000
INK, MUTED, RIM = "#1f1f1d", "#55544f", "#d8d6ce"
INSTANCE, REAL, CLASS, TERM, OWL, PROP = "#e2e8f0", "#166534", "#9a3412", "#4c1d95", "#ffffff", "#fbbf24"
RED = "#dc2626"
_fonts = {}


def font(size, weight=400):
    key = (size, weight)
    if key not in _fonts:
        f = FONTS / ("FiraSans-Medium.ttf" if weight >= 500 else "FiraSans-Regular.ttf")
        _fonts[key] = ImageFont.truetype(str(f), size, layout_engine=ImageFont.Layout.BASIC)
    return _fonts[key]


def tw(s, size, weight=400):
    return font(size, weight).getlength(s)


def wrap(s, size, maxw, weight=400, maxlines=3):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, size, weight) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > maxlines or any(tw(l, size, weight) > maxw + 0.5 for l in lines):
        raise ValueError(f"text does not fit ({maxw}px, {maxlines} lines): {s!r}")
    return lines


class Canvas:
    def __init__(self, title):
        self.title = title
        self.items = []

    def add(self, s):
        self.items.append(s)

    def text(self, x, y, s, size=20, weight=400, fill=INK, anchor="start", maxw=None):
        if maxw is not None and tw(s, size, weight) > maxw + 0.5:
            raise ValueError(f"text too wide ({tw(s, size, weight):.0f}>{maxw}): {s!r}")
        self.add(f'<text x="{x:g}" y="{y:g}" font-family="Fira Sans" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')

    def rect(self, x, y, w, h, fill=OWL, stroke="#000000", rx=10, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def box(self, x, y, w, h, title, sub=None, fill=INSTANCE, ink="#000000", tsize=22, ssize=16, lines=None):
        if fill in (REAL, CLASS, TERM):
            ink = "#ffffff"
        self.rect(x, y, w, h, fill)
        tl = wrap(title, tsize, w - 20, 500, 2)
        sl = wrap(sub, ssize, w - 20, 400, 2) if sub else []
        extra = lines or []
        total = len(tl) * (tsize + 4) + len(sl) * (ssize + 3) + len(extra) * (ssize + 3)
        yy = y + (h - total) / 2 + tsize
        for l in tl:
            self.text(x + w / 2, yy, l, tsize, 500, ink, "middle", w - 20)
            yy += tsize + 4
        yy -= 2
        for l in sl:
            self.text(x + w / 2, yy + 2, l, ssize, 400, ink if fill in (REAL, CLASS, TERM) else MUTED, "middle", w - 20)
            yy += ssize + 3
        for l in extra:
            self.text(x + w / 2, yy + 2, l, ssize, 400, ink if fill in (REAL, CLASS, TERM) else MUTED, "middle", w - 20)
            yy += ssize + 3

    def chip(self, x, y, s, size=16, fill=PROP, ink="#000000", pad=9, h=26):
        w = tw(s, size) + 2 * pad
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h}" rx="13" fill="{fill}" stroke="#000000" stroke-width="1"/>')
        self.text(x + pad, y + h - 8, s, size, 400, ink)
        return w

    def arrow(self, x1, y1, x2, y2, color="#000000", sw=2.0):
        self.add(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{color}" stroke-width="{sw}" marker-end="url(#a)"/>')

    def header(self, title, sub):
        self.text(60, 70, title, 36, 500, INK, maxw=W - 120)
        self.text(60, 106, sub, 20, 400, MUTED, maxw=W - 120)

    def note(self, s):
        self.text(60, H - 34, s, 16, 400, MUTED, maxw=W - 120)

    def svg(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                f'<title>{escape(self.title)}</title><rect width="{W}" height="{H}" fill="#ffffff"/>'
                '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
                '<path d="M0,0 L10,5 L0,10 z" fill="#000000"/></marker></defs>')
        return head + "".join(self.items) + "</svg>\n"


def to_png(svg_text):
    import resvg_py
    return bytes(resvg_py.svg_to_bytes(svg_string=svg_text, skip_system_fonts=True,
                                       font_files=[str(FONTS / "FiraSans-Regular.ttf"), str(FONTS / "FiraSans-Medium.ttf")], zoom=1.0))
