from base2 import *
import random

PAPER = hx('FFF7E6'); SKY = hx('9FDCF5'); SKY2 = hx('E9F8FF'); GRASS = hx('7CC576'); GRASSD = hx('4E9A52')
CARD = hx('D9A066'); CARDD = hx('B97F45'); IRON = hx('3A3F4F'); SNOW = hx('F6FBFF'); SNOWD = hx('CADCF2')
PINE = hx('3E9B6E'); PINED = hx('2B7A52'); WATER = hx('3FA7D6'); WATERD = hx('1F6FA3'); RED = hx('E23B3F')
GLASS = hx('BFE6FF'); DARK = hx('10172B')


def fit(c, s, x, y, size, maxw, col, font=CAP, a=1.0):
    w = tw(c, s, size, font)
    if w > maxw: size *= maxw / w
    txt(c, s, x, y, size, col, font, a=a)


def sweat(c, x, y, s, g, f, n=4, a0=-2.75, da=0.5):
    for i in range(n):
        ph = (g * 2.4 + i / n) % 1
        ang = a0 + i * da; rr = (150 + 95 * ph) * s
        wcirc(c, x + math.cos(ang) * rr * 0.72, y + math.sin(ang) * rr * 0.6, (15 - 9 * ph) * s, ('sw', i), f, amp=1); fs(c, hx('8FD9FA'), 4)


def tickbadge(c, x, y, k, f, key='tk', r=54):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k); c.new_path(); c.arc(0, 0, r, 0, 2 * math.pi); fs(c, GREEN, 8)
    wline(c, [(-r * 0.44, r * 0.04), (-r * 0.13, r * 0.37), (r * 0.48, -r * 0.33)], key, f, lw=r * 0.24, col=WHITE, amp=0.5); c.restore()


def strip(c, y, lines, k, size=38, w=None):
    if k <= 0: return
    c.select_font_face(HAND); c.set_font_size(size)
    ww = (w or max(c.text_extents(s)[4] for s in lines) + 70); hh = len(lines) * size * 1.5 + 14
    c.save(); c.translate(540, y)
    rrect(c, -ww / 2, -hh / 2, ww, hh, 22); rgb(c, INK, 0.88 * k); c.fill()
    for i, s in enumerate(lines):
        txt(c, s, 0, -hh / 2 + size * 1.22 + i * size * 1.5, size, CREAM, HAND, a=k)
    c.restore()


def cam(c, z, fx, fy):
    c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)


def make_draw(SCENES, TR=0.22):
    def draw(c, g, f):
        for i, (a, b, fn) in enumerate(SCENES):
            if a <= g < b or (i == len(SCENES) - 1 and g >= b):
                loc = g - a
                if i >= 1 and loc < TR:
                    o = eout(loc / TR)
                    pa, pb, pfn = SCENES[i - 1]
                    c.save(); c.translate(0, -H * o); c.rectangle(0, 0, W, H); c.clip(); pfn(c, pb - pa - 0.001, f, pb - 0.001); c.restore()
                    c.save(); c.translate(0, H * (1 - o)); c.rectangle(0, 0, W, H); c.clip(); fn(c, loc, f, g); c.restore()
                else:
                    c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, loc, f, g); c.restore()
                return
    return draw


def panel(c, x, y, w, h, text, size, k=1.0, col=GOLD):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k)
    rrect(c, -w / 2 + 12, -h / 2 + 14, w, h, 44); rgb(c, CORAL); c.fill()
    rrect(c, -w / 2, -h / 2, w, h, 44); rgb(c, INK); c.fill()
    fit(c, text, 0, size * 0.36, size, w - 80, col); c.restore()


def cloud(c, x, y, s, a=1.0, col=WHITE):
    for dx, dy, r in ((-60, 10, 44), (0, -14, 60), (64, 8, 46), (0, 22, 50)):
        c.new_path(); c.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi); rgb(c, col, a); c.fill()


def floor(c, y, col, line=True):
    c.rectangle(0, y, W, H - y); rgb(c, col); c.fill()
    if line:
        c.move_to(0, y); c.line_to(W, y); rgb(c, INK); c.set_line_width(9); c.stroke()


def sign(c, x, y, text, col=GOLD, tcol=INK, size=58, rot=0.0, padx=34, k=1.0, lw=8):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    w = tw(c, text, size) + 2 * padx; h = size * 1.55
    rrect(c, -w / 2, -h / 2, w, h, 18); fs(c, col, lw)
    txt(c, text, 0, size * 0.36, size, tcol); c.restore()


def truck(c, x, y, s, f, g, col=BLUE, label=None, key='trk', lcol=WHITE, lsize=40):
    """x, y = ground point under the middle, drives to the right"""
    c.save(); c.translate(x, y); c.scale(s, s)
    bob = 3 * math.sin(g * 14)
    rrect(c, -240, -262 + bob, 330, 212, 18); fs(c, col, 9)
    rrect(c, 96, -196 + bob, 138, 146, 24); fs(c, CREAM, 9)
    rrect(c, 136, -174 + bob, 78, 58, 10); fs(c, GLASS, 6)
    for wx in (-150, 150):
        c.new_path(); c.arc(wx, -38, 42, 0, 2 * math.pi); fs(c, IRON, 9)
        c.new_path(); c.arc(wx, -38, 14, 0, 2 * math.pi); rgb(c, STEEL); c.fill()
    if label:
        for i, s2 in enumerate(label):
            fit(c, s2, -75, -168 + bob + i * lsize * 1.25 - (len(label) - 1) * lsize * 0.6 + lsize * 0.36, lsize, 290, lcol)
    c.restore()


def qmarks(c, pts, t, t0, col=WHITE, size=120):
    for i, (x, y, r) in enumerate(pts):
        k = eback(seg(t, t0 + i * 0.25, t0 + 0.3 + i * 0.25))
        if k > 0.01:
            c.save(); c.translate(x, y); c.rotate(r); c.scale(k, k); txt(c, "?", 0, size * 0.36, size, col); c.restore()
