from nkit import *


def crowb(c, x, y, s, f, g, key, asleep=False, flap=0.0, d=1):
    c.save(); c.translate(x, y); c.scale(s * d, s)
    for lx in (-8, 8):
        c.new_path(); c.move_to(lx, -6); c.line_to(lx, 8); rgb(c, GOLD); c.set_line_width(4); c.stroke()
    if flap > 0:
        fl = math.sin(g * 26)
        for sg in (-1, 1):
            c.new_path(); c.move_to(sg * 14, -40); c.line_to(sg * 66, -62 - 26 * fl); c.line_to(sg * 30, -22); c.close_path(); fs(c, hx('2A2D4A'), 5)
    c.save(); c.scale(1, 0.82); c.new_path(); c.arc(0, -40, 34, 0, 2 * math.pi); c.restore(); fs(c, hx('4A4F86'), 6)
    c.new_path(); c.move_to(26, -40); c.line_to(54, -32); c.line_to(26, -24); c.close_path(); fs(c, GOLD, 4)
    if asleep:
        c.new_path(); c.arc(12, -40, 7, 0.1 * math.pi, 0.9 * math.pi); rgb(c, WHITE); c.set_line_width(3.5); c.stroke()
    else:
        c.new_path(); c.arc(12, -42, 8, 0, 2 * math.pi); rgb(c, WHITE); c.fill(); c.new_path(); c.arc(14, -42, 4, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.restore()


def scA(c, t, f, g): field_scene(c, t, f, g, tease=False)


def fence(c, f):
    for i in range(5):
        px = 130 + i * 112
        wline(c, [(px, 1340), (px, 1262)], ('fp', i), f, lw=12, col=hx('2B2F55'), amp=0.5)
    wline(c, [(110, 1290), (610, 1290)], 'fr', f, lw=9, col=hx('2B2F55'), amp=0.5)


def scB(c, t, f, g):
    ext_begin(c, f, g)
    REV = 1.25
    c.save(); c.translate(330, 1300); c.scale(1, 0.3); c.new_path(); c.arc(0, 0, 330, math.pi, 2 * math.pi); c.restore(); rgb(c, hx('1D3A2E')); c.fill()
    hp = seg(t, 3.0, 4.3); sx_ = lerp(330, 420, ease(hp)); hop = 46 * abs(math.sin(hp * math.pi * 3))
    lit = ease(seg(t, REV, REV + 0.25))
    if lit > 0:
        gl = cairo.RadialGradient(330, 1150, 20, 330, 1150, 330)
        gl.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.4 * lit); gl.add_color_stop_rgba(1, 1, 0.9, 0.6, 0)
        c.set_source(gl); c.rectangle(0, 800, 700, 700); c.fill()
    front = hp > 0.3
    if not front: scarep(c, sx_, 1336 - hop, 0.8, 'fig', f, g, sil=(t < REV), mood='sad' if t < 2.6 else 'happy', look=(1, 0.4))
    fence(c, f)
    stopped_bus(c, f, g, otto=None, door=1.0)
    if front: scarep(c, sx_, 1336 + 60 * ease(seg(hp, 0.3, 1.0)) - hop, 0.8, 'fig', f, g, mood='joy', look=(1, 0.2), rot=0.05 * math.sin(g * 14))
    w = ease(seg(t, 0.0, 1.1)); ox = lerp(600, 520, w)
    otto_full(c, ox, 1396, 0.55, 'of', f, eyes='wide' if t < 2.2 else 'open', mouth='o' if t < 2.2 else 'smile', look=(-1, -0.3), lh=(-150, -120) if t < 3.0 else (-98, 40), rh=(98, 40),
              bob=abs(math.sin(g * 9)) * 6 * (1 if w < 1 else 0))
    hx_, hy_ = ox - 150 * 0.55, 1396 + (-120 - 175) * 0.55
    if t < 3.0:
        c.new_path(); c.arc(hx_ - 8, hy_ - 8, 15, 0, 2 * math.pi); fs(c, GOLD, 5)
        rays(c, hx_ - 8, hy_ - 8, 24, 40 + 6 * math.sin(g * 12), 8, GOLD, 0.8, f, 'lamp', lw=4)
    if REV <= t < REV + 0.6: txt(c, "!", ox + 60, 1140, 100, GOLD, SERIF)
    if 1.9 < t < 2.9: drops(c, 300, 1100, g)
    ext_end(c, g, 0.24)
    cap2(c, t, 0.2, ["A scarecrow."], y=250, size=90, gold=True, t1=2.0)
    cap2(c, t, 2.1, ["A long way from its field."], y=250, size=80)


def scC(c, t, f, g):
    fare_scene(c, t, f, g, scarep, button, "The wind blew it away.", "Fare: one coat button.", ps=0.6)


def pic8(c):
    c.rectangle(-200, -150, 400, 300); rgb(c, hx('27326A')); c.fill()
    c.new_path(); c.arc(-110, -70, 30, 0, 2 * math.pi); rgb(c, hx('FFF3C4')); c.fill()
    c.rectangle(-200, 60, 400, 100); rgb(c, hx('5A4A2A')); c.fill()
    for i in range(6):
        c.rectangle(-200, 72 + i * 14, 400, 4); rgb(c, hx('7A6A3A')); c.fill()
    c.rectangle(46, -70, 12, 150); rgb(c, CREAMT); c.fill(); c.rectangle(-10, -44, 124, 12); c.fill()
    for (x, y) in ((-60, 52), (140, 48)):
        c.new_path(); c.arc(x, y, 12, 0, 2 * math.pi); rgb(c, hx('15182E')); c.fill()


def scD(c, t, f, g):
    road_scene(c, t, f, g, scarep, pic8, "the field with the empty pole.", ps=0.36, size2=70, pdy=24)


PX = 720


def scE(c, t, f, g):
    ext_begin(c, f, g)
    bus_ext(c, f, g, -440, 1010, 0.8, door=1.0, otto=None)
    reflect(c, g, -400, 250, 1396, n=3, depth=50)
    c.save(); c.translate(700, GY5 + 14); c.scale(1, 0.2); c.new_path(); c.arc(0, 0, 420, math.pi, 2 * math.pi); c.restore(); fs(c, hx('4A3F26'), 8)
    for i in range(9):
        x = 420 + i * 62
        for sg in (-1, 0, 1):
            wline(c, [(x, GY5 - 2), (x + sg * 10 + 4 * math.sin(g * 2 + i), GY5 - 46)], ('wh', i, sg), f, lw=5, col=hx('C9A84E'), amp=0.5)
    ARR = 1.5
    hp = seg(t, 0.2, ARR); x = lerp(352, PX, ease(hp)); hop = 50 * abs(math.sin(hp * math.pi * 3))
    if t < ARR:
        wline(c, [(PX, GY5), (PX, GY5 - 190)], 'ep', f, lw=14, col=INK, amp=0.4); wline(c, [(PX, GY5), (PX, GY5 - 190)], 'ep2', f, lw=7, col=hx('8A6A4A'), amp=0.3)
        wline(c, [(PX - 90, GY5 - 150), (PX + 90, GY5 - 150)], 'ec', f, lw=12, col=INK, amp=0.4)
    arr = t >= ARR
    if arr: scarep(c, PX, GY5 - 34, 0.8, 'fig', f, g, mood='joy' if t > 2.4 else 'happy', look=(-0.4, 0.2), rot=0.03 * math.sin(g * 5))
    else: scarep(c, x, 1396 - hop, 0.8, 'fig', f, g, mood='happy', look=(1, 0), rot=0.06 * math.sin(g * 14))
    if 0 <= t - ARR < 0.4:
        q = (t - ARR) / 0.4; rays(c, PX, GY5 - 260, 150 + 80 * q, 190 + 130 * q, 10, GOLD, 1 - q, f, 'arr', lw=6)
    homes = ((560, GY5 - 2, 1), (850, GY5 - 2, -1), (900, GY5 - 60, -1))
    perch = ((PX - 120, GY5 - 34 - 196 * 0.8 - 6, 1), (PX + 120, GY5 - 34 - 196 * 0.8 - 6, -1), (PX + 6, GY5 - 34 - 420 * 0.8, -1))
    for i, ((x0, y0, d), (x1, y1, d1)) in enumerate(zip(homes, perch)):
        u = ease(seg(t, 1.9 + i * 0.25, 2.6 + i * 0.25))
        cx_ = lerp(x0, x1, u); cy_ = lerp(y0, y1, u) - 90 * math.sin(u * math.pi)
        crowb(c, cx_, cy_, 1.15, f, g, ('cr', i), asleep=not arr, flap=1.0 if 0 < u < 1 else 0.0, d=d)
        if not arr:
            zk = (g * 0.5 + i * 0.33) % 1
            txt(c, "z", x0 + 30 + 16 * zk, y0 - 60 - 40 * zk, 34, CREAMT, SERIF, a=1 - zk)
    for i in range(3):
        hq = seg(t, 2.9 + i * 0.3, 4.1 + i * 0.3)
        if 0 < hq < 1: heart(c, PX - 60 + i * 60, GY5 - 420 - 80 * hq, 0.6 + 0.12 * i, CORAL, 1 - ein(hq))
    otto_home(c, f, g, t, wave_t=3.1, eyes='closed' if t > 3.6 else 'open', look=(1, -0.3))
    ext_end(c, g, 0.14)
    cap2(c, t, 0.2, ["Its own pole. Its own crows."], y=250, size=78, t1=1.9)
    cap2(c, t, 2.0, ["They waited up all night."], y=250, size=80, gold=True)


def scF(c, t, f, g): pin_scene(c, t, f, g, 8)
def scG(c, t, f, g): melt_scene(c, t, f, g, tease=True)


SCENES = [(0.0, 3.6, scA), (3.6, 8.0, scB), (8.0, 12.4, scC), (12.4, 16.8, scD), (16.8, 21.2, scE), (21.2, 25.6, scF), (25.6, 30.0, scG)]
draw = make_draw(SCENES)


# November 26 retention edit. Values: output seconds, source start, source end.
from edit import edited_draw
EDIT = [(2, 0, 3.6), (3.8, 3.6, 8), (4, 8, 12.4), (3.2, 12.4, 16.8), (5, 16.8, 21.2), (3, 21.2, 25.6), (4, 25.6, 30)]
DURATION = sum(shot[0] for shot in EDIT)
draw = edited_draw(SCENES, EDIT)
